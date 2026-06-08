# Master Prompt: Build the Complete GBLS Literature Review

This prompt transforms the current baseline structure and coded-summary corpus
into a reviewed manuscript. The baseline determines the manuscript structure
at runtime; no section inventory is encoded in the prompt library.

## Project Configuration

- Project root: `/Users/djgagnon/Library/CloudStorage/GoogleDrive-djgagnon@wisc.edu/.shortcut-targets-by-id/1P-yeNAX497qAu3txZnKjZZ1ztx8V2nSJ/Phase I - Research, Needs Assessment, and Lit Review Resources/GBLS Lit Review Working Docs`
- Baseline: `0-human-sources/baseline_structure_and_prose.md`
- Coded summaries: `1-coded-summaries/*.md`, excluding `template.md`
- Runtime section writer: `prompt-library/section-prompts/01_runtime_section_writer.md`
- Assembly prompt: `prompt-library/section-prompts/02_assemble_and_transition.md`
- Review prompt: `prompt-library/section-prompts/03_review_and_revision.md`
- Output directory: `2-outputs`
- Audit directory: `2-outputs/audits_and_synthetic_reviews`

`2-outputs` is the canonical location for manuscript drafts. Audits and
synthetic reviews belong only in `2-outputs/audits_and_synthetic_reviews`.
Do not create section or section-ledger directories.

## Objective

Produce a cohesive, publishable literature review by developing the
author-supplied baseline prose through synthesis with the coded-summary
corpus. The number, names, sequence, hierarchy, prose, and word targets of
manuscript sections must come from the baseline as it exists when the run
begins.

## Runtime Structure Discovery

At the beginning of the run, read the baseline directly from disk and parse it
into an ordered section manifest.

For every H1:

1. Assign a stable runtime identifier based on its ordinal position, such as
   `section_01`, without using the title as a filename or prompt name.
2. Capture the complete H1 line.
3. Derive the manuscript H1 by removing only trailing parenthetical drafting
   annotations.
4. Capture every consecutive H2 and its order until the next H1.
5. Capture all non-heading prose and associate each passage with the nearest
   preceding H1 or H2.
6. Parse any word target or drafting directive contained in the H1 or H2
   annotations.
7. Classify the section's runtime role from its content and annotations:
   narrative section, front matter, or bibliography/reference section.
8. Record its exact ordinal position in the baseline.

Do not use a section list, title list, topic list, expected count, or expected
order from any prompt or previous run. If the baseline gains, loses, renames,
or reorders an H1 or H2, the runtime manifest must change with it.

Write the parsed manifest to
`2-outputs/audits_and_synthetic_reviews/runtime_structure_manifest.md`.
This manifest is an audit artifact, not a source of authority; reread the
baseline before each section task.

## Execution Rules

1. Treat files in `0-human-sources` and `1-coded-summaries` as authoritative
   inputs.
2. Treat the baseline as both the structural authority and author-supplied
   starting draft.
3. Read `00_shared_section_contract.md` before every section task.
4. Use only `01_runtime_section_writer.md` for section generation. Supply it
   with the current runtime section identifier and freshly extracted section
   block.
5. Execute one fresh writing task for each narrative or front-matter section.
6. Defer any bibliography/reference section until all sections containing
   citations have been drafted. Build it using the reference mode in the same
   runtime writer.
7. Keep completed section text and working ledgers in the master context. Do
   not write standalone section or ledger files.
8. Never invent evidence, procedures, citations, or bibliographic data.
9. Do not alter human sources or coded summaries.
10. Treat rubric scores as internal editorial diagnostics, not external peer
    review or publication decisions.

## Preflight

Confirm that these inputs exist:

- `0-human-sources/baseline_structure_and_prose.md`
- `0-human-sources/metadata-schema-and-lexicon.md`
- `0-human-sources/explicit_values.md`
- `0-human-sources/publishability_rubric.md`
- the coded-summary corpus
- all four runtime prompt files

Create or empty `2-outputs/audits_and_synthetic_reviews`. Remove prior
generated drafts from `2-outputs`. Remove obsolete `2-outputs/sections` and
`2-outputs/section-ledgers` directories if present.

## Runtime Section Loop

Iterate through the runtime manifest rather than a prompt-defined section
sequence.

For each non-reference section:

1. Reread the baseline and re-extract that section by its ordinal position.
2. Execute `01_runtime_section_writer.md` in narrative mode.
3. Verify the H1 and H2 sequence against the freshly extracted block.
4. Verify baseline-prose traceability, evidence calibration, word target, and
   working-ledger completeness.
5. Retain the completed text and ledger in the master context.

After all citation-bearing sections are complete, execute the runtime writer
in reference mode for every section classified as bibliography/reference
material.

If no bibliography/reference section exists, do not invent one. Record that
fact in the citation audit. If more than one exists, process each in baseline
order.

## Audits

Create these files in `2-outputs/audits_and_synthetic_reviews`:

- `runtime_structure_manifest.md`
- `baseline_prose_audit.md`
- `corpus_coverage_audit.md`
- `citation_audit.md`
- `reviewer_notes.md`

The baseline prose audit must account for every substantive passage. The
corpus audit must account for every coded summary. The citation audit must
check citations and references in both directions and list unresolved records.

## Assembly and Review

1. Execute `02_assemble_and_transition.md`. Assemble all completed runtime
   sections strictly by their current baseline ordinal positions. Save
   `FIRST_DRAFT.md` and `SECOND_DRAFT.md`.
2. Execute `03_review_and_revision.md`. Save `THIRD_DRAFT.md`,
   `FINAL_DRAFT.md`, and the synthetic reviews in
   `audits_and_synthetic_reviews/reviewer_notes.md`.

## Final Verification

Before finishing:

- Reread the baseline and rebuild the runtime manifest independently.
- Compare every H1 and H2 in `FINAL_DRAFT.md` with the fresh manifest after
  removing only trailing parenthetical drafting annotations.
- Fail verification for any missing, added, renamed, duplicated, or reordered
  heading.
- Confirm that each word target derived from the baseline was evaluated.
- Confirm that all baseline prose, coded summaries, citations, references, and
  unresolved records are represented in the appropriate audits.
- Confirm that no topic-specific section prompt was used.
- Confirm that `2-outputs/sections` and `2-outputs/section-ledgers` do not
  exist.
- Report all output files and manuscript word counts.

The task is complete only when the manuscript, audits, and two synthetic
review rounds have been generated and verified against the current baseline.

Before you start, ask for approval to clear all the contents of the OUTPUTS folder, then start with a clean slate. 
