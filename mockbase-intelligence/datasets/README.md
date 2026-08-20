# Datasets

Only explicitly supplied Mockbase digital-asset market data belongs here.

Before import, inspect the actual schema. Map only observed fields; keep absent fields NULL. Preserve raw JSON, JSONL, and CSV under `data/raw/`. Never relabel likes as downloads, views as sales, result counts as search volume, or engagement as willingness to pay.

Each import updates `dataset-version.md` with counts calculated from DuckDB, plus source, capture date, import date, missing fields, duplicates removed, cleaning rules, and known limitations.
