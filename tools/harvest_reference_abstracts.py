#!/usr/bin/env python3
"""Harvest citation metadata and abstracts for reference library journals."""

from __future__ import annotations

import html
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "0_human_sources" / "reference_abstracts"
SINCE_YEAR = 1950
NO_ABSTRACT = "not available from source"

OAI_NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


@dataclass
class Record:
    title: str = ""
    authors: list[str] = field(default_factory=list)
    year: str = ""
    journal: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    url: str = ""
    abstract: str = ""
    source: str = ""
    notes: str = ""

    def full_citation(self) -> str:
        authors = "; ".join(self.authors) if self.authors else "Unknown author"
        year = f"({self.year})." if self.year else "(n.d.)."
        title = self.title.rstrip(".") + "." if self.title else "Untitled."
        journal = f" {self.journal}"
        vol_issue = ""
        if self.volume and self.issue:
            vol_issue = f", {self.volume}({self.issue})"
        elif self.volume:
            vol_issue = f", {self.volume}"
        elif self.issue:
            vol_issue = f", no. {self.issue}"
        pages = f", {self.pages}" if self.pages else ""
        doi = f" https://doi.org/{self.doi}" if self.doi else ""
        return clean_text(f"{authors} {year} {title}{journal}{vol_issue}{pages}.{doi}")


def fetch_text(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "GBLSReferenceHarvester/1.0 (mailto:metadata@example.org)"})
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise last_error  # type: ignore[misc]


def strip_invalid_xml_chars(value: str) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", value)


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def safe_filename(record: Record, fallback: str) -> str:
    author = record.authors[0] if record.authors else fallback
    lastname = author_lastname(author) or fallback
    year = record.year or "unknown"
    return f"{lastname}{year}.md"


def author_lastname(author: str) -> str:
    author = clean_text(author)
    if not author:
        return ""
    if "," in author:
        last = author.split(",", 1)[0]
    else:
        parts = author.split()
        last = parts[-1] if parts else ""
    last = unicodedata.normalize("NFKD", last).encode("ascii", "ignore").decode("ascii")
    last = re.sub(r"[^A-Za-z0-9]+", "", last).lower()
    return last


def first(values: list[str]) -> str:
    return next((v for v in values if v), "")


def parse_source_fields(values: list[str]) -> tuple[str, str, str]:
    text = " ".join(values)
    volume = issue = pages = ""
    vol_issue = re.search(r"(?:vol(?:ume)?\.?\s*)?(\d+)\s*[,;:]?\s*(?:no\.?|issue|number)\s*(\d+)", text, re.I)
    if not vol_issue:
        vol_issue = re.search(r"\b(\d+)\s*\((\d+)\)", text)
    if vol_issue:
        volume, issue = vol_issue.group(1), vol_issue.group(2)
    page_match = re.search(r"(?:pp\.?|pages?|p\.)\s*([A-Za-z0-9]+(?:\s*-\s*[A-Za-z0-9]+)?)", text, re.I)
    if not page_match:
        page_match = re.search(r"\b(\d{1,4}\s*-\s*\d{1,4})\b", text)
    if page_match:
        pages = clean_text(page_match.group(1).replace(" ", ""))
    return volume, issue, pages


def has_real_abstract(value: str) -> bool:
    value = clean_text(value).lower()
    return bool(value) and value != NO_ABSTRACT and len(value.split()) >= 10


def harvest_oai(base_url: str, journal: str, source: str) -> list[Record]:
    records: list[Record] = []
    params = {"verb": "ListRecords", "metadataPrefix": "oai_dc"}
    token = ""
    while True:
        if token:
            url = f"{base_url}?verb=ListRecords&resumptionToken={urllib.parse.quote(token)}"
        else:
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
        root = ET.fromstring(strip_invalid_xml_chars(fetch_text(url)))
        for rec in root.findall(".//oai:record", OAI_NS):
            if rec.find("oai:header", OAI_NS) is not None and rec.find("oai:header", OAI_NS).get("status") == "deleted":
                continue
            md = rec.find(".//oai:metadata", OAI_NS)
            if md is None:
                continue
            def vals(tag: str) -> list[str]:
                return [clean_text(e.text) for e in md.findall(f".//dc:{tag}", OAI_NS)]

            dates = vals("date")
            year_match = re.search(r"(19|20)\d{2}", " ".join(dates))
            year = year_match.group(0) if year_match else ""
            if year and int(year) < SINCE_YEAR:
                continue
            identifiers = vals("identifier")
            sources = [s for s in vals("source") if not re.fullmatch(r"\d{4}-\d{3}[\dX]", s)]
            volume, issue, pages = parse_source_fields(sources)
            doi = ""
            url_value = ""
            for ident in identifiers:
                if "doi.org/" in ident:
                    doi = ident.split("doi.org/", 1)[1].strip()
                    url_value = ident
                elif ident.lower().startswith("doi:"):
                    doi = ident.split(":", 1)[1].strip()
                elif ident.startswith("http") and not url_value:
                    url_value = ident
            abstract = first(vals("description"))
            if not has_real_abstract(abstract):
                continue
            records.append(Record(
                title=first(vals("title")),
                authors=vals("creator"),
                year=year,
                journal=journal,
                volume=volume,
                issue=issue,
                pages=pages,
                doi=doi,
                url=url_value,
                abstract=abstract,
                source=source,
                notes="Harvested from OAI-PMH Dublin Core metadata. Full citation assembled from title, authors, date, source, identifier, DOI, and URL fields available in the feed.",
            ))
        token_el = root.find(".//oai:resumptionToken", OAI_NS)
        token = clean_text(token_el.text if token_el is not None else "")
        if not token:
            break
        time.sleep(0.2)
    return records


def crossref_items(issn: str, journal: str, source: str) -> list[Record]:
    records: list[Record] = []
    rows = 100
    offset = 0
    while True:
        params = {
            "filter": f"from-pub-date:{SINCE_YEAR}-01-01,type:journal-article",
            "rows": str(rows),
            "offset": str(offset),
            "select": "title,author,issued,container-title,volume,issue,page,DOI,URL,abstract",
        }
        url = f"https://api.crossref.org/journals/{urllib.parse.quote(issn)}/works?{urllib.parse.urlencode(params)}"
        data = __import__("json").loads(fetch_text(url))
        message = data.get("message", {})
        items = message.get("items", [])
        if not items:
            break
        for item in items:
            issued = item.get("issued", {}).get("date-parts", [[]])[0]
            year = str(issued[0]) if issued else ""
            if year and int(year) < SINCE_YEAR:
                continue
            authors = []
            for author in item.get("author", []) or []:
                name = " ".join(part for part in [author.get("given", ""), author.get("family", "")] if part).strip()
                if name:
                    authors.append(name)
            records.append(Record(
                title=clean_text(first(item.get("title", []))),
                authors=authors,
                year=year,
                journal=journal,
                volume=clean_text(item.get("volume", "")),
                issue=clean_text(item.get("issue", "")),
                pages=clean_text(item.get("page", "")),
                doi=clean_text(item.get("DOI", "")),
                url=clean_text(item.get("URL", "")),
                abstract=clean_text(item.get("abstract", "")) or NO_ABSTRACT,
                source=source,
                notes="Harvested from Crossref metadata. Abstract availability depends on publisher deposits.",
            ))
        offset += rows
        if offset >= min(int(message.get("total-results", 0)), 10000):
            break
        time.sleep(0.2)
    return records


def write_record(record: Record, index: int) -> Path:
    path = OUT_DIR / safe_filename(record, f"record-{index}")
    suffix = 2
    while path.exists():
        path = OUT_DIR / f"{path.stem}-{suffix - 1}.md"
        suffix += 1
    authors = "; ".join(record.authors) if record.authors else "not available from source"
    content = f"""# {record.title or 'Untitled'}

## Citation Metadata

Title: {record.title or 'not available from source'}
Authors: {authors}
Year: {record.year or 'not available from source'}
Journal: {record.journal}
Volume: {record.volume or 'not available from source'}
Issue: {record.issue or 'not available from source'}
Pages: {record.pages or 'not available from source'}
DOI: {record.doi or 'not available from source'}
URL: {record.url or 'not available from source'}
Full_Citation: {record.full_citation()}
Source: {record.source}

## Abstract

{record.abstract or 'not available from source'}

## Harvest Notes

{record.notes}
"""
    path.write_text(content, encoding="utf-8")
    return path


def record_key(record: Record) -> str:
    if record.doi:
        return f"doi:{record.doi.lower()}"
    if record.url:
        return f"url:{record.url.lower()}"
    return "title:" + "|".join([record.journal.lower(), record.year, record.title.lower()])


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()

    sources = [
        ("College & Research Libraries", lambda: harvest_oai("https://crl.acrl.org/index.php/crl/oai", "College & Research Libraries", "https://crl.acrl.org/index.php/crl/oai")),
        ("Information Technology and Libraries", lambda: crossref_items("2163-5226", "Information Technology and Libraries", "https://api.crossref.org/journals/2163-5226/works")),
        ("Library Trends", lambda: crossref_items("1559-0682", "Library Trends", "https://api.crossref.org/journals/1559-0682/works")),
        # Crossref reports no deposited abstracts for The Library Quarterly, and
        # the publisher blocks direct abstract-page harvesting. Skip it for this
        # abstract-required corpus rather than saving citation-only files.
    ]

    total = 0
    seen: set[str] = set()
    for label, fn in sources:
        print(f"Harvesting {label}...", file=sys.stderr)
        try:
            records = fn()
        except Exception as exc:
            print(f"ERROR harvesting {label}: {exc}", file=sys.stderr)
            continue
        saved = 0
        for record in records:
            if not record.title:
                continue
            if not has_real_abstract(record.abstract):
                continue
            key = record_key(record)
            if key in seen:
                continue
            seen.add(key)
            total += 1
            saved += 1
            write_record(record, total)
        print(f"Wrote {saved} abstract-bearing records for {label}", file=sys.stderr)
    print(total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
