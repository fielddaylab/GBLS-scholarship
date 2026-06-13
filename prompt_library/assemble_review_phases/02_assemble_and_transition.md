# Bounded Assembly and Integration

Run in a fresh context after every section packet is complete. Read the shared
contract and `run_status.md`.

This phase has two jobs. Execute one per invocation.

## Job 1: `ASSEMBLE_STAGE_1`

Read:

- `structure_manifest.md`;
- every completed `section_packets/section_NN/draft.md`;
- heading fingerprints and checksums from section ledgers.

Do not read coded summaries or full ledgers.

Validate that every baseline H1 block has exactly one matching section draft.
Assemble them in manifest order. Remove only accidental duplicate boundary
text. Save `stage_1_initial_assembly_draft.md`.

Write a compact stage-1 entry to `phase_ledgers/phase_02.md`, verify heading
parity, and set `INTEGRATE_STAGE_2` as the next job.

## Job 2: `INTEGRATE_STAGE_2`

Read:

- `stage_1_initial_assembly_draft.md`;
- `structure_manifest.md`;
- compact unresolved-issue lists from section ledgers;
- `explicit_values.md`.

Do not read the coded corpus.

Revise the manuscript as one argument:

- improve transitions and cumulative logic;
- remove repetition;
- harmonize terminology, evidence language, citations, and voice;
- retain meaningful context differences, null findings, and limitations;
- keep paragraphs topic-led;
- preserve exact headings.

Save `stage_2_whole_manuscript_integration_draft.md`. Record material changes,
word counts, checksums, and unresolved issues. Update `run_status.md` to phase
3 and stop.
