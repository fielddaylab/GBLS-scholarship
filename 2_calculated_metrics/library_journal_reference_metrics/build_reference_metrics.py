#!/usr/bin/env python3
"""Build the lightweight journal reference corpus used by Metrics Explorer."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def joined(value: object) -> str:
    if isinstance(value, list):
        return "|".join(str(item) for item in value if str(item).strip())
    return str(value or "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows = [
        json.loads(line)
        for line in args.manifest.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    articles = []
    journals = Counter()
    for row in rows:
        journal = str(row.get("journal") or "")
        journals[journal] += 1
        articles.append(
            {
                "article_id": Path(str(row["filename"])).stem,
                "year": int(row["year"]) if str(row.get("year", "")).isdigit() else None,
                "journal": journal,
                "source_type": "peer_reviewed_journal_article",
                "peer_review": "peer_reviewed",
                "evidence_type": joined(row.get("evidence")),
                "primary_methodology": joined(row.get("method")),
                "library_context": joined(row.get("context")),
                "game_format": joined(row.get("game")),
                "service_area": joined(row.get("services")),
                "audience": joined(row.get("audience")),
                "intended_outcome": joined(row.get("outcomes")),
                "coding_confidence": joined(row.get("confidence")),
            }
        )

    years = sorted({article["year"] for article in articles if article["year"] is not None})
    payload = {
        "summary": {
            "total_articles": len(articles),
            "earliest_year": years[0] if years else None,
            "latest_year": years[-1] if years else None,
            "journals": len(journals),
            "coding_basis": "abstract_only",
        },
        "years": years,
        "journals": dict(sorted(journals.items())),
        "articles": articles,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "window.GBLS_REFERENCE_CORPUS = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "articles": len(articles),
                "years": len(years),
                "journals": len(journals),
                "bytes": args.output.stat().st_size,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
