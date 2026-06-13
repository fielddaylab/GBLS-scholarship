# calculate_reference_metrics.py

Reads the coded journal article archive, calculates reproducible metrics for the ~7,200 reference corpus articles (the grey articles in the metrics explorer), and writes all artifacts to `2_calculated_metrics/reference_corpus_metrics/`. Also regenerates `tools/metrics_explorer/reference_corpus_data.js`.

## Requirements

Python 3.10+ with pandas and openpyxl:

```bash
pip install pandas openpyxl
```

## Usage

Run from the project root:

```bash
python3 tools/calculate_reference_metrics.py
```

Or from any directory using an absolute path:

```bash
python3 /path/to/tools/calculate_reference_metrics.py
```

## Source data

The script reads `1_coded_reference_corpus_articles/_manifest.jsonl` — a JSONL file where each line is a structured record for one journal article. This manifest is the authoritative source for the reference corpus; the individual `.md` files in `1_coded_reference_corpus_articles/` are derived from it.

Each manifest record contains:

| Manifest key | Schema field | Type |
|---|---|---|
| `evidence` | `Evidence_Type` | list |
| `method` | `Primary_Methodology` | scalar |
| `context` | `Library_Context` | scalar |
| `game` | `Game_Format` | scalar |
| `services` | `Service_Area` | list |
| `audience` | `Audience` | list |
| `outcomes` | `Intended_Outcome` | list |
| `confidence` | `Coding_Confidence` | scalar |
| `journal` | (extra) | scalar |
| `title` | (extra) | scalar |
| `doi` | (extra) | scalar |

`Source_Type` and `Peer_Review` are fixed as `peer_reviewed_journal_article` / `peer_reviewed` for every record in this corpus.

All coding is based on titles and abstracts only — not full-text review.

## What it does

1. **Reads the schema** — parses `0_human_sources/metadata-schema-and-lexicon.md` for field names and allowed values (same schema used by the GBLS corpus script).
2. **Loads the manifest** — reads all 7,201 records from `_manifest.jsonl`, normalising field names and multi-label list values.
3. **Detects multi-label fields at runtime** — no hardcoded assumptions.
4. **Calculates all metrics** — article-level, aggregate counts, journal breakdown, co-occurrence, year breakdowns.
5. **Writes all output files** — CSVs, JSON, Excel workbook, JS bundle, validation report, manifest.
6. **Cleans up obsolete files** — removes metric files for fields no longer in the schema.

## Output files

All files except the JS bundle are written to `2_calculated_metrics/reference_corpus_metrics/`.

### Article table

| File | Description |
|------|-------------|
| `articles.csv` | One row per article — all fields including journal, title, doi, coding_basis |
| `article_features_long.csv` | One row per article-feature assignment; always `present=1` |
| `article_feature_matrix.csv` | Binary article × feature matrix across all feature groups |

### Per-field tables (one pair per schema field)

| File | Description |
|------|-------------|
| `{field}_matrix.csv` | Binary article × value matrix for that field |
| `{field}_counts.csv` | Aggregate article counts and percentages per value |

### Aggregate tables

| File | Description |
|------|-------------|
| `feature_counts.csv` | Counts for all feature groups in one table |
| `journal_counts.csv` | Article counts per journal, sorted by frequency |
| `publication_year_counts.csv` | Article counts by publication year |
| `feature_year_counts.csv` | Feature counts broken down by publication year |
| `feature_cooccurrence.csv` | Feature pairs co-occurring in ≥2 articles, sorted by frequency |
| `dataset_summary.csv` | Headline corpus metrics (one row per metric) |
| `dataset_summary.json` | Same as above in JSON |

### Support files

| File | Description |
|------|-------------|
| `data_dictionary.csv` | Documents every generated file |
| `readme.md` | Quick-start guide for loading files in pandas |
| `reference_corpus_overview.xlsx` | Excel workbook — Dashboard, Year Counts, Journal Counts, All Feature Counts, per-field sheets |
| `validation_report.json` | Record counts, consistency checks, and any issues |
| `generated_artifact_manifest.json` | All generated files with byte sizes and timestamp |

### JavaScript explorer

| File | Description |
|------|-------------|
| `tools/metrics_explorer/reference_corpus_data.js` | Data bundle powering the grey reference articles in the metrics explorer (`window.GBLS_REFERENCE_CORPUS`) |

## Difference from the GBLS corpus script

| | `calculate_summary_metrics.py` | `calculate_reference_metrics.py` |
|---|---|---|
| Source | `.md` files in `1_coded_gbls_corpus_articles/` | `_manifest.jsonl` in `1_coded_reference_corpus_articles/` |
| Articles | ~200 fully coded | ~7,200 abstract-only coded |
| Extra fields | summary text, contributions | journal, title, doi |
| JS variable | `window.GBLS_METRICS` | `window.GBLS_REFERENCE_CORPUS` |
| Explorer role | Coloured foreground articles | Grey background articles |

## Adding new reference articles

Add new lines to `1_coded_reference_corpus_articles/_manifest.jsonl` and re-run the script. The article count is detected automatically from the manifest.

## Schema changes

The script reads the schema fresh on every run. Changes to `0_human_sources/metadata-schema-and-lexicon.md` are reflected automatically, and metric files for removed fields are deleted on the next run.

## Loading the outputs in Python / Colab

```python
import pandas as pd

metrics_dir = "2_calculated_metrics/reference_corpus_metrics"

articles  = pd.read_csv(f"{metrics_dir}/articles.csv")
features  = pd.read_csv(f"{metrics_dir}/article_features_long.csv")
matrix    = pd.read_csv(f"{metrics_dir}/article_feature_matrix.csv")
counts    = pd.read_csv(f"{metrics_dir}/feature_counts.csv")
journals  = pd.read_csv(f"{metrics_dir}/journal_counts.csv")

# Articles from a specific journal
ccq = articles[articles["journal"] == "Cataloging & Classification Quarterly"]

# Feature counts for service area
service = counts[counts["feature_group"] == "service_area"]
```
