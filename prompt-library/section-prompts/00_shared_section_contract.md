# Shared Contract for Runtime GBLS Section Writing

Use this contract for every section discovered from
`0-human-sources/baseline_structure_and_prose.md`.

## Authority

The baseline is the sole authority for:

- the number of sections;
- H1 and H2 titles;
- section and subsection order;
- word targets and drafting annotations;
- author-supplied starting prose.

Do not infer structure from prompt filenames, earlier drafts, remembered
headings, or topic expectations.

## Runtime Section Input

Each section task must receive:

- `RUNTIME_SECTION_ID`: its ordinal identifier;
- `RUNTIME_SECTION_POSITION`: its current H1 position;
- `RUNTIME_SECTION_ROLE`: narrative, front matter, or reference;
- `RUNTIME_SECTION_BLOCK`: the complete freshly extracted baseline block;
- `PRECEDING_SECTION_CONTEXT`: completed neighboring text when available;
- `FOLLOWING_SECTION_METADATA`: the next section's H1 and directives, without
  prewriting its prose.

If these values were not freshly derived from the baseline, stop and rebuild
them before writing.

## Heading Handling

Copy the runtime H1 and every nested H2 in exact order. Remove only trailing
parenthetical annotations used for word counts or drafting directions. Do not
add, omit, rename, merge, split, or reorder headings.

Text before the first H1 is workflow material unless explicitly labeled as
manuscript prose.

## Baseline Prose

Treat non-heading text in the runtime block as author-supplied starting prose.
Associate each passage with the nearest preceding heading. Use it as the
conceptual and rhetorical starting point, not immutable text.

You may edit, synthesize, reorganize within the section, qualify, or expand
baseline prose. Preserve every substantive idea unless it is duplicative,
obsolete instruction, contradicted by stronger evidence, or outside scope.
Record every retention, revision, relocation, or omission in the working
ledger.

Baseline prose is not evidence by itself. Search the coded summaries for
applicable support, qualification, disagreement, and limits. Label unsupported
authorial propositions as interpretations, recommendations, or proposed
frameworks rather than established findings.

## Evidence and Synthesis

Give greatest weight to empirical studies, systematic reviews, surveys,
interviews, observations, mixed methods, and experiments. Use case studies for
implementation knowledge and practitioner sources cautiously. Use historical
sources for precedent, not contemporary outcome evidence.

Organize prose around field-level themes, patterns, tensions, comparisons,
outcomes, or design principles. Do not write one paragraph per source. Begin
each substantive H1 and H2 with a synthesis claim rather than an author
citation. Distinguish engagement from learning, transfer, belonging, equity,
well-being, and other outcomes. Include credible null findings and outliers.

Use `explicit_values.md` as an interpretive orientation, not as evidence.

## Working Ledger

Maintain an in-memory ledger for the runtime section. Record:

- baseline passages and their disposition;
- summaries cited;
- summaries substantively consulted but not cited;
- excluded summaries and reasons;
- every author-year citation and matched bibliographic heading;
- unresolved bibliographic records;
- evidence limitations and notable outliers.

Return the completed section text and ledger to the master orchestrator. Do
not write standalone section or ledger files.

## Style and Length

Write concise, comparative, scholarly prose accessible to library
professionals. Use the runtime word target when one exists. When no target
exists, use the space necessary for adequate synthesis without padding.
Drafting annotations guide the task but do not appear in manuscript headings.
