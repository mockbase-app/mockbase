#!/usr/bin/env python3
"""Mockbase digital-asset market storage, queries, provenance, and decision memory."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any
from urllib.parse import urlsplit, urlunsplit


ROOT_ENV = "MOCKBASE_INTELLIGENCE_ROOT"
DB_RELATIVE = Path("data/mockbase.duckdb")
DATA_SUFFIXES = {".json", ".jsonl", ".csv"}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def root_path(value: str | Path | None = None) -> Path:
    configured = value or os.environ.get(ROOT_ENV)
    return Path(configured).expanduser().resolve() if configured else Path(__file__).resolve().parents[1]


def db_path(root: Path) -> Path:
    return root / DB_RELATIVE


def require_duckdb():
    try:
        import duckdb
    except ImportError as exc:
        raise RuntimeError("DuckDB is required for database operations: python3 -m pip install duckdb") from exc
    return duckdb


def initialise_directories(root: Path) -> None:
    for relative in (
        "market/category-analysis", "market/competitor-analysis", "market/pricing-analysis",
        "market/opportunity-analysis", "products", "ideas", "datasets", "templates",
        "data/raw", "data/processed",
    ):
        (root / relative).mkdir(parents=True, exist_ok=True)


def initialise_database(root: Path) -> None:
    initialise_directories(root)
    duckdb = require_duckdb()
    connection = duckdb.connect(str(db_path(root)))
    try:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
          product_key VARCHAR PRIMARY KEY, product_id VARCHAR, name VARCHAR, title VARCHAR,
          description VARCHAR, category VARCHAR, subcategory VARCHAR, tags VARCHAR,
          creator VARCHAR, platform VARCHAR, canonical_url VARCHAR, price DOUBLE,
          currency VARCHAR, views BIGINT, likes BIGINT, downloads BIGINT, sales BIGINT,
          rating DOUBLE, reviews_count BIGINT, last_updated TIMESTAMP,
          last_updated_raw VARCHAR, first_seen TIMESTAMP, source VARCHAR,
          dataset_version VARCHAR, raw_json VARCHAR
        );
        CREATE TABLE IF NOT EXISTS reviews (
          review_key VARCHAR PRIMARY KEY, review_id VARCHAR, product_key VARCHAR,
          product_id VARCHAR, review_text VARCHAR, rating DOUBLE, review_date TIMESTAMP,
          review_date_raw VARCHAR, author VARCHAR, platform VARCHAR, source VARCHAR,
          dataset_version VARCHAR, raw_json VARCHAR
        );
        CREATE TABLE IF NOT EXISTS market_observations (
          observation_key VARCHAR PRIMARY KEY, keyword VARCHAR, product_key VARCHAR,
          product_id VARCHAR, rank BIGINT, result_count BIGINT, platform VARCHAR,
          observation_date DATE, source VARCHAR, dataset_version VARCHAR, raw_json VARCHAR
        );
        CREATE TABLE IF NOT EXISTS review_derivations (
          review_key VARCHAR, field_name VARCHAR, value_text VARCHAR, value_boolean BOOLEAN,
          derivation_method VARCHAR, model_version VARCHAR, analysis_date DATE,
          confidence DOUBLE, PRIMARY KEY(review_key, field_name)
        );
        CREATE TABLE IF NOT EXISTS dataset_imports (
          import_key VARCHAR PRIMARY KEY, dataset_version VARCHAR, source VARCHAR,
          capture_date DATE, import_date TIMESTAMP, product_count BIGINT,
          review_count BIGINT, observation_count BIGINT, category_count BIGINT,
          missing_fields VARCHAR, duplicates_removed VARCHAR, cleaning_rules VARCHAR,
          known_data_quality_issues VARCHAR, source_files VARCHAR
        );
        """)
    finally:
        connection.close()


def hash_key(*values: Any) -> str:
    text = "\x1f".join("" if value is None else str(value).strip() for value in values)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def first(record: dict[str, Any], *fields: str) -> Any:
    for field in fields:
        if field in record and record[field] not in (None, ""):
            return record[field]
    return None


def text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    value = str(value).strip()
    return value or None


def number(value: Any, integer: bool = False) -> float | int | None:
    if value in (None, "") or isinstance(value, bool):
        return None
    try:
        parsed = float(str(value).replace(",", "").strip())
        return int(parsed) if integer else parsed
    except (TypeError, ValueError):
        return None


def timestamp(value: Any) -> datetime | None:
    if not value or not re.match(r"^\d{4}-\d{2}-\d{2}", str(value).strip()):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
        return parsed.astimezone(timezone.utc).replace(tzinfo=None) if parsed.tzinfo else parsed
    except ValueError:
        return None


def day(value: Any) -> date | None:
    parsed = timestamp(value)
    return parsed.date() if parsed else None


def canonical_url(value: Any) -> str | None:
    if not value:
        return None
    try:
        parts = urlsplit(str(value).strip())
        path = re.sub(r"/+", "/", parts.path).rstrip("/") or "/"
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))
    except ValueError:
        return text(value)


def normalised_platform(record: dict[str, Any], source_name: str) -> str:
    value = text(first(record, "platform", "marketplace")) or source_name
    return re.sub(r"\s+", "-", value.lower())


def product_identity(record: dict[str, Any], platform: str) -> tuple[str, str | None]:
    product_id = text(first(record, "product_id", "id"))
    if product_id:
        return f"{platform}:{product_id}", product_id
    url = canonical_url(first(record, "canonical_url", "url"))
    if url:
        return f"{platform}:url:{hash_key(url)}", None
    return f"{platform}:hash:{hash_key(first(record, 'name', 'title'), first(record, 'creator'), first(record, 'description'))}", None


def review_identity(record: dict[str, Any], platform: str, product_key: str | None) -> tuple[str, str | None]:
    review_id = text(first(record, "review_id", "id"))
    if review_id:
        return f"{platform}:{review_id}", review_id
    return f"{platform}:hash:{hash_key(product_key, first(record, 'review_text', 'text'), first(record, 'author'), first(record, 'review_date'))}", None


def read_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".jsonl":
        rows = []
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError(f"{path}:{line_number}: expected an object")
                rows.append(row)
        return rows
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in ("products", "reviews", "observations", "records", "items", "data"):
            if isinstance(value.get(key), list):
                return [row for row in value[key] if isinstance(row, dict)]
        return [value]
    return []


def discover_files(sources: list[Path]) -> list[Path]:
    found: set[Path] = set()
    for source in sources:
        if source.is_file() and source.suffix.lower() in DATA_SUFFIXES:
            found.add(source.resolve())
        elif source.is_dir():
            found.update(path.resolve() for path in source.rglob("*") if path.is_file() and path.suffix.lower() in DATA_SUFFIXES)
    return sorted(found)


def record_type(record: dict[str, Any], filename: str) -> str | None:
    name = filename.lower()
    if "observation" in name or ("keyword" in record and any(field in record for field in ("rank", "result_count", "observation_date"))):
        return "market_observations"
    if "review" in name or "comment" in name or "review_text" in record:
        return "reviews" if first(record, "review_text", "text", "comment") is not None else None
    if any(field in record for field in ("product_id", "canonical_url", "url")) and any(field in record for field in ("name", "title", "description")):
        return "products"
    return None


def derive_review(review_text: str) -> dict[str, tuple[str | None, bool | None, float]]:
    lowered = review_text.lower()
    has = lambda *terms: any(term in lowered for term in terms)
    editing = has("smart object", "edit", "editable", "photoshop")
    workflow = editing and has("slow", "too long", "takes", "manual", "workflow")
    resolution = has("resolution", "blurry", "pixelated", "low quality")
    compatibility = has("compatible", "doesn't work", "cannot open", "won't open")
    format_issue = has("file format", "wrong format", "psd only", "figma only")
    customisation = has("customise", "customize", "change color", "change colour")
    pricing = has("expensive", "overpriced", "refund", "subscription")
    licensing = has("license", "licensing", "copyright")
    commercial = has("commercial use", "client work", "resell")
    feature = has("please", "wish", "feature request", "could you", "allow")
    negative = any((workflow, resolution, compatibility, format_issue, pricing, licensing)) or has("broken", "poor", "bad")
    positive = has("great", "excellent", "love", "helpful", "amazing")
    complaint = [name for flag, name in (
        (workflow, "editing_workflow_friction"), (resolution, "resolution_quality"),
        (compatibility, "compatibility"), (format_issue, "format"),
        (customisation, "customisation"), (pricing, "pricing"), (licensing, "licensing"),
    ) if flag]
    return {
        "sentiment": ("negative" if negative else "positive" if positive else "neutral", None, 0.72),
        "complaint_type": (",".join(complaint) or None, None, 0.76),
        "feature_request": (None, feature, 0.78),
        "quality_issue": (None, resolution or has("poor quality"), 0.80),
        "editing_issue": (None, editing, 0.80),
        "compatibility_issue": (None, compatibility, 0.78),
        "format_issue": (None, format_issue, 0.78),
        "resolution_issue": (None, resolution, 0.86),
        "customisation_issue": (None, customisation, 0.76),
        "pricing_issue": (None, pricing, 0.82),
        "licensing_issue": (None, licensing, 0.84),
        "commercial_use_issue": (None, commercial, 0.86),
        "workflow_gap": (None, workflow, 0.85),
        "workaround_detected": (None, has("manual", "workaround", "instead", "photoshop"), 0.74),
    }


def upsert(connection: Any, table: str, key_name: str, row: dict[str, Any]) -> bool:
    duplicate = connection.execute(f"SELECT 1 FROM {table} WHERE {key_name} = ?", [row[key_name]]).fetchone() is not None
    connection.execute(f"DELETE FROM {table} WHERE {key_name} = ?", [row[key_name]])
    columns = list(row)
    connection.execute(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
        [row[column] for column in columns],
    )
    return duplicate


def map_product(connection: Any, platform: str, product_id: str | None) -> str | None:
    if not product_id:
        return None
    direct = f"{platform}:{product_id}"
    if connection.execute("SELECT 1 FROM products WHERE product_key = ?", [direct]).fetchone():
        return direct
    row = connection.execute("SELECT product_key FROM products WHERE product_id = ? LIMIT 1", [product_id]).fetchone()
    return row[0] if row else None


def import_market_data(root: Path, sources: list[Path], source_name: str, dataset_version: str, capture_date: date | None) -> dict[str, Any]:
    initialise_database(root)
    files = discover_files(sources)
    if not files:
        raise ValueError("No JSON, JSONL, or CSV market-data files found in the explicit source")
    raw_target = root / "data" / "raw" / slugify(dataset_version)
    raw_target.mkdir(parents=True, exist_ok=True)
    for source_file in files:
        destination = raw_target / source_file.name
        if destination.resolve() != source_file.resolve():
            shutil.copy2(source_file, destination)

    records: dict[str, list[dict[str, Any]]] = defaultdict(list)
    observed_fields: dict[str, set[str]] = defaultdict(set)
    for source_file in files:
        for record in read_records(source_file):
            kind = record_type(record, source_file.name)
            if kind:
                records[kind].append(record)
                observed_fields[kind].update(record)

    duckdb = require_duckdb()
    connection = duckdb.connect(str(db_path(root)))
    duplicates = Counter()
    quality_issues: list[str] = []
    try:
        connection.execute("BEGIN")
        for record in records["products"]:
            platform = normalised_platform(record, source_name)
            key, product_id = product_identity(record, platform)
            raw_updated = text(first(record, "last_updated", "updated_at"))
            row = {
                "product_key": key, "product_id": product_id,
                "name": text(first(record, "name")), "title": text(first(record, "title")),
                "description": text(first(record, "description")), "category": text(first(record, "category")),
                "subcategory": text(first(record, "subcategory")), "tags": text(first(record, "tags")),
                "creator": text(first(record, "creator", "author")), "platform": platform,
                "canonical_url": canonical_url(first(record, "canonical_url", "url")),
                "price": number(first(record, "price")), "currency": text(first(record, "currency")),
                "views": number(first(record, "views"), True), "likes": number(first(record, "likes"), True),
                "downloads": number(first(record, "downloads"), True), "sales": number(first(record, "sales"), True),
                "rating": number(first(record, "rating")), "reviews_count": number(first(record, "reviews_count"), True),
                "last_updated": timestamp(raw_updated), "last_updated_raw": raw_updated,
                "first_seen": timestamp(first(record, "first_seen")), "source": source_name,
                "dataset_version": dataset_version, "raw_json": json.dumps(record, ensure_ascii=False, sort_keys=True),
            }
            if upsert(connection, "products", "product_key", row):
                duplicates["products"] += 1

        for record in records["reviews"]:
            platform = normalised_platform(record, source_name)
            product_id = text(first(record, "product_id"))
            product_key = map_product(connection, platform, product_id)
            review_key, review_id = review_identity(record, platform, product_key or product_id)
            raw_date = text(first(record, "review_date", "date"))
            original_text = text(first(record, "review_text", "text", "comment")) or ""
            row = {
                "review_key": review_key, "review_id": review_id, "product_key": product_key,
                "product_id": product_id, "review_text": original_text,
                "rating": number(first(record, "rating")), "review_date": timestamp(raw_date),
                "review_date_raw": raw_date, "author": text(first(record, "author")),
                "platform": platform, "source": source_name, "dataset_version": dataset_version,
                "raw_json": json.dumps(record, ensure_ascii=False, sort_keys=True),
            }
            if upsert(connection, "reviews", "review_key", row):
                duplicates["reviews"] += 1
            for field_name, (value_text, value_boolean, confidence) in derive_review(original_text).items():
                connection.execute("DELETE FROM review_derivations WHERE review_key = ? AND field_name = ?", [review_key, field_name])
                connection.execute(
                    "INSERT INTO review_derivations VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    [review_key, field_name, value_text, value_boolean, "transparent_keyword_rules", "mockbase-derived-v1", now_utc().date(), confidence],
                )

        for record in records["market_observations"]:
            platform = normalised_platform(record, source_name)
            product_id = text(first(record, "product_id"))
            product_key = map_product(connection, platform, product_id)
            observed = day(first(record, "observation_date", "date"))
            keyword = text(first(record, "keyword", "query"))
            key = f"{platform}:{hash_key(keyword, product_key or product_id, observed, first(record, 'rank'))}"
            row = {
                "observation_key": key, "keyword": keyword, "product_key": product_key,
                "product_id": product_id, "rank": number(first(record, "rank"), True),
                "result_count": number(first(record, "result_count"), True), "platform": platform,
                "observation_date": observed, "source": source_name, "dataset_version": dataset_version,
                "raw_json": json.dumps(record, ensure_ascii=False, sort_keys=True),
            }
            if upsert(connection, "market_observations", "observation_key", row):
                duplicates["market_observations"] += 1

        product_count, review_count, observation_count, category_count = connection.execute(
            "SELECT (SELECT count(*) FROM products), (SELECT count(*) FROM reviews), (SELECT count(*) FROM market_observations), (SELECT count(DISTINCT category) FROM products WHERE category IS NOT NULL)"
        ).fetchone()
        orphan_count = connection.execute("SELECT count(*) FROM reviews WHERE product_key IS NULL").fetchone()[0]
        if orphan_count:
            quality_issues.append(f"{orphan_count} review(s) could not be mapped to a product")
        if any(record.get("last_updated") and timestamp(record.get("last_updated")) is None for record in records["products"]):
            quality_issues.append("Non-ISO last_updated values were preserved only in last_updated_raw")

        expected = {
            "products": ("product_id", "name", "title", "description", "category", "subcategory", "tags", "creator", "platform", "canonical_url", "price", "currency", "views", "likes", "downloads", "sales", "rating", "reviews_count", "last_updated", "first_seen"),
            "reviews": ("review_id", "product_id", "review_text", "rating", "review_date", "author"),
            "market_observations": ("keyword", "product_id", "rank", "result_count", "platform", "observation_date"),
        }
        missing_fields = {kind: [field for field in fields if field not in observed_fields[kind]] for kind, fields in expected.items()}
        cleaning_rules = [
            "Use platform + product_id; otherwise normalized canonical URL; otherwise stable content hash",
            "Keep absent fields NULL and never convert likes, views, downloads, or sales into one another",
            "Preserve each source record unchanged in raw_json",
            "Keep derived review intelligence separate from original review text with field-level provenance",
        ]
        import_key = f"{dataset_version}:{hash_key(source_name, *map(str, files))[:16]}"
        connection.execute("DELETE FROM dataset_imports WHERE import_key = ?", [import_key])
        connection.execute(
            "INSERT INTO dataset_imports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [import_key, dataset_version, source_name, capture_date, now_utc().replace(tzinfo=None), product_count,
             review_count, observation_count, category_count, json.dumps(missing_fields, ensure_ascii=False),
             json.dumps(dict(duplicates), ensure_ascii=False), json.dumps(cleaning_rules, ensure_ascii=False),
             json.dumps(quality_issues, ensure_ascii=False), json.dumps([str(path) for path in files], ensure_ascii=False)],
        )
        connection.execute("COMMIT")
    except Exception:
        connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()

    result = {
        "dataset_version": dataset_version, "source": source_name,
        "capture_date": capture_date.isoformat() if capture_date else None,
        "import_date": now_utc().isoformat(), "product_count": product_count,
        "review_count": review_count, "observation_count": observation_count,
        "category_count": category_count,
        "duplicates_removed": {key: duplicates[key] for key in ("products", "reviews", "market_observations")},
        "missing_fields": missing_fields, "cleaning_rules": cleaning_rules,
        "known_data_quality_issues": quality_issues, "source_files": [str(path) for path in files],
    }
    write_dataset_notes(root, result)
    return result


def write_dataset_notes(root: Path, result: dict[str, Any]) -> None:
    version = [
        "# Dataset version", "", f"dataset_version: {result['dataset_version']}",
        f"source: {result['source']}", f"capture_date: {result['capture_date'] or 'null'}",
        f"import_date: {result['import_date']}", f"product_count: {result['product_count']}",
        f"review_count: {result['review_count']}", f"observation_count: {result['observation_count']}",
        f"category_count: {result['category_count']}",
        f"missing_fields: {json.dumps(result['missing_fields'], ensure_ascii=False, sort_keys=True)}",
        f"duplicates_removed: {json.dumps(result['duplicates_removed'], ensure_ascii=False, sort_keys=True)}",
        "cleaning_rules:", *[f"  - {rule}" for rule in result["cleaning_rules"]],
        "known_data_quality_issues:", *[f"  - {issue}" for issue in result["known_data_quality_issues"] or ["None detected by importer"]],
        "source_files:", *[f"  - {path}" for path in result["source_files"]], "",
    ]
    (root / "datasets" / "dataset-version.md").write_text("\n".join(version), encoding="utf-8")
    quality = [
        "# Data quality", "", "Only observed source facts are stored. Missing values remain NULL.", "",
        f"- Dataset version: `{result['dataset_version']}`",
        f"- Missing fields: `{json.dumps(result['missing_fields'], ensure_ascii=False, sort_keys=True)}`",
        "- Known issues:", *[f"  - {issue}" for issue in result["known_data_quality_issues"] or ["None detected by importer"]], "",
    ]
    (root / "datasets" / "data-quality.md").write_text("\n".join(quality), encoding="utf-8")


def keyword_filter(keyword: str, alias: str = "p") -> tuple[str, list[str]]:
    tokens = [token for token in re.findall(r"[a-z0-9]+", keyword.lower()) if len(token) > 2]
    if not tokens:
        return "TRUE", []
    haystack = f"lower(coalesce({alias}.name,'') || ' ' || coalesce({alias}.title,'') || ' ' || coalesce({alias}.description,'') || ' ' || coalesce({alias}.tags,'') || ' ' || coalesce({alias}.category,'') || ' ' || coalesce({alias}.subcategory,''))"
    return "(" + " OR ".join(f"{haystack} LIKE ?" for _ in tokens) + ")", [f"%{token}%" for token in tokens]


def competitors(connection: Any, keyword: str) -> list[dict[str, Any]]:
    where, parameters = keyword_filter(keyword)
    result = connection.execute(
        f"SELECT product_key, product_id, coalesce(name,title) AS product_name, category, subcategory, creator, platform, canonical_url, price, currency, views, likes, downloads, sales, rating, reviews_count, last_updated, last_updated_raw FROM products p WHERE {where} ORDER BY coalesce(downloads,sales,views,likes,0) DESC, product_name LIMIT 100",
        parameters,
    )
    columns = [description[0] for description in result.description]
    return [dict(zip(columns, row)) for row in result.fetchall()]


def pain_clusters(connection: Any, product_keys: list[str] | None = None) -> tuple[list[dict[str, Any]], int]:
    if product_keys == []:
        return [], 0
    parameters: list[Any] = []
    product_filter = ""
    if product_keys is not None:
        product_filter = f"AND r.product_key IN ({', '.join('?' for _ in product_keys)})"
        parameters.extend(product_keys)
    rows = connection.execute(
        f"""SELECT r.review_key, r.product_key, r.review_text,
          max(CASE WHEN d.field_name='workflow_gap' AND d.value_boolean THEN 1 ELSE 0 END) workflow,
          max(CASE WHEN d.field_name='resolution_issue' AND d.value_boolean THEN 1 ELSE 0 END) resolution,
          max(CASE WHEN d.field_name='compatibility_issue' AND d.value_boolean THEN 1 ELSE 0 END) compatibility,
          max(CASE WHEN d.field_name='format_issue' AND d.value_boolean THEN 1 ELSE 0 END) format_issue,
          max(CASE WHEN d.field_name='customisation_issue' AND d.value_boolean THEN 1 ELSE 0 END) customisation,
          max(CASE WHEN d.field_name='pricing_issue' AND d.value_boolean THEN 1 ELSE 0 END) pricing,
          max(CASE WHEN d.field_name='licensing_issue' AND d.value_boolean THEN 1 ELSE 0 END) licensing
        FROM reviews r JOIN review_derivations d USING(review_key)
        WHERE r.product_key IS NOT NULL {product_filter}
        GROUP BY r.review_key, r.product_key, r.review_text""",
        parameters,
    ).fetchall()
    definitions = (
        ("editing_workflow_friction", 3), ("resolution_quality", 4),
        ("compatibility", 5), ("format", 6), ("customisation", 7),
        ("pricing", 8), ("licensing", 9),
    )
    clusters = []
    for cluster_name, position in definitions:
        matched = [row for row in rows if row[position]]
        if matched:
            product_count = len({row[1] for row in matched})
            clusters.append({
                "pain_cluster": cluster_name, "review_count": len(matched),
                "product_count": product_count,
                "priority": "cross_product" if product_count > 1 else "isolated",
                "evidence": [row[2] for row in matched[:5]],
            })
    clusters.sort(key=lambda value: (-value["product_count"], -value["review_count"], value["pain_cluster"]))
    return clusters, len(rows)


def pricing_summary(products: list[dict[str, Any]]) -> dict[str, Any]:
    prices = [float(product["price"]) for product in products if product["price"] is not None]
    free = sum(price == 0 for price in prices)
    paid = sum(price > 0 for price in prices)
    return {
        "priced_product_count": len(prices), "median_price": median(prices) if prices else None,
        "average_price": sum(prices) / len(prices) if prices else None,
        "free_count": free, "paid_count": paid,
        "free_paid_ratio": (free / paid) if paid else None,
    }


def supply_analysis(connection: Any, products: list[dict[str, Any]]) -> dict[str, Any]:
    keys = [product["product_key"] for product in products]
    creators = Counter(product["creator"] for product in products if product["creator"])
    creator_top_share = (max(creators.values()) / len(products)) if products and creators else None
    review_count = 0
    if keys:
        review_count = connection.execute(
            f"SELECT count(*) FROM reviews WHERE product_key IN ({', '.join('?' for _ in keys)})",
            keys,
        ).fetchone()[0]
    token_sets = []
    for product in products:
        value = " ".join(str(product.get(field) or "") for field in ("product_name", "category", "subcategory"))
        token_sets.append(set(re.findall(r"[a-z0-9]+", value.lower())))
    similarities = []
    for index, left in enumerate(token_sets):
        for right in token_sets[index + 1:]:
            union = left | right
            similarities.append(len(left & right) / len(union) if union else 0.0)
    dated = [product["last_updated"] for product in products if product["last_updated"] is not None]
    raw_only = sum(product["last_updated"] is None and product["last_updated_raw"] is not None for product in products)
    return {
        "similar_product_count": len(products), "creator_count": len(creators),
        "creator_concentration_top_share": creator_top_share,
        "review_count": review_count,
        "review_density": (review_count / len(products)) if products else None,
        "homogeneity_score": (sum(similarities) / len(similarities)) if similarities else None,
        "update_recency": {
            "dated_product_count": len(dated),
            "oldest_update": min(dated) if dated else None,
            "newest_update": max(dated) if dated else None,
            "raw_date_only_count": raw_only,
        },
        "pricing": pricing_summary(products),
        "existing_supply_adequacy": "requires joint demand, pain, quality, and differentiation evidence",
    }


def execute_query(root: Path, command: str, keyword: str) -> dict[str, Any]:
    database = db_path(root)
    if not database.is_file():
        return {"database_available": False, "fallback_required": True, "fallback": "original_skill_analysis_flow", "reason": "database_not_found"}
    duckdb = require_duckdb()
    connection = duckdb.connect(str(database), read_only=True)
    try:
        related = competitors(connection, keyword)
        keys = [product["product_key"] for product in related]
        clusters, mapped_reviews = pain_clusters(connection, keys)
        if command in ("competitors", "related-products"):
            return {"database_available": True, "keyword": keyword, "similar_product_count": len(related), "supply_analysis": supply_analysis(connection, related), "products": related}
        if command == "pricing-distribution":
            return {"database_available": True, "keyword": keyword, **pricing_summary(related)}
        if command in ("common-complaints", "editing-workflow-gaps"):
            if command == "editing-workflow-gaps":
                clusters = [cluster for cluster in clusters if cluster["pain_cluster"] == "editing_workflow_friction"]
            return {"database_available": True, "keyword": keyword, "mapped_review_count": mapped_reviews, "pain_clusters": clusters}
        if command == "crowded-categories":
            result = connection.execute("SELECT category, count(*) product_count, count(DISTINCT creator) creator_count, median(price) median_price FROM products WHERE category IS NOT NULL GROUP BY category ORDER BY product_count DESC")
            columns = [description[0] for description in result.description]
            return {"database_available": True, "categories": [dict(zip(columns, row)) for row in result.fetchall()]}
        if command in ("seo-opportunity", "underserved-niches", "high-demand-low-supply"):
            observation = connection.execute(
                "SELECT max(result_count), max(observation_date), count(*) FROM market_observations WHERE lower(keyword)=lower(?)", [keyword]
            ).fetchone()
            classification = {
                "code": "F", "label": "Insufficient evidence",
                "reason": "Supply, review, and ranking evidence alone do not prove high demand or willingness to pay",
                "priority_rule": "A > E > B; C and D default no-build; F requires lowest-cost validation",
            }
            return {
                "database_available": True, "keyword": keyword,
                "search_intent": "Requires a named user + context + desired presentation outcome",
                "user_pain": "; ".join(cluster["pain_cluster"] for cluster in clusters) or None,
                "existing_supply": supply_analysis(connection, related),
                "competitive_density": len(related), "purchase_intent": "not proven",
                "differentiation": "not proven", "pricing": pricing_summary(related),
                "pain_clusters": [cluster["pain_cluster"] for cluster in clusters],
                "market_observations": {"latest_result_count": observation[0], "latest_observation_date": observation[1], "observation_count": observation[2]},
                "classification": classification,
                "lowest_cost_validation": ["single asset", "small asset pack", "preview test", "free sample", "small paid listing"],
            }
        raise ValueError(f"Unsupported command: {command}")
    finally:
        connection.close()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or f"product-{hash_key(value)[:8]}"


DECISION_FIELDS = (
    "product_name", "product_id", "engine_product_id", "product_type", "created_at", "updated_at",
    "decision_date", "status", "target_user", "job_to_be_done",
    "use_context", "pain", "why_build", "market_evidence", "review_evidence",
    "competitors", "current_alternatives", "why_existing_products_are_insufficient",
    "core_differentiation", "core_value", "allowed_claims", "prohibited_claims",
    "purchase_motivation", "seo_thesis", "keywords", "validation_hypothesis",
    "success_metric", "stop_condition", "validation_url", "product_url",
    "activation_event", "proxy_validation_event",
    "validated_hypotheses", "unvalidated_hypotheses", "success_metrics",
    "validation_window", "stop_conditions", "scale_conditions", "pivot_conditions",
    "dataset_version", "decision_version",
)


def yaml_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def manage_decision(root: Path, product_name: str, record: dict[str, Any], new_evidence: str | None = None) -> dict[str, Any]:
    product_dir = root / "products" / slugify(product_name)
    product_dir.mkdir(parents=True, exist_ok=True)
    decision = product_dir / "decision.md"
    if decision.exists() and not new_evidence:
        return {"action": "no_new_evidence", "decision_path": str(decision), "reason": "Existing decision preserved"}
    if decision.exists():
        current = decision.read_text(encoding="utf-8")
        match = re.search(r"^decision_version:\s*(\d+)", current, re.MULTILINE)
        version = (int(match.group(1)) if match else 1) + 1
        current = re.sub(r"^decision_version:\s*\d+", f"decision_version: {version}", current, count=1, flags=re.MULTILINE)
        appendix = (
            f"\n## Decision v{version}\n\n"
            f"- New evidence: {new_evidence}\n"
            f"- Changed assumption: {record.get('changed_assumption', 'Not specified')}\n"
            f"- Previous decision: {record.get('previous_decision', 'See Decision v1')}\n"
            f"- New decision: {record.get('status', 'Not specified')}\n"
            f"- Next review condition: {record.get('next_review_condition', 'Not specified')}\n"
        )
        decision.write_text(current.rstrip() + "\n" + appendix, encoding="utf-8")
        return {"action": "versioned_update", "decision_version": version, "decision_path": str(decision)}

    now = now_utc()
    values = {field: record.get(field) for field in DECISION_FIELDS}
    values.update(
        product_name=product_name,
        product_id=record.get("product_id") or slugify(product_name),
        created_at=record.get("created_at") or now.isoformat().replace("+00:00", "Z"),
        updated_at=record.get("updated_at") or now.isoformat().replace("+00:00", "Z"),
        decision_date=record.get("decision_date") or now.date().isoformat(),
        decision_version=1,
    )
    for field in ("market_evidence", "review_evidence", "competitors", "current_alternatives", "allowed_claims", "prohibited_claims", "keywords", "validated_hypotheses", "unvalidated_hypotheses", "success_metrics", "stop_conditions", "scale_conditions", "pivot_conditions"):
        values[field] = values[field] or []
    content = ["---", *[f"{field}: {yaml_value(values[field])}" for field in DECISION_FIELDS],
        "distribution:", "  status: not_started", "  acquisition_skill: distribution-acquisition",
        "  registration_product_id: null", "  target_channels: []", "  target_keywords: []",
        "  experiment_ids: []", "  evidence_input_ids: []", "  last_health_state: null",
        "  last_sync_at: null", "---", "",
        f"# {product_name}", "", "## Decision v1", "",
        "This product tests a falsifiable market hypothesis. Asset count and production hours are not core success metrics.", "",
        "## Future distribution hypotheses", "",
        "Possible channels: Marketplace Search, Pinterest, Instagram, design communities, SEO content, tutorial content.", "",
        "Status: Not yet validated.", ""]
    decision.write_text("\n".join(content), encoding="utf-8")
    for filename, heading in (("launch.md", "Launch"), ("experiments.md", "Experiments"), ("review.md", "Product review")):
        (product_dir / filename).write_text(f"# {heading}: {product_name}\n\nNo evidence recorded yet.\n", encoding="utf-8")
    return {"action": "created", "decision_version": 1, "decision_path": str(decision)}
