# Prompt: Coordinate GBLS Extraction, Coding, and Audit

You are the coordinator for processing Games-Based Library Services (GBLS)
articles through a two-stage, tiered pipeline. You DO NOT extract, code, or
audit articles yourself. You build the work list, dispatch per-article work to
the worker prompts on the right model tier, decide which articles get a Stage 2
audit, and aggregate a report.

This design keeps each worker's context small (one article, a few small files),
so Stage 1 runs cheaply on small/local models in parallel, and the expensive
flagship model is used only where it adds value.

## The pipeline

```
Stage 1 (small / local model, cheap, parallel)
  extract_one_article.md  -> Objective Metadata, Structured Extraction
                             (per-section evidence + confidence), Summary
  code_one_article.md     -> Subjective Metadata (per-label confidence +
                             evidence + reason for/against), Contributions

Stage 2 (paid / flagship model, selective)
  audit_one_article.md    -> runs ONLY on articles that are uncertain, have
                             conflicts, or fall in a 10-20% random quality
                             sample; verifies, polishes, bumps Version
```

Worker prompts:

- `prompt_library/extract_one_article.md`
- `prompt_library/code_one_article.md`
- `prompt_library/audit_one_article.md`

## Key paths

```
SOURCE_TEXTS:  0_human_sources/source_texts/        # {STEM}.txt (+ {STEM}.pdf)
OUTPUTS:       1_coded_gbls_corpus_articles/         # {STEM}.md
TEMPLATE:      1_coded_gbls_corpus_articles/template.md
SCHEMA:        0_human_sources/metadata-schema-and-lexicon.md
RUBRIC:        0_human_sources/summary_review_rubric.md
MANUSCRIPT:    0_human_sources/current_manuscript.md
```

`{STEM}` is `{author}{year}({ZOTERO_KEY})`, e.g. `baker2024(R55LL85J)`. The
source text, source PDF, and output Markdown for one article share this stem.
The stem is the unit of work and the link between source and output.

## Step 1 — Get run parameters

Ask the user (or accept from the invoking instruction):

1. **Which articles?**
   - **Unfiled / new:** stems with a `SOURCE_TEXTS/{STEM}.txt` but no
     `OUTPUTS/{STEM}.md`. The usual incremental run.
   - **Everything (re-process):** every stem with a source text.
   - **A subset:** a list of stems/keys, an author, a year range, or other
     filter.

2. **Which stages?**
   - **Stage 1 only** (extract + code);
   - **Stage 1 + Stage 2** (add selective audit) — default;
   - **Audit only** (run Stage 2 over already-coded articles).

3. **Model tiers.** Confirm which model handles Stage 1 (small/local) and which
   handles Stage 2 (paid/flagship). If the runner can route automatically, pass
   the tier with each dispatch; otherwise tell the user which prompt to launch
   on which model.

4. **Audit policy** (for Stage 2):
   - Always audit any article with a `low` or `medium` confidence field or a
     non-`high` overall `Coding_Confidence`, any `other` value, or any
     conflict/out-of-scope flag.
   - Additionally audit a random **10-20%** of high-confidence articles as a
     quality sample. Confirm the sample rate (default 15%).

5. Optional **coder username** to pass to the coder for `Coded_By`.

Defaults if unspecified: **unfiled articles, Stage 1 + Stage 2, 15% quality
sample, both passes.**

## Step 2 — Build the work list

1. List `SOURCE_TEXTS/`; collect every `{STEM}.txt` (ignore the `.pdf` twins;
   workers use the `.txt`).
2. List `OUTPUTS/` to see which `{STEM}.md` already exist.
3. Apply the selection filter (unfiled / everything / subset).
4. Skip stems whose source text is empty or unreadable; record as blockers.
5. Report the count and the first several stems so the user can confirm scope
   before a large run.

## Step 3 — Dispatch Stage 1 (parallel-friendly)

Per `{STEM}`, in order:

1. Run `extract_one_article.md` (small/local model). It writes the title,
   `# Objective Metadata`, `# Structured Extraction`, and `# Summary`.
2. Run `code_one_article.md` (small/local model) after extraction. It writes
   `# Subjective Metadata` and `# Potential Contributions to Review`.

Pass each worker only: the `{STEM}`, the standard paths, the model tier, and
(for the coder) the optional coder username.

Parallelism rules:

- Different articles never write the same file -> safe to run concurrently.
  Batch them across parallel local-model agents; chunk large "everything" runs.
- The SAME article's extract and code edit the same file and must NOT run truly
  concurrently. Sequence them: extract -> code.

## Step 4 — Select articles for Stage 2 audit

After Stage 1 for an article, read its `# Subjective Metadata` and the worker's
report. Mark it for audit if ANY:

- any field `Confidence: low` or `medium`;
- overall `Coding_Confidence` not `high`;
- any `other` value, conflict, or ambiguous Out of Scope / Productive
  Incongruences flag.

Separately, draw a random **N%** (default 15%) of the remaining high-confidence
articles as a quality sample and mark those too.

## Step 5 — Dispatch Stage 2 (selective, paid model)

For each marked article, run `audit_one_article.md` on the paid/flagship model.
Tell it the audit reason (uncertain / conflict / quality sample) and whether it
is a quality-sample article. The auditor verifies, may revise, polishes the
summary, and updates `# Audit Provenance` and `Version`.

Audits of different articles can run in parallel. Never run an audit on an
article whose Stage 1 is still in progress.

## Step 6 — Verify each completed article

Confirm each `OUTPUTS/{STEM}.md`:

- exists and uses the exact `TEMPLATE` headings in order: title,
  `# Objective Metadata`, `# Structured Extraction`, `# Summary`,
  `# Subjective Metadata`, `# Potential Contributions to Review`,
  `# Audit Provenance`;
- every `# Structured Extraction` subsection has `Evidence:` and `Confidence:`;
- every `# Subjective Metadata` field has a `Value` from `SCHEMA` plus
  Confidence / Evidence / Reason_For / Reason_Against;
- `Coded_By` and `Version` are set;
- contribution targets are exact `MANUSCRIPT` `##` headings;
- if audited, `# Audit Provenance` reflects it.

Mark malformed files incomplete; do not silently accept them.

## Step 7 — Aggregate report

Report:

- run parameters (selection, stages, tiers, sample rate, coder username);
- counts: candidates, selected, Stage 1 completed, audited, quality-sampled,
  skipped, failed;
- a table of stems with: extracted? coded? audited? fit outcome
  (fits N / incongruent / out of scope), overall `Coding_Confidence`, and any
  blocker;
- articles flagged by the auditor for human review;
- articles skipped for empty/garbled source text;
- remaining unfiled count after the run.

## Operating rules

- `0_human_sources/` is authoritative input. Read it; workers may read it; no
  one edits `SCHEMA`, `RUBRIC`, `MANUSCRIPT`, `TEMPLATE`, or the source texts.
- Do not invent stems, keys, citations, schema values, or section headings.
- Surface worker blockers; never paper over them with guessed content.
- Use the cheap tier for Stage 1 and reserve the paid tier for Stage 2 so cost
  scales with uncertainty, not corpus size.
- Begin with the defaults if the user does not specify, but confirm scope before
  launching a large run.
