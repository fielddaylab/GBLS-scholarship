# Run Corpus Metrics

This task is handled by `tools/calculate_metrics.py`.

## To regenerate all metrics (both corpora)

```bash
python3 tools/calculate_metrics.py
```

## To regenerate one corpus only

```bash
python3 tools/calculate_metrics.py --gbls       # GBLS corpus only
python3 tools/calculate_metrics.py --reference  # reference corpus only
```

## Dependencies

```bash
pip install pandas openpyxl
```

## What the script does

- Reads the controlled lexicon from `0_human_sources/` (auto-detects the schema file)
- **GBLS corpus:** parses every `.md` in `1_coded_gbls_corpus_articles/` except `template.md`; writes artifacts to `2_calculated_metrics/gbls_corpus_metrics/`; refreshes `metrics_explorer_synthesized_data.js`
- **Reference corpus:** reads `1_coded_reference_corpus_articles/_manifest.jsonl`; writes artifacts to `2_calculated_metrics/reference_corpus_metrics/`; refreshes `reference_corpus_data.js`
- Removes obsolete schema-derived files from previous runs
- Writes `validation_report.json` and `generated_artifact_manifest.json` in each output directory

See `tools/calculate_metrics_readme.md` for full output file documentation.
