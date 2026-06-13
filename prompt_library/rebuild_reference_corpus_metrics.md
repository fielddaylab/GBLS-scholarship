# Prompt: Rebuild the Abstract-Coded Journal Reference Metrics

Work autonomously and complete this task end to end. Do not ask for project
background, schema details, filenames, or output locations when they can be
discovered from the folder you were given.

## Starting Information

The user will point you to either the GBLS project root or any folder inside
it. Starting from that folder, locate the project root. It is the nearest
ancestor, or a nearby directory, containing these markers:

- `0_human_sources`
- `1_coded_reference_corpus_articles`
- `2_calculated_metrics`
- `tools/metrics_explorer`

Do not rely on a remembered absolute path. Do not search the entire computer
unless ordinary ancestor and sibling discovery fails.

## Objective

Parse the complete abstract-coded journal archive, calculate reproducible
article-level and aggregate metrics, and refresh the gray reference layer used
by the Metrics Explorer.

This corpus is a broad snapshot of library and information science literature.
It is not the curated GBLS corpus. Keep its outputs separate from
`2_calculated_metrics/gbls_corpus_metrics`, which belongs to the curated GBLS corpus.

## Authoritative Inputs

Discover and use:

- Coded articles: `<project root>/1_coded_reference_corpus_articles`
- Preferred input:
  `<project root>/1_coded_reference_corpus_articles/_manifest.jsonl`
- Live metadata schema: the document inside `<project root>/0_human_sources`
  whose contents define the metadata schema and controlled lexicon
- Existing builder, when present:
  `<project root>/2_calculated_metrics/library_journal_reference_metrics/build_reference_metrics.py`

Identify the schema document by contents, not solely by a remembered filename.
Parse it at run time. It is the authority for controlled field names, order,
allowed values, cardinality, definitions, and null conventions.

The JSONL manifest is preferred because it represents one record per coded
article. Verify it against the Markdown archive:

1. Count non-hidden article `.md` files, excluding `_readme.md`.
2. Count nonblank JSONL records.
3. Confirm every JSONL `filename` names an existing Markdown file.
4. Confirm filenames are unique.
5. Confirm representative records agree with their Markdown metadata.
6. Stop with a clear error if the manifest and archive differ. Do not silently
   omit records.

If `_manifest.jsonl` is missing, reconstruct equivalent records from every
article Markdown file using a line-structured Markdown parser.

## Coding Rules

1. Treat each article record as one article.
2. Preserve controlled values exactly as coded.
3. Do not infer new labels during metric calculation.
4. Deduplicate repeated values within an article while preserving order.
5. Counts represent article presence, not term frequency.
6. Keep missing years missing and label them `n.d.` in year summaries.
7. Retain the distinction that this corpus is `abstract_only`.
8. Validate every controlled value against the live schema. Report unknown or
   obsolete values; do not silently remap them.
9. Use `filename` without its extension as `article_id`, unless the archive
   contains a more durable unique identifier.

## Output Locations

Create or replace reference-corpus metrics only in:

`<project root>/2_calculated_metrics/library_journal_reference_metrics`

Refresh the explorer bundle at:

`<project root>/tools/metrics_explorer/reference_corpus_data.js`

Keep both locations synchronized in the same run. Do not place reference CSVs
directly in `2_calculated_metrics/gbls_corpus_metrics`; that location describes the curated GBLS
corpus. Do not alter coded article Markdown.

## Required Article Tables

Write UTF-8 CSV files with headers and no dataframe index.

### `articles.csv`

One row per reference article. Include:

- `article_id`
- `filename`
- `journal`
- `year`
- `year_status`
- `decade`
- `title`
- `authors` when available
- `issue` when available
- `doi`
- `citation`
- `coding_basis`
- one column for every controlled field in the live schema
- a `<field>_count` column for every multi-label controlled field
- `summary_word_count`
- `source_path`
- `summary_text`

Use lowercase snake_case columns and `|` between multiple values.

### `articles_core.csv`

The same rows and columns as `articles.csv`, excluding `summary_text` and
`source_path`.

### `article_features_long.csv`

One row per article-feature assignment with columns:

`article_id`, `year`, `feature_group`, `feature_value`, `feature_column`,
`present`

`present` must always be `1`.

### `article_feature_matrix.csv`

One row per article. Put identity columns first, followed by one binary integer
column per coded feature using:

`<feature_group>__<snake_case_feature_value>`

### Schema-Derived Matrices

For every controlled feature group in the live schema, write:

`<feature_group>_matrix.csv`

Each contains identity columns plus only that group's binary columns.

## Required Aggregate Tables

### `feature_counts.csv`

Columns:

`feature_group`, `feature_value`, `article_count`, `total_articles`,
`article_pct`, `rank_within_group`

Use dense descending rank within each feature group.

For every controlled feature group, also write
`<feature_group>_counts.csv`. It must exactly equal the corresponding subset
of `feature_counts.csv`.

### `publication_year_counts.csv`

Columns: `year_label`, `article_count`, `article_pct`

Include `n.d.` when necessary.

### `feature_year_counts.csv`

Columns:

`year`, `feature_group`, `feature_value`, `article_count`, `total_articles`,
`article_pct_in_year`

The denominator is the number of reference articles in that year.

### `feature_cooccurrence.csv`

One row per unordered pair of distinct features assigned to the same article:

`feature_group_a`, `feature_value_a`, `feature_group_b`, `feature_value_b`,
`article_count`, `article_pct`

Include pairs occurring in at least two articles.

### `journal_counts.csv`

Columns:

`journal`, `article_count`, `total_articles`, `article_pct`, `earliest_year`,
`latest_year`

### `journal_year_counts.csv`

Columns: `journal`, `year`, `article_count`, `journal_year_pct`

Use each journal's article count as the percentage denominator.

### `dataset_summary.csv`

One row per metric with columns `metric` and `value`. Include at least:

- `corpus_role` = `general_literature_reference`
- `coding_basis` = `abstract_only`
- `total_articles`
- `unique_journals`
- `earliest_year`
- `latest_year`
- `missing_year_articles`
- `unique_feature_labels`
- `total_article_feature_assignments`
- `mean_features_per_article`
- `median_summary_word_count`

### `data_dictionary.csv`

Document every generated file, its grain, purpose, and primary key.

## Workbook

Create:

`<project root>/2_calculated_metrics/library_journal_reference_metrics/reference_corpus_feature_overview.xlsx`

Include sheets: Dashboard, Year Counts, Journal Counts, All Feature Counts,
Data Dictionary, and one sheet per controlled feature group. Use frozen
headers, filters or tables where useful, readable widths, plain headers, and
no merged multi-row table headers.

## Documentation and Validation

Create `reference_datasets_readme.md` explaining:

- this is a broad abstract-coded reference corpus, not the GBLS corpus;
- table grains and percentage denominators;
- counts indicate coded article presence;
- abstract-only coding is less reliable than full-text coding;
- how to load the core files with pandas; and
- how to rerun the build.

Create `validation_report.json` containing:

- Markdown article count
- JSONL record count
- parsed article count
- unique and duplicate article ID counts
- missing files referenced by the manifest
- unreferenced Markdown article files
- missing-year count
- unknown controlled values by field
- article-feature assignment count
- sum of `feature_counts.article_count`
- matrix row and binary-column counts
- parse warnings and failures

Validation must confirm:

- one article row per source record;
- unique, nonblank article IDs;
- exact agreement between manifest and Markdown filenames;
- `present` contains only `1`;
- matrix row count equals article count;
- feature count sum equals long-table assignment count;
- generated feature groups exactly match the live schema contract;
- schema-derived files match their source tables;
- all generated CSVs load successfully; and
- the explorer bundle article count matches `articles_core.csv`.

Stop and report a clear error when validation fails.

Create `generated_artifact_manifest.json` listing every generated file, byte
size, row count when applicable, and generation timestamp. Use the previous
manifest to remove obsolete files from earlier reference-metrics runs. Never
delete unrelated files.

## Explorer Bundle

Regenerate `<project root>/tools/metrics_explorer/reference_corpus_data.js` and
define `window.GBLS_REFERENCE_CORPUS`.

Include summary metadata, sorted known years, journal counts, compact article
records required for filtering and charts, and every controlled feature group
required by the current explorer.

Do not include full abstracts in the browser bundle. Inspect the current
`tools/metrics_explorer/metrics_explorer.js` and match its data contract. Preserve
the gray reference-layer role and blue GBLS foreground role.

Verify in a browser that:

- the reference total is correct;
- gray marks render;
- feature and year filters affect the reference layer;
- the GBLS layer still renders;
- the article table remains GBLS-only unless explicitly labeled otherwise;
  and
- there are no console errors.

## Reproducible Implementation

Use or improve:

`<project root>/2_calculated_metrics/library_journal_reference_metrics/build_reference_metrics.py`

The script must accept the project root or discover it from a supplied folder,
use project-relative paths, print progress and validation results, create all
required outputs, exit nonzero on validation failure, and avoid network access.

Do not manually calculate or edit metric rows. If the existing script only
creates explorer JavaScript, expand it to implement this complete contract.
Retain a backward-compatible invocation accepting explicit manifest and
explorer-output paths if that form already exists.

## Completion Report

Report:

- source and parsed article counts;
- unique journal count;
- feature assignment and unique-label counts;
- missing-year count;
- workbook status;
- explorer refresh and browser-test status;
- exact reference metrics folder; and
- exact explorer bundle path.

Do not stop after writing a plan or script. Run it, validate all outputs, and
save the deliverables.
