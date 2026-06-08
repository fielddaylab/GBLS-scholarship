# Review Every Section for Topical Cohesion

This prompt can run without conversation history. Resolve `PROJECT_ROOT` and
read:

- the live baseline and runtime structure manifest;
- `00_shared_section_contract.md`;
- `2-outputs/TERMINOLOGY_DRAFT.md`;
- all working ledgers;
- the current baseline, corpus, and citation audits.

Do not use an earlier manuscript as an authority. This pass occurs before the
publishability rubric reviews and has one purpose: replace paper-by-paper or
author-centered narration with cohesive, topically driven synthesis.

## Blocking Structural Rule

Before and after editing, independently compare every H1-H6 heading with the
live baseline after removing only trailing drafting annotations. Do not add,
remove, rename, relevel, duplicate, merge, split, or reorder headings.

## Section-By-Section Diagnostic

Review every non-reference H1 block and every substantive H2-H6 subsection.
For each, record in the disposable run-state ledger:

- the section's intended collective message;
- passages that read as lists of authors or individual papers;
- paragraphs lacking a topic-led synthesis claim;
- single-source claims presented as field-level conclusions;
- author-led sentences that are analytically necessary and should remain;
- revisions made to improve topical cohesion.

Flag, but do not mechanically delete, sentences matching patterns such as:

- “Author (year) argues/found/reports/describes...”
- “In a study of..., Author...”
- one source summarized per sentence in publication or discovery order;
- paragraphs whose main nouns are researchers, articles, or studies rather
  than services, outcomes, contexts, tensions, mechanisms, or design choices.

Author-led prose may remain when source identity is necessary to attribute a
distinctive concept, explain a direct disagreement, contrast methods, identify
a historical intervention, or discuss an outlier. State why it remains.

## Cohesion Revision

Revise each flagged passage using this sequence:

1. open with the topical claim, pattern, debate, or uncertainty;
2. group evidence from multiple applicable sources;
3. compare agreement, divergence, context, method, or evidence strength;
4. interpret what the collective evidence means for GBLS;
5. position citations after the claims they support where feasible.

Do not manufacture synthesis by attaching unrelated citations to a broad
sentence. Preserve meaningful differences among studies. When only one source
supports a point, narrow the claim and label it as a local example,
single-study result, practitioner account, or proposition requiring further
evidence.

Also remove redundant article-level detail that does not advance the section's
collective message. Preserve methods or sample details only when they affect
evidentiary weight, explain disagreement, or bound generalization.

## Output And Verification

Save the revised manuscript as `2-outputs/COHESION_DRAFT.md`. Record the
following in the disposable run-state ledger:

- findings for every H1 section;
- representative categories of author-centric prose found;
- revision principles applied;
- any justified author-led sentences retained;
- any sections requiring no change;
- checksums for `TERMINOLOGY_DRAFT.md` and `COHESION_DRAFT.md`.

Synchronize affected ledgers and audits. Verify heading parity, citation
integrity, baseline-prose traceability, and word counts. If no change is
warranted in a section, say so explicitly. If the two drafts are identical,
document why; do not claim that a revision occurred. Do not overwrite the
target-journal simulations ultimately required in `reviewer_notes.md`.
