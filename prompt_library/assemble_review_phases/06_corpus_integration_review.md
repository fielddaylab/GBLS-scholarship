# Bounded Underused-Corpus Integration

Run in fresh contexts. Read the shared contract and `run_status.md`.

This phase is deliberately batchable. Execute exactly one job per invocation.

## Job A: `BUILD_UNDERUSED_INDEX`

Read:

- `stage_5_topical_cohesion_draft.md`;
- `source_index.tsv`;
- current corpus and citation audits;
- phase-5 evidence needs.

Do not read full summaries.

Create `run_state/underused_index.tsv` containing every uncited summary,
provisional destination heading, priority, and batch number. Prioritize
relevant-but-uncited sources. Reconsider excluded sources only when their
index record indicates a plausible, bounded contribution.

Batch at no more than 12 summaries or 45,000 tokens. Set the first
`READ_UNDERUSED_BATCH` job and stop.

## Job B: `READ_UNDERUSED_BATCH batch_MM`

Read:

- only the summaries named in the batch;
- `underused_index.tsv`;
- the matching H1 blocks from stage 5, not necessarily the whole manuscript;
- existing `underused_notes.md`.

Append one compact decision per source:

- `integrate` or `remain_uncited`;
- destination heading and existing claim;
- exact contribution;
- evidence type and limitation;
- minimum prose or citation change;
- precise exclusion reason if unused.

Do not edit the manuscript. Set the next batch or `APPLY_INTEGRATION` and stop.

## Job C: `APPLY_INTEGRATION`

Read:

- `stage_5_topical_cohesion_draft.md`;
- completed `underused_notes.md`;
- exact bibliographic headings for sources marked `integrate`.

Do not reread summaries.

Integrate sources into existing topic-led paragraphs. Prefer a citation plus
the minimum comparison or qualification needed. Do not add one sentence per
source or weaken paragraph coherence to improve a count.

Rebuild References from exact coded bibliographic headings. Save
`stage_6_corpus_integration_draft.md`. Update corpus and citation audits,
record before/after coverage and word counts in `phase_ledgers/phase_06.md`,
verify headings and bidirectional references, advance to phase 7, and stop.
