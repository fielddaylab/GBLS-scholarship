# Bounded Publishability, Factual Audit, and Final Review

Run in fresh contexts. Read the shared contract and `run_status.md`.

Execute exactly one job per invocation.

## Job 1: `PUBLISHABILITY_ROUND_1`

Read:

- `stage_6_corpus_integration_draft.md`;
- `publishability_rubric.md`;
- `structure_manifest.md`;
- compact unresolved issues from phase ledgers;
- corpus and citation audit summaries, not all source rows.

Revise for contribution, synthesis, evidence calibration, context comparison,
equity, practice implications, research agenda, organization, concision, and
target fit. Save `stage_7_first_publishability_review_draft.md`.

Write a compact revision ledger and a machine-readable list of citation-bearing
claims to `claim_packets/claim_index.tsv`. Divide claims into batches of at
most 8. Set the first factual-audit batch and stop.

## Job 2: `FACT_CHECK_BATCH batch_MM`

Read only:

- the claims named in the batch;
- their resolved coded-summary records;
- matching `.txt` files from `0_human_sources/source_texts/`;
- existing results for this batch if retrying.

Do not read the entire manuscript or source-text corpus.

For each claim, record:

- claim ID, heading, full claim, and citations;
- source filename and stable locator;
- short exact quotation;
- `verified`, `verified_with_scope_change`, `partially_verified`,
  `contradicted`, `source_text_missing`, `not_located`, or `not_applicable`;
- recommended disposition.

Write `claim_packets/batch_MM_results.md`. Set the next batch or
`COMBINE_FACT_AUDIT` and stop.

## Job 3: `COMBINE_FACT_AUDIT`

Read only `claim_index.tsv` and all completed batch result files. Confirm every
claim appears exactly once. Combine them into
`audits_and_synthetic_reviews/factual_reliability_audit.md`, with status counts,
missing texts, flagged claims, unresolved risks, and non-destructive
confirmation.

Set `PUBLISHABILITY_ROUND_2` and stop.

## Job 4: `PUBLISHABILITY_ROUND_2`

Read:

- `stage_7_first_publishability_review_draft.md`;
- the factual audit;
- `publishability_rubric.md`;
- `structure_manifest.md`;
- citation and corpus audit summaries.

Adjudicate every factual flag semantically. Revise only where evidence
warrants correction, qualification, citation change, or removal. Also inspect
residual source-led prose, repetition, equity gaps, target overruns, and
citation problems.

Save `stage_8_final_independent_review_draft.md`. Record a disposition for
every factual flag. Set `WRITE_REVIEWER_NOTES` and stop.

## Job 5: `WRITE_REVIEWER_NOTES`

Read:

- `stage_8_final_independent_review_draft.md`;
- `publishability_rubric.md`;
- final word-count and audit summaries.

Do not read coded summaries or source texts.

Write one simulated report per venue with hard-constraint fit and exact delta,
1-5 score, likely recommendation, reviewer summary, strengths, major concerns,
required corrections, and bottom-line fit. Add a comparative table and ranked
submission assessment. Save `reviewer_notes.md`.

Set `FINAL_VERIFY` in `run_status.md` and stop.
