# Run Corpus Metrics

This task is now handled by a repeatable Python script.

## To regenerate all metrics

```bash
python3 tools/calculate_summary_metrics.py
```

Run from the project root. The script is self-contained — it finds its own paths relative to its location, so it works from any directory:

```bash
python3 /absolute/path/to/tools/calculate_summary_metrics.py
```

## What the script does

1. Reads the controlled lexicon from `0_human_sources/` (auto-detects the schema file by content)
2. Parses every `.md` in `1_coded_gbls_corpus_articles/` except `template.md`
3. Detects which fields are multi-label at run time (no hard-coded assumptions)
4. Writes all metric artifacts to `2_calculated_metrics/gbls_corpus_metrics/`
5. Regenerates `2_calculated_metrics/metrics_explorer_synthesized_data.js`
6. Removes obsolete schema-derived files from previous runs
7. Writes `validation_report.json` and `generated_artifact_manifest.json`

## Dependencies

```bash
pip install pandas openpyxl
```

## Output files

| File | Description |
|------|-------------|
| `articles.csv` | One row per article including full summary text |
| `articles_core.csv` | Same without summary text |
| `article_features_long.csv` | One row per article-feature assignment |
| `article_feature_matrix.csv` | Binary article × feature matrix |
| `{field}_matrix.csv` | Binary matrix per schema field |
| `{field}_counts.csv` | Aggregate counts per schema field |
| `feature_counts.csv` | Counts across all feature groups |
| `publication_year_counts.csv` | Counts by year |
| `feature_year_counts.csv` | Counts by year × feature |
| `feature_cooccurrence.csv` | Co-occurring feature pairs (≥2 articles) |
| `contributions.csv` | One row per extracted proposed contribution |
| `dataset_summary.csv` / `.json` | Headline corpus metrics |
| `gbls_feature_overview.xlsx` | Excel workbook with dashboard and per-field sheets |
| `validation_report.json` | Parse and consistency checks |
| `generated_artifact_manifest.json` | File list with sizes and timestamp |

## Adding new source files

Drop new `.md` coded summaries into `1_coded_gbls_corpus_articles/` and re-run the script.
The number of source files is detected automatically each run — no configuration needed.

## Schema changes

The script reads the schema fresh on every run. Adding, removing, or renaming a
field in `0_human_sources/metadata-schema-and-lexicon.md` is reflected automatically.
Metric files for fields removed from the schema are deleted on the next run.
