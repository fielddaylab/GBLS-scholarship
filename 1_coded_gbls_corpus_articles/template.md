# [Full citation / reference for the article]

<!--
  FORMAT NOTES (delete when filling, or leave — parsers ignore HTML comments)

  This file is built in stages and shares its filename stem with the source
  text: 0_human_sources/source_texts/{author}{year}(ZOTERO_KEY).txt
  ->        1_coded_gbls_corpus_articles/{author}{year}(ZOTERO_KEY).md

  Pipeline that fills this file:
    Stage 1  extract_one_article.md   (small/local model) -> Objective Metadata,
             Structured Extraction (each subsection has Evidence + Confidence),
             and the Summary.
    Stage 1  code_one_article.md      (small/local model) -> Subjective Metadata
             (each label has confidence + evidence + reason for/against) and
             Potential Contributions to Review.
    Stage 2  audit_one_article.md     (paid/flagship model) -> reviews low/medium
             confidence items, resolves conflicts, polishes the Summary, and
             updates Audit Provenance + Version.

  Use the EXACT heading text and order below. Headings are the contract.
  Confidence is always one of: high | medium | low.
-->

# Objective Metadata

Citation_Key:
Year:
Zotero_Item_Key:
Better_BibTeX_Citation_Key:
Attachment_Key:

# Structured Extraction

## Purpose
[What the article sets out to do or argue, in the article's own terms.]
Evidence: [short quote(s) or sentence/section reference from the source text]
Confidence: [high | medium | low]

## Method
[What the article did: study design, approach, or "none" for opinion/essay.]
Evidence: [quote or reference]
Confidence: [high | medium | low]

## Population and Data
[Who or what was studied: participants, sample, setting, corpus, or artifacts.
 Use "not applicable" if the source studies nothing empirically.]
Evidence: [quote or reference]
Confidence: [high | medium | low]

## Findings
[What the article actually found, reported, or claimed. Distinguish measured
 results from assertions.]
Evidence: [quote or reference]
Confidence: [high | medium | low]

## Implications
[What the article says follows from its work — recommendations, significance,
 or implications it draws.]
Evidence: [quote or reference]
Confidence: [high | medium | low]

# Summary
[A faithful ~2-page prose summary (about 500-900 words) in the article's own
 language and voice. Covers purpose, method, population/data, findings, and
 implications, and notes relevance to games-based library services where the
 article supports it. No invented claims.]

# Subjective Metadata

Coded_By: [model name] / [online coder username, if any]
Version: 1.0

<!--
  For each field below, use ONLY values from
  0_human_sources/metadata-schema-and-lexicon.md.
  Multi-value fields list each value as its own "- " bullet.
  Each field carries: the value(s), Confidence, Evidence, and brief
  Reason_For / Reason_Against. Keep the value line first so it stays easy to
  read and parse.
-->

## Source_Type
Value: [one schema value]
Confidence: [high | medium | low]
Evidence: [quote or reference]
Reason_For: [why this label fits]
Reason_Against: [strongest reason it might not fit, or "none"]

## Peer_Review
Value: [one schema value]
Confidence: [high | medium | low]
Evidence:
Reason_For:
Reason_Against:

## Evidence_Type
Value:
- [schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Primary_Methodology
Value: [one schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Library_Context
Value: [one schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Game_Format
Value:
- [schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Service_Area
Value:
- [schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Audience
Value: [one schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Intended_Outcome
Value: [one schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Evidence_Confidence
Value: [one schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Service_Conditions_Addressed
Value:
- [schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Conceptual_Theme
Value:
- [schema value]
Confidence:
Evidence:
Reason_For:
Reason_Against:

## Coding_Confidence
Value: [high | medium | low — overall confidence in the classification]

# Potential Contributions to Review

<!--
  Target_Section must be an EXACT copy of a "## " heading from
  0_human_sources/current_manuscript.md. Add one block per fitting section.
  If the article does not fit, use the Productive Incongruences or Out of Scope
  note instead.
-->

## [Exact ## heading copied from current_manuscript.md]
Contribution_Text: [concise, review-ready prose explaining what this article
  contributes to that section.]

## Productive Incongruences
[Any mismatch with the schema or section structure; record any "other" value
 assigned above. Or: "No substantial incongruence identified."]

## Out of Scope
[If the article does not belong in the GBLS review, state so and justify
 briefly. Otherwise delete this section.]

# Audit Provenance

Audited: [yes | no]
Audited_By: [paid model name, or "not audited"]
Audit_Action: [confirmed | revised classifications | revised summary | flagged | not audited]
Audit_Notes: [what the auditor checked or changed, or "n/a"]
Sampled_For_Quality: [yes | no]
