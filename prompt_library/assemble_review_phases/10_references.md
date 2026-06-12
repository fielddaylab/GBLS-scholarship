# Build the References Section

Read `00_shared_section_contract.md`, every completed section and in-memory
working ledger retained by the master orchestrator, approved human-source
records, and the complete coded-summary corpus.

## Runtime Structure

Reread `0-human-sources/baseline_structure_and_prose.md` at runtime. Use its final H1
section and any H2 headings nested beneath that H1. Do not rely on headings
from a previous run. The verification heading described below may be added
only when unresolved cited records exist.

## Section Task

Extract every author-year citation used in the completed section texts. Match
each citation to the full bibliographic heading in the coded summaries or an
approved human-source record. Deduplicate and alphabetize the references.
Include only cited works.

Include citations inherited from baseline prose in the same audit. Do not
assume that a citation appearing in the baseline is complete or correct;
verify it against an approved bibliographic record.

Perform a bidirectional audit:

- Every in-text author-year citation must map to exactly one reference or to an
  explicit verification note.
- Every reference entry must be cited in the manuscript.
- Name variants, same-year works, group authors, and multi-author
  abbreviations must resolve consistently.

Do not invent missing titles, authors, dates, journal details, page ranges, or DOIs. For a cited work that cannot be matched confidently, add it under a final `## Bibliographic Records Requiring Verification` heading with the in-text citation and the source artifact where it appears.

Apply consistent APA-style presentation as far as the available metadata
permits. Preserve DOIs and stable URLs supplied by source records. When Zotero
or another approved bibliographic source is available, use it to verify and
normalize records after matching them to the corpus; do not silently replace a
record when identity is uncertain.

Write the completed references section back to the master orchestrator for
assembly. Write the citation-audit results to
`2-outputs/audits_and_synthetic_reviews/citation_audit.md`, including counts of
in-text citations, matched references, uncited references removed, and
unresolved records. Do not create a standalone references artifact or ledger.
