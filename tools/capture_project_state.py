#!/usr/bin/env python3
"""Capture a compact, machine-readable GBLS project checkpoint."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "project_state.json"


def count_files(directory: str, pattern: str, excluded: set[str] | None = None) -> int:
    excluded = excluded or set()
    path = ROOT / directory
    if not path.exists():
        return 0
    return sum(
        1
        for item in path.glob(pattern)
        if item.is_file() and item.name not in excluded
    )


def sha256(relative_path: str) -> str | None:
    path = ROOT / relative_path
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def load_json(relative_path: str) -> object | None:
    path = ROOT / relative_path
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


status = git("status", "--porcelain=v1") or ""
status_lines = status.splitlines()
status_counts = {
    "entries": len(status_lines),
    "staged": sum(1 for line in status_lines if line and line[0] not in {" ", "?"}),
    "unstaged": sum(1 for line in status_lines if len(line) > 1 and line[1] != " "),
    "untracked": sum(1 for line in status_lines if line.startswith("??")),
}

key_files = [
    "readme.md",
    "project_memory.md",
    "data_contracts.md",
    "file_formats.md",
    "todos.md",
    "0_human_sources/baseline_structure_and_prose.md",
    "0_human_sources/explicit_values.md",
    "0_human_sources/metadata_schema_and_lexicon.md",
    "0_human_sources/publishability_rubric.md",
    "1_coded_journal_article_archive/_manifest.jsonl",
    "prompt_library/assemble_review.md",
    "prompt_library/rebuild_gbls_corpus_metrics.md",
    "tools/gbls_lit_coder/package-lock.json",
]

manifest_path = ROOT / "1_coded_journal_article_archive" / "_manifest.jsonl"
manifest_records = (
    sum(
        1
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    if manifest_path.is_file()
    else 0
)

state = {
    "schema_version": 1,
    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    "project_root": str(ROOT),
    "git": {
        "branch": git("branch", "--show-current"),
        "head": git("rev-parse", "HEAD"),
        "remote": git("remote", "get-url", "fielddaylab"),
        "dirty": bool(status_lines),
        "status_counts": status_counts,
    },
    "counts": {
        "source_txt": count_files("0_human_sources/corpus_source_texts", "*.txt"),
        "source_pdf": count_files("0_human_sources/corpus_source_texts", "*.pdf"),
        "coded_summaries": count_files(
            "1_coded_summaries", "*.md", {"template.md"}
        ),
        "reference_coded_articles": count_files(
            "1_coded_journal_article_archive", "*.md", {"_readme.md"}
        ),
        "reference_manifest_records": manifest_records,
        "prompt_files": count_files("prompt_library", "*.md")
        + count_files("prompt_library/assemble_review_phases", "*.md")
        + count_files("prompt_library/tools", "*.py"),
        "article_output_files": sum(
            1
            for item in (ROOT / "3_article_outputs").rglob("*")
            if item.is_file()
        )
        if (ROOT / "3_article_outputs").exists()
        else 0,
    },
    "validation": load_json("2_calculated_metrics/validation_report.json"),
    "key_file_sha256": {path: sha256(path) for path in key_files},
    "external_state": [
        "Zotero group library, collections, attachments, and stable item keys",
        "Google Drive hydration, permissions, and shared generated outputs",
        "Cloudflare Worker deployment and KV coding records",
        "Institutional authentication used for lawful source acquisition",
    ],
}

OUTPUT.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT}")
print(json.dumps(state["counts"], indent=2, sort_keys=True))
print(json.dumps(state["git"], indent=2, sort_keys=True))
