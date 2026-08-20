# Mockbase Product Intelligence System

This Obsidian-compatible vault is the human-readable decision layer for sellable or distributable digital design assets: mockups, templates, asset packs, and visual asset products.

The objective is not to maximise asset output. Each product must test a market hypothesis, produce behavioural evidence, update a versioned Decision Record, and improve the next product choice.

## System boundary

```text
Market Data
→ Opportunity Analysis
→ SEO / Demand Validation
→ Product Decision
→ Build
→ Publish
→ Decision Record
```

Acquisition automation, social posting, outreach, paid advertising, backlinks, email campaigns, and community distribution are out of scope. Decision Records expose an empty `distribution` interface for a future Acquisition Skill; possible channels remain hypotheses until validated.

## Storage model

- `market/`, `ideas/`, and `products/` contain compact human-readable reasoning.
- `data/raw/` preserves explicit JSON, JSONL, and CSV inputs.
- `data/processed/` is reserved for reproducible intermediate exports.
- `data/mockbase.duckdb` is the structured query layer.
- `datasets/` records version, provenance, missing fields, cleaning rules, and quality limits.

Do not mechanically convert raw market records into Markdown. Do not infer absent sales, downloads, views, prices, or user counts.

## Configure the root

```bash
export MOCKBASE_INTELLIGENCE_ROOT=/path/to/mockbase-intelligence
```

Every script also accepts `--root`. No machine-specific absolute path is embedded in the system.

## Import explicit market data

Inspect the source schema before mapping it. Then run:

```bash
python3 scripts/import_market_data.py \
  --root "$MOCKBASE_INTELLIGENCE_ROOT" \
  --source /path/to/explicit-market-export \
  --source-name marketplace-export \
  --dataset-version 2026-08-13-v1 \
  --capture-date 2026-08-13
```

Re-running the same import updates stable entities rather than creating duplicates. Stable product identity is `platform + product_id`, then normalized canonical URL, then a deterministic content hash. Review identity follows the same rule using `review_id` where available.

## Query examples

```bash
python3 scripts/query_mockbase_market.py competitors --keyword "portfolio mockup" --json
python3 scripts/query_mockbase_market.py pricing-distribution --keyword "wedding template" --json
python3 scripts/query_mockbase_market.py crowded-categories --json
python3 scripts/query_mockbase_market.py common-complaints --keyword "packaging mockup" --json
python3 scripts/query_mockbase_market.py editing-workflow-gaps --keyword "phone mockup" --json
python3 scripts/query_mockbase_market.py underserved-niches --keyword "saas onboarding mockup" --json
python3 scripts/query_mockbase_market.py high-demand-low-supply --keyword "editable portfolio mockup" --json
python3 scripts/query_mockbase_market.py related-products --keyword "instagram carousel template" --json
python3 scripts/query_mockbase_market.py seo-opportunity --keyword "editable saas onboarding mockup" --json
```

If the database does not exist, the query returns an explicit `original_skill_analysis_flow` fallback. It does not block the pre-existing Mockbase workflow.

## Decision memory

Create a Decision Record only when formal development investment begins:

```bash
python3 scripts/manage_product_decision.py create \
  --product-name "Product name" \
  --record-json /path/to/evidence-backed-record.json
```

An existing product is not re-decided without new evidence. To append Decision v2:

```bash
python3 scripts/manage_product_decision.py revise \
  --product-name "Product name" \
  --record-json /path/to/revised-record.json \
  --new-evidence "Observed conversion after the 28-day validation window"
```

## Dependency and tests

```bash
python3 -m pip install "duckdb>=1.4,<2"
python3 -m unittest discover -s tests -v
```
