# Prompt: Rebuild All Coded-Summary Metrics

Work autonomously and complete this task end to end. Do not ask for background context unless a required
folder is genuinely missing.

## Objective

Parse every coded article summary in `1-coded-summaries`, calculate reproducible article-level and
aggregate metrics, and write every generated metric artifact to `2-outputs/metrics`.

The resulting files must be directly usable with Python pandas in Google Colab and must refresh the
existing JavaScript metrics explorer when it is present.

## Project Location

The project root is:

`/Users/djgagnon/Library/CloudStorage/GoogleDrive-djgagnon@wisc.edu/.shortcut-targets-by-id/1P-yeNAX497qAu3txZnKjZZ1ztx8V2nSJ/Phase I - Research, Needs Assessment, and Lit Review Resources/GBLS Lit Review Working Docs`

Use these folders:

- Input: `<project root>/1-coded-summaries`
- Output root: `<project root>/2-outputs`
- Metrics output: `<project root>/2-outputs/metrics`
- JavaScript explorer folder: `<project root>/metrics-explorer`
- JavaScript explorer files: `<project root>/metrics-explorer/index.html`,
  `<project root>/metrics-explorer/metrics-explorer.css`, and
  `<project root>/metrics-explorer/metrics-explorer.js`

If the absolute path is unavailable, locate the project root by finding a directory containing both
`1-coded-summaries` and `2-outputs`. Create `2-outputs/metrics` if it does not exist. Do not search
outside likely workspace or mounted-drive locations
unless necessary.

## Input Rules

1. Read every `.md` file directly inside `1-coded-summaries`.
2. Exclude `template.md`, `.DS_Store`, hidden files, and non-Markdown files.
3. Treat each remaining Markdown file as one source article.
4. Preserve source-coded labels exactly. Do not silently merge, rename, stem, or infer labels.
5. Deduplicate repeated labels within the same article while preserving their original order.
6. Derive `article_id` from `Zotero_Item_Key`; if missing, use the eight-character key in the filename;
   if neither exists, use the filename stem.
7. Keep genuinely undated sources as missing year and label them `n.d.` in publication-year summaries.
   Do not invent publication years.
8. Counts represent coded article presence. A source contributes no more than one count to a particular
   feature label, regardless of how often that concept appears in prose.

## Fields to Parse

Parse these scalar metadata fields when present:

- `Citation_Key`
- `Year`
- `Zotero_Item_Key`
- `Better_BibTeX_Citation_Key`
- `Attachment_Key`
- `Coding_Confidence`

Parse these as multi-label fields, accepting either a single inline value or a Markdown bullet list:

- `Source_Type`
- `Evidence_Type`
- `Methodology`
- `Library_Context`
- `Game_Format`
- `Service_Area`
- `Audience`
- `Outcome`
- `Theme`
- `Contribution_Type`
- `Design_Principles`

Also extract:

- Full citation shown before the `Metadata` heading
- Full text following the `Summary` heading
- Proposed contribution entries, including contribution number, target section, and contribution text
- Source filename and absolute source path

Handle heading variations such as `# Metadata`, `### Metadata`, `# Summary`, and `### Summary`.
Accept contribution headings such as `Contributions`, `Potential Contributions`, and
`Suggested Review Contributions`.

## Article-Level Derived Features

For each article calculate:

- `article_id`
- `filename`
- `citation`
- `year`
- `year_status`: `known` or `not_dated`
- `decade`
- Citation and Zotero identifiers
- `coding_confidence`
- `summary_word_count`
- `summary_character_count`
- `contribution_count`
- `target_sections`, pipe-delimited
- `source_path`
- `summary_text`
- One pipe-delimited column for every multi-label field
- A `<field>_count` column for every multi-label field

Use lowercase snake_case column names. Store multi-label values in readable article tables with `|`
as the delimiter.

## Required Output Files

Write all files in this section to `<project root>/2-outputs/metrics`. Write UTF-8 CSV files with
headers and no dataframe index:

### Article tables

1. `articles.csv`
   - One row per article
   - Includes all parsed and derived article fields, including full summary text

2. `articles_core.csv`
   - Same article-level data without `summary_text`

3. `article_features_long.csv`
   - One row per article-feature assignment
   - Columns: `article_id`, `year`, `feature_group`, `feature_value`, `feature_column`, `present`
   - `present` must always equal `1`
   - Include `coding_confidence` as a feature group

4. `article_feature_matrix.csv`
   - One row per article
   - Identity columns first: `article_id`, `year`, `decade`, `citation`, `coding_confidence`,
     `summary_word_count`
   - One integer binary column per unique coded feature using
     `<feature_group>__<snake_case_feature_value>`

5. `article_topic_matrix.csv`
   - Identity columns plus only `service_area__*` binary columns

6. `article_theme_matrix.csv`
   - Identity columns plus only `theme__*` binary columns

7. `contributions.csv`
   - One row per extracted proposed contribution
   - Columns: `article_id`, `contribution_number`, `target_section`, `contribution_text`

### Aggregate tables

8. `feature_counts.csv`
   - One row per unique feature label
   - Columns: `feature_group`, `feature_value`, `article_count`, `total_articles`, `article_pct`,
     `rank_within_group`
   - `article_pct = article_count / total_articles * 100`
   - Use dense descending rank within each feature group

9. `topic_area_counts.csv`
   - The `service_area` rows from `feature_counts.csv`

10. `theme_counts.csv`
    - The `theme` rows from `feature_counts.csv`

11. `publication_year_counts.csv`
    - One row per publication year plus `n.d.`
    - Columns: `year_label`, `article_count`, `article_pct`

12. `feature_year_counts.csv`
    - One row per year-feature combination that occurs
    - Columns: `year`, `feature_group`, `feature_value`, `article_count`, `total_articles`,
      `article_pct_in_year`
    - Use the number of articles published in that year as the denominator

13. `feature_cooccurrence.csv`
    - One row per unordered pair of distinct coded features assigned to the same article
    - Columns: `feature_group_a`, `feature_value_a`, `feature_group_b`, `feature_value_b`,
      `article_count`, `article_pct`
    - Include pairs occurring in at least two articles
    - Sort primarily by descending `article_count`

14. `dataset_summary.csv`
    - One row per metric with columns `metric`, `value`
    - Include at least:
      - `total_articles`
      - `earliest_year`
      - `latest_year`
      - `unique_feature_labels`
      - `total_article_feature_assignments`
      - `mean_features_per_article`
      - `median_summary_word_count`
      - `articles_with_contributions`

15. `data_dictionary.csv`
    - Document every generated data file, its grain, purpose, and primary key

## Documentation and Validation

Create or replace these metric-specific support files inside `2-outputs/metrics`:

16. `FEATURE_DATASETS_README.md`
    - Explain the tables and recommend:

      ```python
      import pandas as pd

      metrics_dir = "2-outputs/metrics"
      articles = pd.read_csv(f"{metrics_dir}/articles_core.csv")
      features = pd.read_csv(f"{metrics_dir}/article_features_long.csv")
      matrix = pd.read_csv(f"{metrics_dir}/article_feature_matrix.csv")
      ```

    - State that counts represent coded article presence, not prose term frequency
    - Explain denominators used by percentage columns
    - Note any undated records

17. `validation_report.json`
    - Include:
      - Source Markdown count excluding the template
      - Parsed article count
      - Unique article ID count
      - Duplicate article ID count
      - Missing-year count
      - Article-feature assignment count
      - Sum of `feature_counts.article_count`
      - Matrix row count and binary feature-column count
      - List of parse warnings or failures

Validation must confirm:

- Every non-template Markdown file produced exactly one article row
- `article_id` is unique and nonblank
- `article_features_long.present` contains only `1`
- The number of matrix rows equals the article count
- The sum of `feature_counts.article_count` equals the number of long-table feature assignments
- Topic and theme count files exactly match their corresponding `feature_counts` subsets
- All generated CSV files can be loaded by pandas

Stop and report a clear error if any source cannot be parsed. Do not silently omit files.

## Overview Workbook

Create or replace `2-outputs/metrics/gbls_feature_overview.xlsx` with clean, machine-readable sheets:

- Dashboard
- Topic Areas
- Themes
- Year Counts
- All Feature Counts
- Data Dictionary

The Dashboard must show headline corpus metrics and charts for the top topic areas and themes. Use
plain headers, frozen header rows, filters or Excel tables where useful, and avoid merged multi-row
table headers.

## Refresh the JavaScript Explorer

If `<project root>/metrics-explorer/index.html` and
`<project root>/metrics-explorer/metrics-explorer.js` exist:

1. Regenerate `2-outputs/metrics/metrics-explorer-synthesized-data.js` from the newly calculated files.
2. Define the data as `window.GBLS_METRICS`.
3. Include:
   - Dataset summary
   - Sorted known publication years
   - Article records needed by the explorer
   - Feature counts
   - Publication-year counts
   - Feature-year counts
4. Keep the existing HTML, CSS, and interaction logic unless a schema change requires a narrowly scoped
   compatibility fix.
5. Verify that `metrics-explorer/index.html` loads with no console errors and shows the newly
   calculated total article count.

The explorer HTML, CSS, application script, and README are siblings in the project-root
`metrics-explorer` folder. The generated data bundle is under `2-outputs/metrics`. Keep these
references in `metrics-explorer/index.html` valid:

- `metrics-explorer.css`
- `metrics-explorer.js`
- `../2-outputs/metrics/metrics-explorer-synthesized-data.js`

## Implementation Requirements

- Use a reproducible script rather than manually editing CSV files.
- Prefer Python with pandas for parsing and tabular calculations.
- Use a Markdown-aware or line-structured parser; do not calculate metrics by loosely counting words in
  summaries.
- If optional Parquet libraries are already available, Parquet copies may also be created, but they are
  not required. Do not install dependencies solely for Parquet.
- Write generated metric artifacts only inside `2-outputs/metrics`.
- Do not overwrite unrelated files in `2-outputs`, including literature-review drafts, audit notes,
  section folders, or the generic `README.md`.
- Keep the explorer HTML, CSS, application script, and README inside the project-root
  `metrics-explorer` folder. Do not move them into `2-outputs/metrics`; only the generated
  `metrics-explorer-synthesized-data.js` bundle belongs there.
- Do not alter source summaries.
- Use temporary or workspace files for scripts and previews; put only final metric deliverables in
  `2-outputs/metrics`.

## Completion Report

After implementation and verification, report:

- Number of source summaries parsed
- Number of unique articles
- Number of feature assignments
- Number of unique coded labels
- Number of undated sources
- Whether the workbook was created
- Whether the JavaScript explorer was refreshed and tested
- Exact metrics output folder (`2-outputs/metrics`)

Do not stop after proposing a schema. Build, validate, and save all deliverables.
