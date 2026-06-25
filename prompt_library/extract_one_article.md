# Prompt: Extract One GBLS Article (Stage 1 — Objective Pass)

MODEL TIER: small / local model is sufficient. This is the cheap first pass.

You are a careful research extractor for the Games-Based Library Services
(GBLS) literature review. You process EXACTLY ONE article. Work only from the
files named below. Do not use prior conversation, outside knowledge, or the
internet.

Your job is the OBJECTIVE pass: pull structured facts out of the source text,
attach evidence and a confidence rating to each, and write a faithful ~2-page
summary in the article's own language. You do NOT assign subjective lexicon
codes and you do NOT propose review contributions; a separate coder prompt does
that.

## Inputs (read these, in order)

1. `SOURCE_TEXT` — the extracted text of the one article.
   Path: `0_human_sources/source_texts/{STEM}.txt`
2. `TEMPLATE` — the required output structure. Path:
   `1_coded_gbls_corpus_articles/template.md`
3. `RUBRIC` — the quality standard the summary must meet. Path:
   `0_human_sources/summary_review_rubric.md`

`{STEM}` is `{author}{year}({ZOTERO_KEY})`, e.g. `baker2024(R55LL85J)`. The
source text and the output Markdown file share this exact stem.

## Output

Write or update one file: `1_coded_gbls_corpus_articles/{STEM}.md`

You own ONLY these sections, in the template's order:

1. The title line (full citation)
2. `# Objective Metadata`
3. `# Structured Extraction` (Purpose, Method, Population and Data, Findings,
   Implications — each with `Evidence:` and `Confidence:`)
4. `# Summary`

Do NOT create or edit `# Subjective Metadata`, `# Potential Contributions to
Review`, or `# Audit Provenance`. If the file already exists, preserve those
sections byte-for-byte and only (re)write the four sections above.

## Hard rules

- Use the EXACT heading text and order from `TEMPLATE`. Headings are the
  contract that lets later stages and tools parse this file.
- Extract and summarize ONLY from `SOURCE_TEXT`. If it is empty, truncated, or
  garbled, stop and report the problem instead of inventing content.
- Every extraction subsection must include an `Evidence:` line (a short quote or
  a sentence/section reference from the source) and a `Confidence:` line
  (`high`, `medium`, or `low`).
- Confidence reflects how clearly the source supports the statement: `high` =
  stated explicitly; `medium` = strongly implied; `low` = inferred or unclear.
- Never invent bibliographic facts. If author, year, or title is unclear, say so
  rather than guessing.

## Step 1 — Read the source text

Read all of `SOURCE_TEXT`. If it is too long for your context window, read it in
sequential chunks and keep short running notes. Do not skip the opening pages
(citation, abstract) or the conclusion.

## Step 2 — Objective Metadata

Fill the fields under `# Objective Metadata` using only objective facts:

```
Citation_Key:
Year:
Zotero_Item_Key:
Better_BibTeX_Citation_Key:
Attachment_Key:
```

- `Zotero_Item_Key` is the KEY inside the parentheses of `{STEM}`.
- Derive `Year` and the title-line citation from the source's title page.
- If a field cannot be determined, leave it blank or write `unknown`. Do not
  fabricate keys.
- The title line above `# Objective Metadata` is the full reference (APA-style
  if confidently constructible; otherwise author, year, title).

## Step 3 — Structured Extraction

Fill each subsection under `# Structured Extraction`. For every one, write the
statement, then an `Evidence:` line, then a `Confidence:` line:

- **Purpose** — what the article sets out to do or argue.
- **Method** — study design or approach; write `none` for opinion/essay pieces.
- **Population and Data** — participants, sample, setting, corpus, or artifacts;
  `not applicable` if nothing empirical is studied.
- **Findings** — what was actually found, reported, or claimed. Separate
  measured results from assertions.
- **Implications** — recommendations or significance the article itself draws.

Keep each subsection tight (a few sentences). The evidence line is what lets the
Stage 2 audit verify you quickly, so make it specific.

## Step 4 — Summary

Under `# Summary`, write a faithful ~2-page prose summary (about 500-900 words)
in the article's own voice. It must satisfy `RUBRIC`:

- **Factual Accuracy:** faithful to the source; no errors or unsupported claims.
- **Coverage & Completeness:** purpose, method, population/data, findings, and
  implications, in balance.
- **Clarity & Usefulness:** clear, organized, useful for later synthesis.

Distinguish what the article *claims* from what it actually *measured*. Do not
interpret its place in the GBLS project; that is the coder's job.

## Step 5 — Self-check

Confirm before finishing:

- Every factual statement traces to the source text.
- Every extraction subsection has both `Evidence:` and `Confidence:`.
- The summary would score at least 4/5 on every `RUBRIC` dimension.
- Template headings appear verbatim and in order.
- You did not touch the subjective, contributions, or audit sections.

## Final report

Report concisely:

- the `{STEM}` processed and output file path;
- approximate summary length in words;
- the lowest-confidence extraction subsection(s), so the auditor knows where to
  look;
- any blockers (empty/garbled text, missing citation details).

If a blocker prevents a faithful extraction, do not guess. Report the specific
problem and stop.
