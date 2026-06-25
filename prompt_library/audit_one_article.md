# Prompt: Audit One GBLS Article (Stage 2 — Verification Pass)

MODEL TIER: paid / flagship model (e.g. Sonnet, GPT-5-mini, Gemini Pro). This
pass is expensive, so it runs SELECTIVELY — only when an article needs it, not
on every article.

You verify and finalize ONE already-extracted, already-coded article. Work only
from the files named below. Do not use prior conversation or the internet.

## When this prompt runs

The coordinator sends an article to audit when ANY of these is true:

1. **Uncertain classification** — the coder marked one or more fields
   `Confidence: low` or `medium`, or the overall `Coding_Confidence` is not
   `high`.
2. **Category conflict** — labels disagree with the extraction or summary, an
   `other` value was used, or the coder flagged Productive Incongruences / Out
   of Scope ambiguously.
3. **Quality sample** — the article was randomly selected as part of a 10-20%
   audit sample even though its confidence is high.

If none of these apply, the article should not be sent here; if it is, do a
light confirmation pass and record it.

## Inputs

1. `ARTICLE` — the file to audit:
   `1_coded_gbls_corpus_articles/{STEM}.md`
2. `SOURCE_TEXT` — ground truth:
   `0_human_sources/source_texts/{STEM}.txt`
3. `SCHEMA` — the fixed lexicon:
   `0_human_sources/metadata-schema-and-lexicon.md`
4. `RUBRIC` — summary quality standard:
   `0_human_sources/summary_review_rubric.md`
5. `MANUSCRIPT` — valid contribution targets (its `##` headings):
   `0_human_sources/current_manuscript.md`
6. `TEMPLATE` — the required structure:
   `1_coded_gbls_corpus_articles/template.md`

The coordinator also tells you the **audit reason** (uncertain / conflict /
quality sample) and whether this is a **quality-sample** article.

## What you may change

You may revise any section of `ARTICLE` to make it correct and faithful, but:

- Use the EXACT template headings and order; never restructure the file.
- Use ONLY `SCHEMA` values for classification.
- Use ONLY exact `MANUSCRIPT` `##` headings as contribution targets.
- Preserve `Objective Metadata` keys unless they are factually wrong.
- Make minimal, justified edits. Do not rewrite content that is already correct.

## Step 1 — Read ground truth, then the article

Read `SOURCE_TEXT` first so your judgment is anchored in the source, not in the
existing coding. Then read `ARTICLE`.

## Step 2 — Targeted verification

Focus your effort where it matters:

- **Low/medium-confidence fields:** re-decide each using `SOURCE_TEXT` and
  `SCHEMA`. Confirm or correct the `Value`, then update `Confidence`, `Evidence`,
  `Reason_For`, and `Reason_Against`.
- **Conflicts and `other` values:** resolve the disagreement. Either pick a
  defensible schema value, or confirm the incongruence is real and document it
  under `## Productive Incongruences`.
- **Out-of-scope claims:** verify the article truly does or does not belong in
  the GBLS review.
- **Contributions:** confirm each `Target_Section` is an exact `MANUSCRIPT`
  heading and that the `Contribution_Text` is accurate and review-ready.

For a **quality-sample** article whose confidence is already high, spot-check a
few labels and the summary rather than re-deciding everything.

## Step 3 — Polish the summary

Check the `# Summary` against `RUBRIC`. If it scores below 4/5 on any dimension
(Factual Accuracy, Coverage & Completeness, Clarity & Usefulness), revise it so
it does. Keep the article's own voice; do not pad to length. Verify every claim
against `SOURCE_TEXT` and the `# Structured Extraction` evidence lines.

## Step 4 — Update Audit Provenance and Version

In `# Audit Provenance`, set:

```
Audited: yes
Audited_By: [your model name]
Audit_Action: [confirmed | revised classifications | revised summary | flagged | ...]
Audit_Notes: [what you checked or changed, and why — brief]
Sampled_For_Quality: [yes | no]
```

In `# Subjective Metadata`, increment `Version` (e.g., `1.0` -> `1.1` for a
refinement, larger bump for substantial recoding) and append your model to
`Coded_By` if you changed any codes.

If after review the article cannot be confidently coded or summarized from the
source, set `Audit_Action: flagged`, explain in `Audit_Notes`, and leave the
best-supported values in place rather than guessing.

## Step 5 — Self-check

Confirm:

- Every classification `Value` is a verbatim `SCHEMA` value.
- Every revised field has consistent Confidence / Evidence / Reason_For /
  Reason_Against.
- Contribution targets are exact `MANUSCRIPT` headings.
- The summary meets `RUBRIC`.
- Template headings are verbatim and in order.
- `Audit Provenance` and `Version` are updated.

## Final report

Report concisely:

- the `{STEM}` and the audit reason;
- fields confirmed vs. revised (with old -> new for revisions);
- whether the summary was revised and why;
- final overall `Coding_Confidence`;
- whether you flagged the article for human review;
- whether it was a quality-sample article.
