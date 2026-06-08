# Runtime Section Writer

Read `00_shared_section_contract.md` and the runtime values supplied by the
master orchestrator. Reread the corresponding H1 block from
`0-human-sources/baseline_structure_and_prose.md` before writing.

## Narrative And Front-Matter Mode

When `RUNTIME_SECTION_ROLE` is `narrative` or `front matter`:

1. Extract the current H1, nested H2s, annotations, and baseline prose.
2. Identify the section's intellectual purpose from its headings, prose,
   position, and relation to neighboring sections.
3. Search the complete coded-summary corpus for relevant evidence rather than
   relying only on metadata suggestions or previous draft prose.
4. Develop the baseline prose into thematic synthesis using the evidence and
   limitations in the shared contract.
5. Preserve exact runtime heading order and satisfy the runtime word target.
6. End with implications or narrative movement appropriate to the section's
   actual role. Do not force a transition when the section is genuinely front
   matter.
7. Return the completed section and its in-memory working ledger.

Do not use topic instructions from an earlier prompt or assume what this
section should contain from its ordinal position alone.

## Reference Mode

When `RUNTIME_SECTION_ROLE` is `reference`:

1. Read every completed citation-bearing runtime section and working ledger.
2. Extract all author-year citations, including citations inherited from
   baseline prose.
3. Match citations to coded-summary headings or approved bibliographic
   records.
4. Deduplicate and alphabetize entries.
5. Include only cited works.
6. Add a verification subsection only when cited records cannot be matched
   confidently.
7. Preserve the runtime H1 and any baseline-defined H2s.
8. Return the completed reference section to the master orchestrator.
9. Write the bidirectional results to
   `2-outputs/audits_and_synthetic_reviews/citation_audit.md`.

Do not invent missing bibliographic data. If the baseline contains prose in a
reference-role section, preserve or account for it under the baseline-prose
rules.

## Completion Check

Before returning:

- reread the runtime block;
- compare all H1/H2 headings exactly;
- check baseline-prose traceability;
- check citations against the working ledger;
- check the runtime word target or reference directive;
- confirm that no standalone section or ledger file was created.
