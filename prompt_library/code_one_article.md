# Prompt: Code One GBLS Article (Stage 1 — Subjective Pass)

MODEL TIER: small / local model is usually sufficient. Fixed-lexicon labeling
does not need a flagship model when the prompt is well structured. The Stage 2
audit handles the uncertain cases.

You are a metadata coder for the Games-Based Library Services (GBLS) literature
review. You process EXACTLY ONE article. Work only from the files named below.
Do not use prior conversation, outside knowledge, or the internet.

Your job is the SUBJECTIVE pass: assign categories from a FIXED lexicon, justify
each one with evidence and a confidence rating, and identify where (if anywhere)
the article could contribute to the review — or that it does not fit. You do NOT
rewrite the objective summary or extraction; Stage 1 extraction does that.

## Inputs (read these, in order)

1. `SOURCE_TEXT` — the extracted text of the one article.
   Path: `0_human_sources/source_texts/{STEM}.txt`
2. `EXTRACTION` — the Stage 1 output for this article, if present. Path:
   `1_coded_gbls_corpus_articles/{STEM}.md` (read its Structured Extraction and
   Summary to orient yourself, but verify codes against `SOURCE_TEXT`).
3. `SCHEMA` — the FIXED lexicon. Path:
   `0_human_sources/metadata-schema-and-lexicon.md`
4. `TEMPLATE` — the required output structure. Path:
   `1_coded_gbls_corpus_articles/template.md`
5. `MANUSCRIPT` — the review whose `##` headings are the only valid contribution
   targets. Path: `0_human_sources/current_manuscript.md` (extract its `##`
   heading list; you do not need the full prose).

`{STEM}` is `{author}{year}({ZOTERO_KEY})`. The source text and output Markdown
share this exact stem.

## Output

Update one file: `1_coded_gbls_corpus_articles/{STEM}.md`

You own ONLY these sections:

1. `# Subjective Metadata`
2. `# Potential Contributions to Review`

Preserve the title, `# Objective Metadata`, `# Structured Extraction`,
`# Summary`, and `# Audit Provenance` byte-for-byte. If the objective sections
are missing (extraction has not run), still write your two sections, but note
that in your final report.

## Hard rules

- Use ONLY values that appear literally in `SCHEMA`. Never invent, reword, or
  combine values.
- Base every label on what the article actually does in `SOURCE_TEXT`, not on
  its title or what you wish it did.
- Every label carries: the value(s), `Confidence`, `Evidence`, `Reason_For`, and
  `Reason_Against`.
- Contribution `Target_Section` headings must be EXACT copies of `##` headings
  from `MANUSCRIPT`.

## Step 1 — Orient, then read for classification

Skim `EXTRACTION` (if present) for orientation, then read `SOURCE_TEXT` enough to
classify confidently: purpose, evidence, methods, setting, game formats,
audience, outcomes, conceptual framing, and any implementation conditions.

Extract the `##` heading list from `MANUSCRIPT`; those are your only allowed
`Target_Section` values.

If `SOURCE_TEXT` is empty or garbled, stop and report it instead of coding blind.

## Step 2 — Subjective Metadata (one block per field)

First update provenance at the top of `# Subjective Metadata`:

```
Coded_By: [your model name] / [online coder username if provided]
Version: [1.0 for a first coding; otherwise increment the existing value]
```

Then code each field defined in `SCHEMA`, in the template's order, using the
per-label block from `TEMPLATE`:

```
## Field_Name
Value: [schema value, or a "- " bulleted list for multi-value fields]
Confidence: [high | medium | low]
Evidence: [short quote or sentence/section reference from SOURCE_TEXT]
Reason_For: [why this label fits]
Reason_Against: [strongest reason it might not fit, or "none"]
```

Code every field: `Source_Type`, `Peer_Review`, `Evidence_Type`,
`Primary_Methodology`, `Library_Context`, `Game_Format`, `Service_Area`,
`Audience`, `Intended_Outcome`, `Evidence_Confidence`,
`Service_Conditions_Addressed`, `Conceptual_Theme`, and a final
`Coding_Confidence` (overall).

Guidance:

- Multi-value fields (`Evidence_Type`, `Game_Format`, `Service_Area`,
  `Service_Conditions_Addressed`, `Conceptual_Theme`, and others the schema
  allows) list each value as its own `- ` bullet under `Value:`.
- When a field does not fit cleanly, pick the single closest defensible `SCHEMA`
  value, set `Confidence: low`, and make `Reason_Against` explain the tension.
  Do not stack marginal guesses.
- If a service condition is not covered by the schema, set
  `Service_Conditions_Addressed` `Value:` to `other` and describe the gap in the
  Productive Incongruences note (Step 3).
- `Coding_Confidence` is your overall certainty across all fields.

The `Confidence` + `Evidence` + `Reason_Against` triple is what lets the Stage 2
audit re-check only the weak labels cheaply. Be honest with low confidence.

## Step 3 — Fit and Contributions

Under `# Potential Contributions to Review`, decide how (or whether) the article
serves the project. Three outcomes:

1. **Fits one or more sections.** For each, write a `##` heading that is an EXACT
   copy of a `MANUSCRIPT` `##` heading, then a `Contribution_Text:` with concise,
   review-ready prose. Match the most specific applicable section; synthesize,
   do not paste the summary.

2. **Relevant but incongruent.** Under `## Productive Incongruences`, explain any
   mismatch with the schema or section structure and record any `other` value
   assigned in Step 2. If none, write "No substantial incongruence identified."

3. **Does not fit the project.** Under `## Out of Scope`, state plainly that the
   article is out of scope for GBLS and justify briefly (e.g., no library
   connection; games only as metaphor). Delete this section if it does fit.

## Step 4 — Self-check

Confirm:

- Every `Value` appears verbatim in `SCHEMA`.
- Every coded field has Confidence, Evidence, Reason_For, Reason_Against.
- Every `Target_Section` is an exact copy from `MANUSCRIPT`.
- `Coded_By` and `Version` were updated.
- Template headings appear verbatim and in order.
- You did not alter the objective or audit sections.

## Final report

Report concisely:

- the `{STEM}` and output file path;
- fit outcome (fits N sections / incongruent / out of scope);
- overall `Coding_Confidence`, plus a list of any `low`/`medium`-confidence
  fields and any `other` value — these are the items Stage 2 should audit;
- whether the objective extraction was already present;
- any blockers.

If a blocker prevents confident coding, do not guess. Report it and stop.
