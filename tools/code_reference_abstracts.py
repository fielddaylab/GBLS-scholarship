#!/usr/bin/env python3
"""Code harvested reference abstracts with an OpenAI-compatible Qwen/vLLM model."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "0_human_sources" / "reference_abstracts"
OUTPUT_DIR = ROOT / "1_coded_reference_corpus_articles"
SCHEMA_PATH = ROOT / "0_human_sources" / "metadata-schema-and-lexicon.md"

DEFAULT_BASE_URL = os.environ.get("VLLM_BASE_URL", "http://100.94.191.86:11434/v1")
DEFAULT_MODEL = os.environ.get("VLLM_MODEL", "qwen3.6:35b")

FIELDS = [
    "Source_Type",
    "Evidence_Type",
    "Primary_Methodology",
    "Library_Context",
    "Game_Format",
    "Service_Area",
    "Audience",
    "Intended_Outcome",
    "Evidence_Confidence",
    "Service_Conditions_Addressed",
    "Conceptual_Theme",
    "Coding_Confidence",
]


@dataclass
class Article:
    path: Path
    title: str
    authors: str
    year: str
    journal: str
    volume: str
    issue: str
    pages: str
    doi: str
    url: str
    full_citation: str
    abstract: str


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def field(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}: (.*)$", text, re.M)
    return match.group(1).strip() if match else ""


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group("body").strip() if match else ""


def parse_article(path: Path) -> Article:
    text = path.read_text(encoding="utf-8")
    return Article(
        path=path,
        title=field(text, "Title"),
        authors=field(text, "Authors"),
        year=field(text, "Year"),
        journal=field(text, "Journal"),
        volume=field(text, "Volume"),
        issue=field(text, "Issue"),
        pages=field(text, "Pages"),
        doi=field(text, "DOI"),
        url=field(text, "URL"),
        full_citation=field(text, "Full_Citation"),
        abstract=section(text, "Abstract"),
    )


def slug_for_output(article: Article) -> str:
    return article.path.name


def prompt_for(article: Article, schema: str) -> list[dict[str, str]]:
    system = """You are a careful literature-review metadata coder. Do not think step by step. Do not output analysis or reasoning.
Code only from the citation metadata and abstract provided. Do not infer from full text, prior coding, outside knowledge, or the file name.
Use the metadata schema exactly. Prefer conservative low/medium confidence when the abstract does not provide enough evidence.
Return only Markdown, with no preamble."""

    user = f"""Use this schema and controlled vocabulary:

{schema}

Code the following abstract-only library scholarship record. Use a format as similar as possible to the `# Subjective Metadata` section in the GBLS coded corpus.

Required output format:

# Subjective Metadata

Coded_By: {DEFAULT_MODEL}
Version: 2.0.0-reference-abstract
Coding_Basis: citation_and_abstract_only

For each field below, include exactly this structure:

## FIELD_NAME
Value: one value or a Markdown list for multi-value fields
Confidence: high|medium|low
Evidence: quote or paraphrase from the citation/abstract only
Reason_For: concise rationale
Reason_Against: concise limitation or "none"

Fields to code in this order:
{chr(10).join('- ' + f for f in FIELDS)}

Important constraints:
- Source_Type should usually be peer_reviewed_journal_article unless the citation/abstract clearly indicates otherwise.
- For Game_Format, use only values from the Game_Format schema. Use unspecified_game_format unless games/play/gamification/game technology are actually mentioned. Never use not_applicable for Game_Format.
- For GBLS-specific Service_Area, Intended_Outcome, Service_Conditions_Addressed, and Conceptual_Theme, use not_applicable or not_identified when the abstract is general library scholarship without games-based service relevance.
- Do not invent pages, methods, participants, or findings not present in the abstract.
- Evidence must never cite page numbers because only citation and abstract are available.

Article citation metadata:
Title: {article.title}
Authors: {article.authors}
Year: {article.year}
Journal: {article.journal}
Volume: {article.volume}
Issue: {article.issue}
Pages: {article.pages}
DOI: {article.doi}
URL: {article.url}
Full_Citation: {article.full_citation}

Abstract:
{article.abstract}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def call_model(base_url: str, model: str, messages: list[dict[str, str]], timeout: int) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "top_p": 0.8,
        "max_tokens": 5000,
        "stream": False,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            message = body.get("choices", [{}])[0].get("message", {})
            content = message.get("content")
            if content is None:
                content = body.get("choices", [{}])[0].get("text")
            if content is None:
                content = message.get("reasoning")
            if content is None:
                raise RuntimeError(f"model returned no content: {body}")
            return str(content).strip()
        except Exception as exc:
            last_error = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"model call failed after retries: {last_error}")


def render_output(article: Article, metadata_md: str) -> str:
    metadata_md = re.sub(r"^```(?:markdown)?\s*|\s*```$", "", metadata_md.strip(), flags=re.I | re.S).strip()
    if not metadata_md.startswith("# Subjective Metadata"):
        metadata_md = "# Subjective Metadata\n\n" + metadata_md
    metadata_md = re.sub(
        r"(## Game_Format\s+Value:\s*)not_applicable\b",
        r"\1unspecified_game_format",
        metadata_md,
        flags=re.I,
    )
    metadata_md = re.sub(r"^## Service_Audience\s*$", "## Audience", metadata_md, flags=re.M)
    return f"""# {article.full_citation or article.title}

# Objective Metadata

Citation_Key: 
Year: {article.year}
Zotero_Item_Key: 
Better_BibTeX_Citation_Key: 
Attachment_Key: 

Title: {article.title}
Authors: {article.authors}
Journal: {article.journal}
Volume: {article.volume}
Issue: {article.issue}
Pages: {article.pages}
DOI: {article.doi}
URL: {article.url}
Full_Citation: {article.full_citation}

## Abstract

{article.abstract}

{metadata_md}

# Audit Provenance

Audited: no
Audited_By: not audited
Audit_Action: not audited
Audit_Notes: n/a
Sampled_For_Quality: no
"""


def code_one(path: Path, schema: str, base_url: str, model: str, timeout: int, overwrite: bool) -> tuple[str, bool, str]:
    article = parse_article(path)
    out_path = OUTPUT_DIR / slug_for_output(article)
    if out_path.exists() and not overwrite:
        return (path.name, False, "exists")
    messages = prompt_for(article, schema).copy()
    messages[1] = {"role": "user", "content": messages[1]["content"].replace(DEFAULT_MODEL, model)}
    metadata = call_model(base_url, model, messages, timeout)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_output(article, metadata), encoding="utf-8")
    return (path.name, True, "coded")


def main() -> int:
    global OUTPUT_DIR
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int, default=8, help="Number of files to code; use 0 for all")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--progress-seconds", type=int, default=60)
    args = parser.parse_args()

    OUTPUT_DIR = args.output_dir

    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    paths = sorted(args.input_dir.glob("*.md"))
    if args.limit:
        paths = paths[: args.limit]
    total = len(paths)
    if total == 0:
        print("No input files found", file=sys.stderr)
        return 1

    print(f"Coding {total} files with {args.workers} workers using {args.model} at {args.base_url}", file=sys.stderr)
    started = time.monotonic()
    last_progress = started
    completed = coded = skipped = failed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(code_one, path, schema, args.base_url, args.model, args.timeout, args.overwrite): path
            for path in paths
        }
        pending = set(futures)
        while pending:
            done, pending = concurrent.futures.wait(pending, timeout=1, return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                completed += 1
                try:
                    name, changed, status = future.result()
                    if changed:
                        coded += 1
                    else:
                        skipped += 1
                    print(f"[{completed}/{total}] {status}: {name}", file=sys.stderr)
                except Exception as exc:
                    failed += 1
                    print(f"[{completed}/{total}] failed: {futures[future].name}: {exc}", file=sys.stderr)
            now = time.monotonic()
            if now - last_progress >= args.progress_seconds:
                elapsed = int(now - started)
                print(
                    f"PROGRESS elapsed={elapsed}s completed={completed}/{total} coded={coded} skipped={skipped} failed={failed}",
                    file=sys.stderr,
                )
                last_progress = now

    print(json.dumps({"total": total, "coded": coded, "skipped": skipped, "failed": failed}, indent=2))
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
