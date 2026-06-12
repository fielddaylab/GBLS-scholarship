#!/usr/bin/env python3
"""Build a non-destructive quotation-backed audit for a GBLS manuscript."""

from __future__ import annotations

import argparse
import functools
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]{2,}")
YEAR_RE = r"(?:19|20)\d{2}[a-z]?"
PAREN_CITE_RE = re.compile(r"\(([^()]*?\b" + YEAR_RE + r"[^()]*)\)")
NARRATIVE_CITE_RE = re.compile(
    r"\b([A-Z][A-Za-z'’-]+(?:\s+(?:and|&)\s+[A-Z][A-Za-z'’-]+)?"
    r"(?:\s+et al\.)?)\s*\((" + YEAR_RE + r")\)"
)
STOP = {
    "about", "after", "again", "against", "also", "among", "because", "been",
    "before", "being", "between", "both", "could", "does", "from", "have",
    "into", "itself", "more", "most", "other", "over", "rather", "should",
    "such", "than", "that", "their", "them", "these", "they", "this", "those",
    "through", "under", "using", "were", "what", "when", "where", "which",
    "while", "with", "within", "would", "game", "games", "library", "libraries",
}


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def tokens(value: str) -> set[str]:
    return {w.lower() for w in WORD_RE.findall(value) if w.lower() not in STOP}


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    return [
        part.strip()
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"'])", text)
        if part.strip()
    ]


def citation_pairs(sentence: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for author, year in NARRATIVE_CITE_RE.findall(sentence):
        surname = author.split()[0]
        pairs.append((norm(surname), year[:4]))
    for group in PAREN_CITE_RE.findall(sentence):
        chunks = [chunk.strip() for chunk in group.split(";")]
        for chunk in chunks:
            years = re.findall(YEAR_RE, chunk)
            if not years:
                continue
            author_match = re.search(r"([A-Z][A-Za-z'’-]+)", chunk)
            if not author_match:
                continue
            surname = norm(author_match.group(1))
            pairs.extend((surname, year[:4]) for year in years)
    seen = set()
    return [pair for pair in pairs if not (pair in seen or seen.add(pair))]


@functools.lru_cache(maxsize=None)
def load_source(path: Path, _text_cache: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def source_candidates(source_dir: Path) -> dict[tuple[str, str], list[Path]]:
    result: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for path in sorted(source_dir.iterdir()):
        if path.suffix.lower() != ".txt":
            continue
        match = re.match(r"([A-Za-z'’-]+).*?((?:19|20)\d{2})", path.stem)
        if match:
            result[(norm(match.group(1)), match.group(2))].append(path)
    return result


@functools.lru_cache(maxsize=None)
def passages(text: str) -> tuple[tuple[int, str], ...]:
    rows = []
    for line_no, line in enumerate(text.splitlines(), 1):
        clean = re.sub(r"\s+", " ", line).strip()
        if 45 <= len(clean) <= 900 and len(tokens(clean)) >= 5:
            rows.append((line_no, clean))
    if rows:
        return tuple(rows)
    return tuple(
        (idx, sentence)
        for idx, sentence in enumerate(split_sentences(text), 1)
        if len(sentence) >= 45
    )


def best_quote(claim: str, paths: list[Path], pdf_cache: Path) -> tuple[float, Path | None, int, str]:
    claim_tokens = tokens(re.sub(PAREN_CITE_RE, "", claim))
    best = (0.0, None, 0, "")
    for path in paths:
        text = load_source(path, pdf_cache)
        for line_no, passage in passages(text):
            passage_tokens = tokens(passage)
            if not claim_tokens or not passage_tokens:
                continue
            overlap = len(claim_tokens & passage_tokens)
            recall = overlap / len(claim_tokens)
            precision = overlap / min(len(passage_tokens), max(len(claim_tokens) * 2, 1))
            score = (0.8 * recall) + (0.2 * precision)
            if score > best[0]:
                best = (score, path, line_no, passage)
    return best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("audit", type=Path)
    parser.add_argument("revised", type=Path)
    args = parser.parse_args()

    draft = args.draft.read_text(encoding="utf-8")
    index = source_candidates(args.source_dir)
    heading = "(front matter)"
    claims = []
    for paragraph in re.split(r"\n\s*\n", draft):
        if paragraph.startswith("#"):
            heading = paragraph.splitlines()[0].lstrip("# ").strip()
            continue
        for sentence in split_sentences(paragraph):
            pairs = citation_pairs(sentence)
            if pairs:
                claims.append((heading, sentence, pairs))

    statuses = Counter()
    entries = []
    missing_sources = set()
    with tempfile.TemporaryDirectory(prefix="gbls-factcheck-") as tmp:
        pdf_cache = Path(tmp)
        for claim_no, (claim_heading, claim, pairs) in enumerate(claims, 1):
            evidence = []
            for pair in pairs:
                candidates = index.get(pair, [])
                if not candidates:
                    evidence.append((pair, 0.0, None, 0, ""))
                    missing_sources.add(f"{pair[0]} ({pair[1]})")
                    continue
                evidence.append((pair, *best_quote(claim, candidates, pdf_cache)))

            found = [item for item in evidence if item[2] is not None]
            if not found:
                status = "source_text_missing"
            elif any(item[1] < 0.20 for item in found):
                status = "not_located"
            elif len(found) < len(pairs):
                status = "partially_verified"
            elif min(item[1] for item in found) < 0.34:
                status = "verified_with_scope_change"
            else:
                status = "verified"
            statuses[status] += 1
            entries.append((claim_no, claim_heading, claim, status, evidence))

    # Preserve the historical command-line contract, but never rewrite prose.
    args.revised.write_text(draft, encoding="utf-8")

    lines = [
        "# Factual Reliability Audit",
        "",
        "## Feasibility Run",
        "",
        f"- Input draft: `{args.draft.name}`",
        f"- TXT source files available: {sum(1 for p in args.source_dir.iterdir() if p.suffix.lower() == '.txt')}",
        f"- Citation-bearing claims audited: {len(entries)}",
        f"- Claims provisionally verified by direct quotation: {statuses['verified']}",
        f"- Claims requiring scope change: {statuses['verified_with_scope_change']}",
        f"- Claims partially verified: {statuses['partially_verified']}",
        f"- Claims with source text missing: {statuses['source_text_missing']}",
        f"- Claims where support was not located: {statuses['not_located']}",
        "",
        "This feasibility run used exact passages from `.txt` files in "
        "`corpus_source_texts` and "
        "lexical retrieval to test the scale and file-resolution requirements of "
        "the new workflow. `Verified` is provisional until a human or semantic "
        "reviewer confirms that the quoted passage entails the full claim. The "
        "manuscript copy is preserved unchanged. Retrieval scores identify "
        "claims for semantic review; they do not authorize automatic deletion.",
        "",
        "## Missing Source Texts",
        "",
    ]
    lines.extend(f"- {item}" for item in sorted(missing_sources))
    if not missing_sources:
        lines.append("- None")
    lines.extend(["", "## Claim Ledger", ""])

    for claim_no, claim_heading, claim, status, evidence in entries:
        lines.extend(
            [
                f"### FC-{claim_no:04d}",
                "",
                f"- Heading: {claim_heading}",
                f"- Status: `{status}`",
                f"- Claim: {claim}",
                "- Evidence:",
            ]
        )
        for pair, score, path, line_no, quote in evidence:
            if path is None:
                lines.append(f"  - {pair[0]} ({pair[1]}): source text missing")
            else:
                clipped = quote[:700].replace("\n", " ")
                lines.append(
                    f"  - `{path.name}`, text line {line_no}, retrieval score "
                    f"{score:.3f}: “{clipped}”"
                )
        disposition = (
            "No automatic change; quotation support should be confirmed during independent review."
            if status == "verified"
            else "Flagged for semantic review; manuscript text preserved unchanged."
        )
        lines.extend([f"- Disposition: {disposition}", ""])

    lines.extend(
        [
            "## Feasibility Finding",
            "",
            "The pass is computationally feasible using the existing TXT source "
            "extractions and claim-level quotation retrieval. Fully autonomous completion is not "
            "responsible when lexical similarity is treated as semantic proof. "
            "The production workflow therefore requires semantic verification "
            "during independent review and prohibits automated prose deletion.",
            "",
        ]
    )
    args.audit.write_text("\n".join(lines), encoding="utf-8")
    print(
        f"claims={len(entries)} verified={statuses['verified']} "
        f"flagged={len(entries) - statuses['verified']} missing_sources={len(missing_sources)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
