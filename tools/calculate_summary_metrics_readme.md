# calculate_summary_metrics.py

Parses every coded article summary in `1_coded_gbls_corpus_articles/`, calculates reproducible metrics, and writes all artifacts to `2_calculated_metrics/gbls_corpus_metrics/`. Also regenerates the JavaScript metrics explorer data bundle.

## Requirements

Python 3.10+ with pandas and openpyxl:

```bash
pip install pandas openpyxl
```

## Usage

Run from the project root:

```bash
python3 tools/calculate_summary_metrics.py
```

Or from any directory using an absolute path:

```bash
python3 /path/to/tools/calculate_summary_metrics.py
```

## What it does

1. **Reads the schema** — finds and parses the controlled lexicon in `0_human_sources/` to get the current field names and allowed values. No field names are hardcoded in the script.
2. **Discovers source files** — finds all `.md` files in `1_coded_gbls_corpus_articles/`, excluding `template.md` and hidden files.
3. **Parses each file** — extracts citation, all metadata fields, summary text, and proposed contributions. Handles both scalar fields (`Field: value`) and multi-label list fields (YAML list format).
4. **Detects multi-label fields at runtime** — a field is treated as multi-label if any article in the corpus encodes it as a list. No hardcoded assumptions.
5. **Calculates all metrics** — article-level derived fields, aggregate counts, co-occurrence, year breakdowns.
6. **Writes all output files** — CSVs, JSON, Excel workbook, JS bundle, validation report, manifest.
7. **Cleans up obsolete files** — removes metric files for fields that no longer exist in the schema.

## Output files

All files except the JS bundle are written to `2_calculated_metrics/gbls_corpus_metrics/`.

### Article tables

| File | Description |
|------|-------------|
| `articles.csv` | One row per article — all fields including full summary text |
| `articles_core.csv` | Same without `summary_text` |
| `article_features_long.csv` | One row per article-feature assignment; always `present=1` |
| `article_feature_matrix.csv` | Binary article × feature matrix across all feature groups |
| `contributions.csv` | One row per extracted proposed contribution |

### Per-field tables (one pair per schema field)

| File | Description |
|------|-------------|
| `{field}_matrix.csv` | Binary article × value matrix for that field |
| `{field}_counts.csv` | Aggregate article counts and percentages per value |

Current fields: `source_type`, `peer_review`, `evidence_type`, `primary_methodology`, `library_context`, `game_format`, `service_area`, `audience`, `intended_outcome`, `coding_confidence`.

### Aggregate tables

| File | Description |
|------|-------------|
| `feature_counts.csv` | Counts for all feature groups in one table |
| `publication_year_counts.csv` | Article counts by publication year |
| `feature_year_counts.csv` | Feature counts broken down by publication year |
| `feature_cooccurrence.csv` | Pairs of features co-occurring in ≥2 articles, sorted by frequency |
| `dataset_summary.csv` | Headline corpus metrics (one row per metric) |
| `dataset_summary.json` | Same as above in JSON |

### Support files

| File | Description |
|------|-------------|
| `data_dictionary.csv` | Documents every generated file — grain, purpose, primary key |
| `feature_datasets_readme.md` | Human-readable guide to loading the metric files in pandas |
| `gbls_feature_overview.xlsx` | Excel workbook — Dashboard, Year Counts, All Feature Counts, per-field sheets |
| `validation_report.json` | Parse counts, consistency checks, and any warnings |
| `generated_artifact_manifest.json` | List of all generated files with byte sizes and timestamp |

### JavaScript explorer

| File | Description |
|------|-------------|
| `2_calculated_metrics/metrics_explorer_synthesized_data.js` | Data bundle for the standalone metrics explorer at `tools/metrics_explorer/index.html` |

## Counting conventions

- A source contributes **at most one count** per feature value, regardless of how many times a concept appears in its summary prose.
- Multi-label fields (e.g., `Service_Area`, `Audience`) can contribute multiple assignments per article — one per coded value.
- `article_pct` = `article_count / total_articles × 100`
- `article_pct_in_year` uses the number of articles published in that year as the denominator.
- Multi-label values in `articles_core.csv` are pipe-delimited: `learning_and_literacy|programming_and_facilitation`.

## Adding new source files

Drop new `.md` files into `1_coded_gbls_corpus_articles/` following the standard template format and re-run the script. The file count is detected automatically — no configuration changes needed.

## Schema changes

The script reads `0_human_sources/metadata-schema-and-lexicon.md` on every run. To add, rename, or remove a controlled field:

1. Edit the lexicon file.
2. Update the relevant coded summaries.
3. Re-run the script.

Files for removed fields (e.g., `old_field_matrix.csv`) are automatically deleted. Files for new fields are created fresh.

## Validation

After every run, `validation_report.json` confirms:

- Every non-template source file produced exactly one article row.
- All `article_id` values are unique and non-blank.
- `article_features_long.present` contains only `1`.
- The matrix row count equals the article count.
- The sum of `feature_counts.article_count` equals the total feature assignments in the long table.
- All generated CSV files can be loaded by pandas.

Any warnings or failures are listed in `validation_report.json` under `parse_warnings`.

## Loading the outputs in Python / Colab

```python
import pandas as pd

metrics_dir = "2_calculated_metrics/gbls_corpus_metrics"

articles = pd.read_csv(f"{metrics_dir}/articles_core.csv")
features = pd.read_csv(f"{metrics_dir}/article_features_long.csv")
matrix   = pd.read_csv(f"{metrics_dir}/article_feature_matrix.csv")
counts   = pd.read_csv(f"{metrics_dir}/feature_counts.csv")

# Filter to a single feature group
service_area_counts = counts[counts["feature_group"] == "service_area"]

# Articles with a specific service area
learning = features[features["feature_value"] == "learning_and_literacy"]["article_id"]
```
