import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


VAULT = Path(__file__).resolve().parents[1]
IMPORTER = VAULT / "scripts" / "import_market_data.py"
QUERY = VAULT / "scripts" / "query_mockbase_market.py"
DECISIONS = VAULT / "scripts" / "manage_product_decision.py"


class ProductIntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name)
        self.root = base / "vault"
        self.source = base / "market-data"
        self.source.mkdir()

        products = [
            {
                "product_id": "asset-1",
                "name": "Dark SaaS Onboarding iPhone Mockup",
                "description": "Editable Figma mockup for portfolio case studies",
                "category": "Mockup",
                "subcategory": "Mobile",
                "tags": ["iphone", "saas", "portfolio"],
                "creator": "Studio One",
                "platform": "Design Market",
                "canonical_url": "https://market.example/assets/asset-1",
                "price": 12,
                "currency": "USD",
                "downloads": 140,
                "likes": 38,
                "first_seen": "2026-07-01",
            },
            {
                "product_id": "asset-2",
                "title": "Portfolio Phone Mockup Template",
                "description": "PSD phone scenes for UI case studies",
                "category": "Template",
                "tags": "phone,portfolio,psd",
                "creator": "Studio Two",
                "platform": "Design Market",
                "canonical_url": "https://market.example/assets/asset-2/",
                "price": 0,
                "currency": "USD",
                "downloads": 70,
                "likes": 12,
            },
        ]
        with (self.source / "products.jsonl").open("w", encoding="utf-8") as handle:
            for product in products:
                handle.write(json.dumps(product) + "\n")

        reviews = [
            {
                "review_id": "review-1",
                "product_id": "asset-1",
                "review_text": "Editing every smart object takes too long for a portfolio.",
                "rating": 2,
                "review_date": "2026-08-01",
                "author": "Buyer A",
                "platform": "Design Market",
            },
            {
                "review_id": "review-2",
                "product_id": "asset-2",
                "review_text": "Please make it directly editable; the Photoshop workflow is slow.",
                "rating": 3,
                "review_date": "2026-08-02",
                "author": "Buyer B",
                "platform": "Design Market",
            },
            {
                "review_id": "review-3",
                "product_id": "asset-2",
                "review_text": "The export is blurry at presentation size.",
                "rating": 2,
                "review_date": "2026-08-03",
                "author": "Buyer C",
                "platform": "Design Market",
            },
        ]
        with (self.source / "reviews.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=reviews[0])
            writer.writeheader()
            writer.writerows(reviews)

        observations = [{
            "keyword": "iphone portfolio mockup",
            "product_id": "asset-1",
            "rank": 3,
            "result_count": 84,
            "platform": "Design Market",
            "observation_date": "2026-08-10",
        }]
        (self.source / "market_observations.json").write_text(
            json.dumps(observations), encoding="utf-8"
        )

    def run_cli(self, script, *args, expected=0, env=None):
        result = subprocess.run(
            [sys.executable, str(script), *map(str, args)],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(result.returncode, expected, result.stderr or result.stdout)
        return json.loads(result.stdout)

    def import_data(self):
        return self.run_cli(
            IMPORTER,
            "--root", self.root,
            "--source", self.source,
            "--source-name", "design-market-export",
            "--dataset-version", "market-2026-08-10",
            "--capture-date", "2026-08-10",
        )

    def query(self, command, keyword=""):
        args = ["--root", self.root, command, "--json"]
        if keyword:
            args.extend(["--keyword", keyword])
        return self.run_cli(QUERY, *args)

    def test_existing_market_data_imports_using_discovered_schema(self):
        result = self.import_data()
        self.assertEqual(result["product_count"], 2)
        self.assertEqual(result["review_count"], 3)
        self.assertEqual(result["observation_count"], 1)
        self.assertIn("sales", result["missing_fields"]["products"])
        self.assertTrue((self.root / "data" / "mockbase.duckdb").is_file())

    def test_reviews_map_to_products_and_raw_text_is_preserved(self):
        self.import_data()
        result = self.query("common-complaints", "portfolio mockup")
        self.assertEqual(result["mapped_review_count"], 3)
        evidence = [text for cluster in result["pain_clusters"] for text in cluster["evidence"]]
        self.assertIn("Editing every smart object takes too long for a portfolio.", evidence)

    def test_reimport_is_idempotent(self):
        self.import_data()
        second = self.import_data()
        self.assertEqual(second["product_count"], 2)
        self.assertEqual(second["review_count"], 3)
        self.assertEqual(second["duplicates_removed"], {"products": 2, "reviews": 3, "market_observations": 1})

    def test_competitor_query_finds_related_digital_assets(self):
        self.import_data()
        result = self.query("competitors", "portfolio mockup")
        self.assertEqual(result["similar_product_count"], 2)
        self.assertEqual({item["product_id"] for item in result["products"]}, {"asset-1", "asset-2"})
        supply = result["supply_analysis"]
        self.assertEqual(supply["creator_count"], 2)
        self.assertEqual(supply["creator_concentration_top_share"], 0.5)
        self.assertEqual(supply["review_density"], 1.5)
        self.assertIn("homogeneity_score", supply)
        self.assertEqual(supply["update_recency"]["dated_product_count"], 0)

    def test_pain_clusters_prioritise_repeated_cross_product_workflow_gap(self):
        self.import_data()
        result = self.query("editing-workflow-gaps", "portfolio mockup")
        editing = result["pain_clusters"][0]
        self.assertEqual(editing["pain_cluster"], "editing_workflow_friction")
        self.assertEqual(editing["review_count"], 2)
        self.assertEqual(editing["product_count"], 2)
        self.assertEqual(editing["priority"], "cross_product")

    def test_unrelated_keyword_does_not_borrow_reviews_from_other_products(self):
        self.import_data()
        result = self.query("common-complaints", "wedding invitation stationery")
        self.assertEqual(result["mapped_review_count"], 0)
        self.assertEqual(result["pain_clusters"], [])

    def test_seo_query_combines_intent_supply_pain_and_observations(self):
        self.import_data()
        result = self.query("seo-opportunity", "iphone portfolio mockup")
        self.assertTrue(result["database_available"])
        self.assertEqual(result["existing_supply"]["similar_product_count"], 2)
        self.assertEqual(result["market_observations"]["latest_result_count"], 84)
        self.assertIn("editing_workflow_friction", result["pain_clusters"])
        self.assertEqual(result["classification"]["code"], "F")

    def test_new_product_creates_unified_decision_record_and_distribution_interface(self):
        self.import_data()
        record = {
            "status": "validation",
            "product_type": "mockbase-digital-asset",
            "target_user": "Freelance UI designers creating Behance SaaS case studies",
            "job_to_be_done": "Present an onboarding flow credibly",
            "use_context": "Dark-mode mobile portfolio case study",
            "pain": "Photoshop smart-object editing is slow",
            "why_build": "Test a browser-native editing gap",
            "market_evidence": ["2 related products"],
            "review_evidence": ["2 complaints across 2 products"],
            "competitors": ["asset-1", "asset-2"],
            "current_alternatives": ["Manual Photoshop editing"],
            "why_existing_products_are_insufficient": "Repeated workflow friction",
            "core_differentiation": "Browser-native editing",
            "core_value": "Test a browser-native workflow before full production",
            "purchase_motivation": "Save case-study preparation time",
            "seo_thesis": "Narrow editable portfolio intent",
            "validated_hypotheses": [],
            "unvalidated_hypotheses": ["Browser-native workflow improves conversion"],
            "success_metrics": ["listing_impressions", "conversion_rate", "sales"],
            "validation_window": "28 days",
            "stop_conditions": ["Stop if qualified impressions are sufficient but conversion misses the threshold"],
            "scale_conditions": ["Scale only after the sales threshold passes"],
            "pivot_conditions": ["Pivot positioning after clicks without sales"],
            "dataset_version": "market-2026-08-10",
        }
        record_path = Path(self.temporary.name) / "decision.json"
        record_path.write_text(json.dumps(record), encoding="utf-8")
        result = self.run_cli(
            DECISIONS, "--root", self.root, "create",
            "--product-name", "Browser Native SaaS Mockup",
            "--record-json", record_path,
        )
        content = Path(result["decision_path"]).read_text(encoding="utf-8")
        self.assertIn("decision_version: 1", content)
        self.assertIn('product_id: "browser-native-saas-mockup"', content)
        self.assertIn('product_type: "mockbase-digital-asset"', content)
        self.assertIn("acquisition_skill: distribution-acquisition", content)
        self.assertIn("evidence_input_ids: []", content)
        self.assertIn("status: not_started", content)
        self.assertIn("Status: Not yet validated.", content)

    def test_existing_product_does_not_redecide_without_new_evidence(self):
        record_path = Path(self.temporary.name) / "record.json"
        record_path.write_text(json.dumps({"target_user": "Specific user"}), encoding="utf-8")
        args = ["--root", self.root, "create", "--product-name", "Existing Asset", "--record-json", record_path]
        first = self.run_cli(DECISIONS, *args)
        decision_path = Path(first["decision_path"])
        before = decision_path.read_bytes()
        second = self.run_cli(DECISIONS, *args)
        self.assertEqual(second["action"], "no_new_evidence")
        self.assertEqual(decision_path.read_bytes(), before)

    def test_new_evidence_appends_decision_version_without_overwriting_history(self):
        record_path = Path(self.temporary.name) / "versioned-record.json"
        record_path.write_text(json.dumps({"status": "validation", "target_user": "Specific user"}), encoding="utf-8")
        base_args = ["--root", self.root, "--product-name", "Versioned Asset", "--record-json", record_path]
        created = self.run_cli(DECISIONS, *base_args[:2], "create", *base_args[2:])
        decision_path = Path(created["decision_path"])
        original = decision_path.read_text(encoding="utf-8")
        revised_record = {
            "status": "pivot", "changed_assumption": "Generic positioning was too broad",
            "previous_decision": "validate", "next_review_condition": "After one narrow listing test",
        }
        record_path.write_text(json.dumps(revised_record), encoding="utf-8")
        revised = self.run_cli(
            DECISIONS, *base_args[:2], "revise", *base_args[2:],
            "--new-evidence", "Qualified clicks occurred but no sales",
        )
        content = decision_path.read_text(encoding="utf-8")
        self.assertEqual(revised["decision_version"], 2)
        self.assertIn("## Decision v1", content)
        self.assertIn("## Decision v2", content)
        self.assertIn("Qualified clicks occurred but no sales", content)
        self.assertIn("Generic positioning was too broad", content)
        self.assertIn(original.split("## Decision v1", 1)[1].split("## Future", 1)[0], content)

    def test_missing_database_returns_original_flow_fallback_using_configurable_root(self):
        configured_root = Path(self.temporary.name) / "missing-vault"
        environment = os.environ.copy()
        environment["MOCKBASE_INTELLIGENCE_ROOT"] = str(configured_root)
        result = self.run_cli(QUERY, "competitors", "--keyword", "mockup", "--json", env=environment)
        self.assertFalse(result["database_available"])
        self.assertTrue(result["fallback_required"])
        self.assertEqual(result["fallback"], "original_skill_analysis_flow")


if __name__ == "__main__":
    unittest.main()
