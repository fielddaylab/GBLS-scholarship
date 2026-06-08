# Review Heading Framing and Section Introductions

This prompt can run without conversation history. Resolve `PROJECT_ROOT` and
read the live baseline, runtime manifest, shared contract, `SECOND_DRAFT.md`,
working ledgers, and current audits.

Its purpose is to ensure that the reader understands each heading before
encountering evidence, cases, or source-specific detail.

## Blocking Structural Rule

Before and after editing, compare every H1-H6 heading with the live baseline
after removing only trailing drafting annotations. Do not add, remove, rename,
relevel, duplicate, merge, split, or reorder headings.

## Heading Diagnostic

Review every narrative H1-H6 heading except `# Abstract` and `# References`.
Inspect the first paragraph beneath each heading and ask:

1. Does it explain what the heading means in this review?
2. Does it identify the collective question, argument, or service problem?
3. Does it preview the topics, distinctions, evidence categories, or tensions
   developed in the following paragraphs?
4. Does it begin with field-level framing rather than a named author, article,
   local program, or citation?
5. Does it avoid merely repeating the heading or announcing “This section
   discusses...”?

## Revision Rules

Where framing is absent or incomplete, write or revise a concise opening
paragraph. Use substantive prose that introduces the conceptual scope and
organizing logic. A good opening should tell readers why the topic matters and
how the following evidence is organized without listing every source.

For headings that contain only one paragraph, integrate the framing into that
paragraph rather than adding redundant prose. Do not manufacture claims that
the evidence cannot support. Preserve citations when needed, but do not begin
the framing paragraph with an author citation.

Record each heading's status and revision in the disposable run-state ledger.

## Output And Verification

Save the revised manuscript as `2-outputs/FRAMED_DRAFT.md`. Verify:

- every narrative heading has an adequate orienting opening;
- heading parity remains exact;
- framing does not introduce unsupported claims;
- citations and references remain synchronized;
- word counts and target deviations are recalculated.

Compare checksums for `SECOND_DRAFT.md` and `FRAMED_DRAFT.md`. If a heading
requires no change, record that explicitly. Do not write internal process notes
into the final target-journal `reviewer_notes.md`.
