# Prompt: Rebuild All GBLS and Reference-Corpus Metrics

Work autonomously from the folder the user provides. Do not ask for ordinary
project context that can be discovered from the filesystem.

## Goal

Rebuild and validate both datasets used by the GBLS Metrics Explorer:

1. The curated GBLS corpus in `1_coded_gbls_corpus_articles`
2. The broad abstract-coded journal reference corpus in
   `1_coded_reference_corpus_articles`

Then verify that the Metrics Explorer displays the GBLS corpus as the primary
blue layer and the journal reference corpus as the gray comparison layer.

## Locate the Project

The supplied folder may be the project root or any folder inside it. Locate
the nearest project root containing:

- `0_human_sources`
- `1_coded_gbls_corpus_articles`
- `1_coded_reference_corpus_articles`
- `2_calculated_metrics`
- `prompt_library`
- `tools/metrics_explorer`

Do not rely on remembered absolute paths.

## Execute the Canonical Prompts

Read and follow these prompts from the discovered project:

1. `prompt_library/calculate_summary_metrics.md`
2. `prompt_library/rebuild_reference_corpus_metrics.md`

Treat each as a required build contract. Complete the curated GBLS build
first, then the reference build, because the final browser test requires both
generated bundles.

If either prompt is missing, stop and report the missing path. Do not invent a
different output layout.

## Shared Rules

- Discover the live metadata schema inside `0_human_sources`.
- Preserve controlled values exactly as coded.
- Do not mix reference rows into curated GBLS CSVs.
- Do not mix curated GBLS rows into reference CSVs.
- Keep reference metrics under `2_calculated_metrics/library_journal_reference_metrics`.
- Keep curated metrics directly under `2_calculated_metrics/gbls_corpus_metrics`.
- Refresh both JavaScript data bundles:
  - `2_calculated_metrics/metrics_explorer_synthesized_data.js`
  - `tools/metrics_explorer/reference_corpus_data.js`
- Do not alter coded source Markdown.
- Use reproducible scripts and validation, never manual row editing.

## Cross-Corpus Verification

After both builds succeed:

1. Load both article-level core tables.
2. Confirm row counts equal totals in their validation reports and JavaScript
   bundles.
3. Confirm both datasets use the same live controlled feature groups.
4. Report valid labels occurring in only one corpus as informational.
5. Confirm charts compare within-corpus prevalence, not raw corpus totals.
6. Confirm the reference corpus is identified as abstract-coded and
   non-GBLS-focused.

## Browser Verification

Serve the project locally and test `tools/metrics_explorer/index.html`.

Verify:

- both corpus totals appear;
- GBLS renders in blue;
- the reference corpus renders in gray;
- feature-family and year filters update both layers;
- raw counts remain available in labels or tooltips;
- percentage scaling prevents the larger corpus from visually erasing GBLS;
- the article explorer remains clearly scoped to GBLS articles; and
- no browser console errors occur.

Stop the temporary server after testing.

## Completion Report

Report:

- curated GBLS article count;
- reference article count;
- controlled feature-group count;
- unique labels in each corpus;
- validation and workbook status for each corpus;
- browser verification status;
- curated metrics path; and
- reference metrics path.

Do not merely describe what should happen. Execute both builds, validate the
artifacts, and verify the combined explorer.
