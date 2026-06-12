# Runtime Section Writer

This prompt can be invoked in a fresh task with no conversation history. Read
`00_shared_section_contract.md`, resolve `PROJECT_ROOT`, validate the complete
runtime packet, and reread the identified H1 block from the live baseline.

Do not read existing files in `3_article_outputs` as source material.

## Narrative Or Front-Matter Mode

When `RUNTIME_SECTION_ROLE` is `narrative` or `front matter`:

1. Validate the supplied block against its ordinal position and source lines.
2. Extract its H1, every nested H2-H6, annotations, and prose passages.
3. Infer its intellectual purpose from the live block and neighboring heading
   metadata, not from its position alone.
4. Search the complete eligible coded-summary corpus for relevant evidence,
   counterevidence, null findings, context differences, and evidence limits.
5. Cluster relevant findings by claim, pattern, tension, outcome, context, or
   design principle before drafting. Do not draft in source-discovery order.
6. Develop baseline prose into thematic, cross-source synthesis whose
   paragraph subjects are topics rather than authors or articles.
7. Preserve exact heading wording, level, and order after removing only
   trailing drafting annotations.
8. Begin every substantive narrative heading with an orienting paragraph that
   defines its scope and previews the topics and distinctions that follow.
9. Introduce specialized terms, organizations, frameworks, and acronyms at
   first use before relying on them.
10. Give practical GBLS implications where appropriate to the section's role.
11. Create narrative movement toward the next section without prewriting it.
12. Meet or explicitly account for the runtime word target.
13. Run the author-centric prose check below, revise, and return the completed
   section and structured working ledger.

The opening paragraph should frame the section's collective question and
principal patterns. Paragraphs should be organized around ideas, not papers.
Where the evidence base is mainly descriptive, say so.

## Author-Centric Prose Check

For every paragraph:

1. identify its topic sentence and collective message;
2. flag sentences that begin with an author name, study name, or citation;
3. flag sequences that summarize one source per sentence;
4. flag paragraphs supported by only one source but written as general claims;
5. rewrite flagged prose around a topical claim, grouped evidence,
   comparison, and interpretation.

Retain author-led sentences only for a necessary attribution, direct
disagreement, methodological contrast, distinctive concept, historical
intervention, or outlier. The final paragraph should remain coherent if
author names are removed and only the substantive claims remain.

## Reference Mode

When `RUNTIME_SECTION_ROLE` is `reference`:

1. Read every completed citation-bearing section and ledger from active context
   or the disposable run-state directory.
2. Extract every in-text citation, including citations inherited from baseline
   prose.
3. Match each citation to coded-summary bibliographic headings or explicitly
   approved records.
4. Resolve same-author/same-year suffixes consistently.
5. Deduplicate and alphabetize matched entries.
6. Include only works cited in the manuscript.
7. Preserve the runtime H1 and all baseline-defined nested headings.
8. If unmatched citations remain, place them in a verification subsection only
   when that exact subsection already exists in the baseline. Otherwise list
   them only in `citation_audit.md`; never add a manuscript heading.
9. Check references back against the manuscript and remove uncited entries.
10. Return the completed reference section and update data for the citation
    audit.

Never invent bibliographic data. Account for prose found in a reference-role
block under the baseline-prose rules.

## Completion Check

Before returning:

- compare the complete H1-H6 sequence with the live block;
- verify every baseline passage has a ledger disposition;
- verify every citation has a source match or unresolved status;
- calculate actual section word count and target deviation;
- confirm no output section or ledger directory was created;
- return a clear success or blocking-error status.
