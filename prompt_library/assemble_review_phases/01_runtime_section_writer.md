# Bounded Runtime Section Writer

Run this prompt in a fresh context. Read
`00_shared_section_contract.md`, then `3_article_outputs/run_state/run_status.md`.

This phase has three job modes. Execute exactly one mode per invocation.

## Mode A: `BUILD_PACKET section_NN`

Read:

- `structure_manifest.md`;
- the section's exact baseline line span;
- `source_index.tsv`;
- the previous section's final paragraph if already drafted;
- the next section's headings from the manifest.

Create `section_packets/section_NN/packet.md`.

Route candidate sources using suggested-contribution text first. Add metadata
matches only when necessary. Rank candidates by relevance and evidence
strength, then divide them into batches of no more than 12 summaries or 45,000
tokens. Write filenames only in the batch manifest.

Do not read full summaries and do not draft prose in this mode.

Update `run_status.md` to the first `READ_EVIDENCE_BATCH` job and stop.

## Mode B: `READ_EVIDENCE_BATCH section_NN batch_MM`

Read:

- the section `packet.md`;
- existing `evidence_notes.md`, if any;
- only the complete coded summaries named in `batch_MM`.

Append compact notes to `evidence_notes.md`. For every source record:

- bibliographic heading and citation form;
- exact destination heading;
- one to three supported claims;
- method, setting, and evidence weight;
- useful comparison, disagreement, null finding, or implementation detail;
- limitation;
- provisional `use`, `consult`, `defer`, or `exclude`.

Use no more than 120 words per source. Preserve discriminating evidence and
remove generic article-summary language. If cumulative notes would exceed the
shared packet ceiling, mark lower-priority candidates `defer`; phase 6 will
reconsider them.

Do not draft the section. Do not reread earlier source batches. Existing
`evidence_notes.md` is the handoff.

Update `run_status.md` to the next evidence batch or `DRAFT_SECTION` and stop.

## Mode C: `DRAFT_SECTION section_NN`

Read only:

- the shared contract;
- the section `packet.md`;
- the completed `evidence_notes.md`;
- `explicit_values.md`;
- the relevant terminology entries from
  `metadata-schema-and-lexicon.md`, not necessarily the whole file.

Write:

- `draft.md`;
- `ledger.md`.

Requirements:

- preserve the exact heading sequence;
- account for every baseline passage;
- begin each substantive heading with field-level framing;
- synthesize by topic rather than source order;
- define specialized terms at first use;
- calibrate claims to evidence type;
- move toward the following section without drafting it;
- meet or explain deviation from the target.

For a reference-role section, use completed section ledgers to build a
deduplicated, alphabetized reference list. Do not reread all summaries.

Verify heading parity, citation resolution, baseline dispositions, word count,
and checksum. Mark the section complete and set the next exact job in
`run_status.md`, then stop.
