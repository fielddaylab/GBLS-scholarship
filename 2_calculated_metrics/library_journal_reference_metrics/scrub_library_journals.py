#!/usr/bin/env python3
"""Collect journal article metadata into a one-row-per-article Markdown table.

The crawler prefers metadata from each journal archive and article page. If a
publisher blocks crawling, it can fall back to Crossref's public API.
"""

from __future__ import annotations

import argparse
import html
import io
import json
import logging
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urljoin, urlparse, urlunparse

import requests
import yaml
from bs4 import BeautifulSoup
from pypdf import PdfReader
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


USER_AGENT = (
    "GBL-journal-metadata-research/1.0 "
    "(polite academic metadata collection; contact via local project)"
)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.I)
YEAR_RE = re.compile(r"\b(18|19|20)\d{2}\b")
ARTICLE_HINTS = (
    "/doi/",
    "/article/view/",
    "/article/",
    "/articles/",
    "/pub/",
)
ISSUE_HINTS = (
    "/toc/",
    "/loi/",
    "/issue/",
    "/issues/",
    "/journal/",
    "/vol",
)
SKIP_SUFFIXES = (
    ".css",
    ".csv",
    ".doc",
    ".docx",
    ".epub",
    ".gif",
    ".ico",
    ".jpg",
    ".jpeg",
    ".js",
    ".json",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".rss",
    ".svg",
    ".tif",
    ".tiff",
    ".txt",
    ".xml",
    ".xls",
    ".xlsx",
    ".zip",
)


@dataclass
class Article:
    journal: str
    year: str
    issue: str
    title: str
    authors: str
    abstract: str
    doi: str
    url: str = ""


def clean_text(value: object) -> str:
    if value is None:
        return ""
    soup = BeautifulSoup(html.unescape(str(value)), "html.parser")
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text).strip()


def normalize_doi(value: str) -> str:
    match = DOI_RE.search(html.unescape(value or ""))
    return match.group(0).rstrip(".,;:)") if match else ""


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = re.sub(r"/+", "/", parsed.path).rstrip("/") or "/"
    path = re.sub(
        r"/doi/(?:abs|epub|full|ref|suppl)/(?=10\.)",
        "/doi/",
        path,
        flags=re.I,
    )
    query = "" if re.search(r"/doi/10\.", path, re.I) else parsed.query
    return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", query, ""))


def year_from(value: str) -> str:
    match = YEAR_RE.search(value or "")
    return match.group(0) if match else ""


def markdown_cell(value: str) -> str:
    return clean_text(value).replace("\\", "\\\\").replace("|", "\\|")


def make_session() -> requests.Session:
    retry = Retry(
        total=4,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8",
        }
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    return session


def load_journals(path: Path) -> list[dict[str, str]]:
    source = path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(source)
    except yaml.YAMLError as exc:
        logging.warning(
            "%s is not strict YAML (%s); using the simple journal-list parser",
            path,
            exc.problem if hasattr(exc, "problem") else exc,
        )
        data = {"journals": load_simple_journal_list(source)}
    if isinstance(data, dict):
        data = data.get("journals", [])
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a 'journals' list")
    journals = []
    for item in data:
        if not isinstance(item, dict) or not item.get("name") or not item.get("archive"):
            raise ValueError("Each journal needs both 'name' and 'archive'")
        journals.append({str(key): str(value) for key, value in item.items()})
    return journals


def load_simple_journal_list(source: str) -> list[dict[str, str]]:
    """Parse the project's flat journal list, including unquoted colons in values."""
    journals: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "journals:":
            continue
        if line.startswith("- "):
            if current:
                journals.append(current)
            current = {}
            line = line[2:].strip()
        if current is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        current[key.strip()] = value.strip().strip("'\"")
    if current:
        journals.append(current)
    return journals


def meta_values(soup: BeautifulSoup, *names: str) -> list[str]:
    ordered_names = [name.lower() for name in names]
    values_by_name = {name: [] for name in ordered_names}
    for tag in soup.find_all("meta"):
        key = (tag.get("name") or tag.get("property") or "").lower()
        if key in values_by_name and tag.get("content"):
            value = clean_text(tag["content"])
            if value and value not in values_by_name[key]:
                values_by_name[key].append(value)
    values = []
    for name in ordered_names:
        values.extend(values_by_name[name])
    return values


def jsonld_objects(soup: BeautifulSoup) -> Iterable[dict]:
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            payload = json.loads(script.string or script.get_text())
        except (json.JSONDecodeError, TypeError):
            continue
        stack = payload if isinstance(payload, list) else [payload]
        while stack:
            obj = stack.pop()
            if not isinstance(obj, dict):
                continue
            yield obj
            graph = obj.get("@graph")
            if isinstance(graph, list):
                stack.extend(graph)


def jsonld_article(soup: BeautifulSoup) -> dict:
    for obj in jsonld_objects(soup):
        kinds = obj.get("@type", [])
        kinds = [kinds] if isinstance(kinds, str) else kinds
        if any(str(kind).lower() in {"article", "scholarlyarticle", "newsarticle"} for kind in kinds):
            return obj
    return {}


def author_names(value: object) -> list[str]:
    people = value if isinstance(value, list) else [value]
    names = []
    for person in people:
        if isinstance(person, dict):
            name = person.get("name")
            if not name:
                name = " ".join(
                    part for part in (person.get("givenName"), person.get("familyName")) if part
                )
        else:
            name = str(person or "")
        name = clean_text(name)
        if name and name not in names:
            names.append(name)
    return names


def extract_article(soup: BeautifulSoup, url: str, journal: str) -> Article | None:
    data = jsonld_article(soup)
    title = next(
        iter(meta_values(soup, "citation_title", "dc.title", "og:title")),
        clean_text(data.get("headline") or data.get("name")),
    )
    authors = meta_values(soup, "citation_author", "dc.creator")
    if not authors:
        authors = author_names(data.get("author", []))
    abstract = next(
        iter(
            meta_values(
                soup,
                "citation_abstract",
                "dc.description",
                "description",
                "og:description",
            )
        ),
        clean_text(data.get("abstract") or data.get("description")),
    )
    if not abstract:
        selectors = (
            ".abstract",
            "#abstract",
            ".abstractSection",
            ".article-abstract",
            "#articleAbstract",
            "[class*='abstractInFull']",
            "[class*='abstract']",
        )
        for selector in selectors:
            node = soup.select_one(selector)
            candidate = clean_text(node.get_text(" ", strip=True)) if node else ""
            candidate = re.sub(r"^\s*Abstract\s*", "", candidate, flags=re.I)
            if len(candidate) >= 40:
                abstract = candidate
                break
    if abstract and clean_text(abstract).casefold() == clean_text(title).casefold():
        abstract = ""

    doi_values = meta_values(soup, "citation_doi", "dc.identifier", "dc.identifier.doi")
    doi = normalize_doi(" ".join(doi_values))
    if not doi:
        doi = normalize_doi(str(data.get("sameAs") or data.get("identifier") or ""))

    date = next(
        iter(
            meta_values(
                soup,
                "citation_publication_date",
                "citation_date",
                "dc.date",
                "article:published_time",
            )
        ),
        clean_text(data.get("datePublished")),
    )
    volume = next(iter(meta_values(soup, "citation_volume")), "")
    issue_number = next(iter(meta_values(soup, "citation_issue")), "")
    issue = ", ".join(
        part
        for part in (
            f"Vol. {volume}" if volume else "",
            f"No. {issue_number}" if issue_number else "",
        )
        if part
    )
    if not issue:
        issue = next(iter(meta_values(soup, "citation_journal_title.issue")), "")

    generic_titles = {"home", "current issue", "table of contents", journal.lower()}
    if not title or title.lower() in generic_titles:
        return None
    looks_like_article = is_probable_article(url)
    if not looks_like_article:
        return None
    return Article(
        journal=journal,
        year=year_from(date),
        issue=issue,
        title=title,
        authors="; ".join(authors),
        abstract=abstract,
        doi=doi,
        url=url,
    )


def is_probable_article(url: str) -> bool:
    path = urlparse(url).path.lower()
    if (
        path.endswith(SKIP_SUFFIXES)
        or "/article/download/" in path
        or re.search(r"/doi/(?:epdf|pdf|pdfdirect)/", path)
        or "/doi/toc/" in path
    ):
        return False
    if "/article/view/" in path:
        tail = path.split("/article/view/", 1)[1].strip("/").split("/")
        return len(tail) == 1
    return any(hint in path for hint in ARTICLE_HINTS)


def is_probable_index(url: str, archive_url: str) -> bool:
    parsed = urlparse(url)
    archive = urlparse(archive_url)
    if parsed.netloc.lower() != archive.netloc.lower():
        return False
    path = parsed.path.lower()
    query = parsed.query.lower()
    if "/hub/" in path:
        return False
    return (
        any(hint in path for hint in ISSUE_HINTS)
        or "page=" in query
        or "page/" in path
        or normalize_url(url) == normalize_url(archive_url)
    ) and not path.endswith(SKIP_SUFFIXES)


def links_from(soup: BeautifulSoup, base_url: str) -> set[str]:
    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if not href or href.startswith(("#", "javascript:", "mailto:")):
            continue
        url = normalize_url(urljoin(base_url, href))
        if url.startswith(("http://", "https://")):
            links.add(url)
    return links


def link_belongs_to_journal(link: str, archive: str) -> bool:
    """Apply narrow publisher guards where one host serves many related journals."""
    archive_parsed = urlparse(archive)
    path = unquote(urlparse(link).path).lower()
    ojs_match = re.search(r"^(.*?/index\.php/[^/]+)(?:/|$)", archive_parsed.path, re.I)
    if ojs_match:
        journal_root = ojs_match.group(1).lower().rstrip("/")
        return path == journal_root or path.startswith(f"{journal_root}/")
    if (
        archive_parsed.netloc.endswith("onlinelibrary.wiley.com")
        and archive_parsed.path.rstrip("/").endswith("/23301643")
    ):
        if "/doi/" in path:
            return "/doi/10.1002/asi." in path or "1097-4571" in path
        if "/toc/" in path:
            return "/toc/23301643/" in path or "/toc/19366108/" in path
        if "/loi/" in path:
            return "/loi/23301643" in path
        return normalize_url(link) == normalize_url(archive)
    return True


def blocked_page(response: requests.Response, soup: BeautifulSoup) -> bool:
    text = clean_text(soup.title.get_text() if soup.title else "")
    body = response.text[:5000].lower()
    return (
        response.status_code in (401, 403)
        or "just a moment" in text.lower()
        or "cf-chl-" in body
        or "access denied" in body
        or "captcha" in body
    )


def pdf_abstract(content: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages[:3])
    except Exception as exc:
        logging.debug("Could not extract PDF text: %s", exc)
        return ""
    text = text.replace("\r", "\n")
    match = re.search(
        r"\bAbstract\b\s*[:.-]?\s*(.+?)(?=\n\s*(?:Keywords?|Introduction|"
        r"Background|Literature Review|Statement of (?:the )?Problem)\b)",
        text,
        flags=re.I | re.S,
    )
    if not match:
        return ""
    abstract = clean_text(match.group(1))
    return abstract if len(abstract) >= 40 else ""


def crawl_school_library_research(
    session: requests.Session,
    journal: dict[str, str],
    delay: float,
) -> tuple[list[Article], bool]:
    name = journal["name"]
    roots = (
        "https://www.ala.org/aasl/pubs/slr/archive",
        "https://www.ala.org/aasl/pubs/slr",
    )
    volume_urls: set[str] = set()
    for root in roots:
        logging.info("[%s] Discovering volumes from %s", name, root)
        response = session.get(root, timeout=40)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for link in links_from(soup, response.url):
            if re.search(r"/aasl/pubs/slr/vol\d+/?$", urlparse(link).path, re.I):
                volume_urls.add(link)

    articles: list[Article] = []
    ordered_volumes = sorted(
        volume_urls,
        key=lambda value: int(re.search(r"vol(\d+)", value, re.I).group(1)),
    )
    for volume_index, volume_url in enumerate(ordered_volumes, 1):
        volume_match = re.search(r"vol(\d+)", volume_url, re.I)
        volume = volume_match.group(1)
        logging.info(
            "[%s] Volume %s (%d/%d) %s",
            name,
            volume,
            volume_index,
            len(ordered_volumes),
            volume_url,
        )
        response = session.get(volume_url, timeout=40)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        pdf_links = [
            tag
            for tag in soup.find_all("a", href=True)
            if urlparse(tag["href"]).path.lower().endswith(".pdf")
        ]
        for article_index, tag in enumerate(pdf_links, 1):
            title = clean_text(tag.get_text(" ", strip=True))
            paragraph = tag.find_parent("p")
            citation = clean_text(paragraph.get_text(" ", strip=True)) if paragraph else ""
            prefix = clean_text(paragraph.get_text(" ", strip=True).split(title, 1)[0]) if paragraph else ""
            citation_match = re.match(r"^(.*?)\s*\((\d{4})\)\.?\s*$", prefix)
            authors = clean_text(citation_match.group(1)) if citation_match else ""
            year = citation_match.group(2) if citation_match else year_from(citation)
            pdf_href = tag["href"].strip()
            if re.match(r"^(?:sites|aasl/sites)/", pdf_href, re.I):
                pdf_href = f"/{pdf_href}"
            pdf_url = normalize_url(urljoin(response.url, pdf_href))
            logging.info(
                "[%s] Volume %s article %d/%d: %s",
                name,
                volume,
                article_index,
                len(pdf_links),
                title,
            )
            abstract = ""
            try:
                pdf_response = session.get(pdf_url, timeout=90)
                pdf_response.raise_for_status()
                abstract = pdf_abstract(pdf_response.content)
            except requests.RequestException as exc:
                logging.warning("[%s] Could not fetch PDF %s: %s", name, pdf_url, exc)
            articles.append(
                Article(
                    journal=name,
                    year=year,
                    issue=f"Vol. {volume}",
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    doi=normalize_doi(citation),
                    url=pdf_url,
                )
            )
            time.sleep(delay)
    return articles, False


def crawl_archive(
    session: requests.Session,
    journal: dict[str, str],
    delay: float,
    max_pages: int,
) -> tuple[list[Article], bool]:
    name = journal["name"]
    archive = normalize_url(journal["archive"])
    if name.casefold() == "school library research" and "ala.org" in urlparse(archive).netloc:
        return crawl_school_library_research(session, journal, delay)
    queue = [archive]
    queued = {archive}
    visited = set()
    articles: list[Article] = []
    blocked = False

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        visited.add(url)
        logging.info("[%s] %d/%d %s", name, len(visited), max_pages, url)
        try:
            response = session.get(url, timeout=40)
            response.raise_for_status()
        except requests.RequestException as exc:
            logging.warning("[%s] Could not fetch %s: %s", name, url, exc)
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        if blocked_page(response, soup):
            logging.warning("[%s] Publisher blocked archive crawling at %s", name, url)
            blocked = True
            break

        article = extract_article(soup, response.url, name)
        if article:
            articles.append(article)
            time.sleep(delay)
            continue

        for link in links_from(soup, response.url):
            if link in queued:
                continue
            if urlparse(link).netloc.lower() != urlparse(archive).netloc.lower():
                continue
            if not link_belongs_to_journal(link, archive):
                continue
            if is_probable_article(link):
                queue.insert(0, link)
                queued.add(link)
            elif is_probable_index(link, archive):
                queue.append(link)
                queued.add(link)
        time.sleep(delay)
    if queue:
        logging.warning(
            "[%s] Reached --max-pages=%d with %d URLs still queued",
            name,
            max_pages,
            len(queue),
        )
    return articles, blocked


def similarity(left: str, right: str) -> float:
    left_words = set(re.findall(r"[a-z0-9]+", left.lower()))
    right_words = set(re.findall(r"[a-z0-9]+", right.lower()))
    return len(left_words & right_words) / max(1, len(left_words | right_words))


def resolve_crossref_issn(session: requests.Session, journal: dict[str, str]) -> str:
    if journal.get("issn"):
        return journal["issn"]
    archive_path = urlparse(journal.get("archive", "")).path
    embedded_issn = re.search(r"(?:^|/)(\d{8})(?:/|$)", archive_path)
    if embedded_issn:
        digits = embedded_issn.group(1)
        return f"{digits[:4]}-{digits[4:]}"
    response = session.get(
        "https://api.crossref.org/journals",
        params={"query": journal["name"], "rows": 10},
        timeout=40,
    )
    response.raise_for_status()
    candidates = response.json()["message"]["items"]
    if not candidates:
        return ""
    best = max(candidates, key=lambda item: similarity(journal["name"], item.get("title", "")))
    if similarity(journal["name"], best.get("title", "")) < 0.35:
        return ""
    issns = best.get("ISSN", [])
    return issns[0] if issns else ""


def crossref_articles(
    session: requests.Session,
    journal: dict[str, str],
    delay: float,
    max_records: int,
) -> list[Article]:
    name = journal["name"]
    try:
        issn = resolve_crossref_issn(session, journal)
    except (requests.RequestException, KeyError, ValueError) as exc:
        logging.warning("[%s] Crossref journal lookup failed: %s", name, exc)
        return []
    if not issn:
        logging.warning("[%s] Crossref could not confidently resolve an ISSN", name)
        return []

    logging.info("[%s] Crossref fallback using ISSN %s", name, issn)
    articles = []
    cursor = "*"
    rows = 1000
    while len(articles) < max_records:
        response = session.get(
            f"https://api.crossref.org/journals/{issn}/works",
            params={
                "cursor": cursor,
                "rows": min(rows, max_records - len(articles)),
                "select": "DOI,title,author,abstract,published-print,published-online,issued,issue,volume,URL,type",
            },
            timeout=60,
        )
        response.raise_for_status()
        message = response.json()["message"]
        items = message.get("items", [])
        if not items:
            break
        for item in items:
            if item.get("type") not in (None, "journal-article"):
                continue
            title = clean_text(" ".join(item.get("title", [])))
            if not title:
                continue
            author_list = []
            for author in item.get("author", []):
                author_list.append(
                    clean_text(
                        " ".join(
                            part for part in (author.get("given"), author.get("family")) if part
                        )
                    )
                )
            date_parts = []
            for key in ("published-print", "published-online", "issued"):
                date_parts = item.get(key, {}).get("date-parts", [])
                if date_parts:
                    break
            year = str(date_parts[0][0]) if date_parts and date_parts[0] else ""
            volume = clean_text(item.get("volume"))
            issue_number = clean_text(item.get("issue"))
            issue = ", ".join(
                part
                for part in (
                    f"Vol. {volume}" if volume else "",
                    f"No. {issue_number}" if issue_number else "",
                )
                if part
            )
            articles.append(
                Article(
                    journal=name,
                    year=year,
                    issue=issue,
                    title=title,
                    authors="; ".join(filter(None, author_list)),
                    abstract=clean_text(item.get("abstract")),
                    doi=normalize_doi(item.get("DOI", "")),
                    url=item.get("URL", ""),
                )
            )
        next_cursor = message.get("next-cursor")
        if not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
        time.sleep(delay)
    return articles


def deduplicate(articles: Iterable[Article]) -> list[Article]:
    merged: dict[str, Article] = {}
    for article in articles:
        title_key = (
            f"title:{article.journal.lower()}:"
            f"{re.sub(r'[^a-z0-9]', '', article.title.lower())}"
        )
        key = title_key
        current = merged.get(key)
        if current is None:
            merged[key] = article
            continue
        for field in ("year", "issue", "title", "authors", "abstract", "doi", "url"):
            old = getattr(current, field)
            new = getattr(article, field)
            if not old or len(new) > len(old):
                setattr(current, field, new)
    return sorted(
        merged.values(),
        key=lambda item: (item.journal.lower(), item.year or "0000", item.title.lower()),
    )


def write_markdown(path: Path, articles: list[Article]) -> None:
    lines = [
        "# Journal Article Titles and Abstracts",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "| Journal | Year | Issue | Article title | Authors | Abstract | DOI |",
        "|---|---:|---|---|---|---|---|",
    ]
    for article in articles:
        doi = (
            f"[{markdown_cell(article.doi)}](https://doi.org/{article.doi})"
            if article.doi
            else ""
        )
        cells = (
            article.journal,
            article.year,
            article.issue,
            article.title,
            article.authors,
            article.abstract,
        )
        lines.append("| " + " | ".join(markdown_cell(cell) for cell in cells) + f" | {doi} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_checkpoint(path: Path, articles: list[Article]) -> None:
    path.write_text(
        "\n".join(json.dumps(asdict(article), ensure_ascii=False) for article in articles) + "\n",
        encoding="utf-8",
    )


def load_checkpoint(path: Path) -> list[Article]:
    articles = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            articles.append(Article(**json.loads(line)))
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError(f"Invalid checkpoint line {line_number} in {path}: {exc}") from exc
    return articles


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        help="YAML file (default: journal.yaml, journals.yaml, or journals beside script)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("journal_article_archive.md"),
        help="Markdown output path",
    )
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between requests")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=10000,
        help="Maximum archive/article pages visited per journal",
    )
    parser.add_argument(
        "--max-crossref-records",
        type=int,
        default=100000,
        help="Maximum Crossref records per journal",
    )
    parser.add_argument(
        "--crossref",
        choices=("fallback", "always", "never"),
        default="fallback",
        help="When to supplement archive crawling with Crossref",
    )
    parser.add_argument(
        "--journal",
        action="append",
        default=[],
        help="Only process journal names containing this text (repeatable)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Load the output checkpoint and skip journals already represented there",
    )
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def find_default_config(script_dir: Path) -> Path:
    for name in ("journal.yaml", "journals.yaml", "journals.yml", "journals"):
        candidate = script_dir / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No journal.yaml, journals.yaml, journals.yml, or journals file found")


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    script_dir = Path(__file__).resolve().parent
    config = args.config.resolve() if args.config else find_default_config(script_dir)
    output = args.output
    if not output.is_absolute():
        output = script_dir / output
    checkpoint = output.with_suffix(".jsonl")
    journals = load_journals(config)
    if args.journal:
        needles = [value.lower() for value in args.journal]
        journals = [
            journal
            for journal in journals
            if any(needle in journal["name"].lower() for needle in needles)
        ]
    if not journals:
        raise SystemExit("No journals matched")

    session = make_session()
    all_articles: list[Article] = []
    completed_journals: set[str] = set()
    if args.resume and checkpoint.exists():
        all_articles = deduplicate(load_checkpoint(checkpoint))
        completed_journals = {article.journal for article in all_articles}
        logging.info(
            "Resuming with %d records across %d completed journals",
            len(all_articles),
            len(completed_journals),
        )
    for journal in journals:
        if journal["name"] in completed_journals:
            logging.info("[%s] Already checkpointed; skipping", journal["name"])
            continue
        archive_articles, blocked = crawl_archive(
            session, journal, args.delay, args.max_pages
        )
        logging.info(
            "[%s] Extracted %d archive records",
            journal["name"],
            len(archive_articles),
        )
        all_articles.extend(archive_articles)

        use_crossref = args.crossref == "always" or (
            args.crossref == "fallback" and (blocked or not archive_articles)
        )
        if use_crossref:
            try:
                fallback = crossref_articles(
                    session, journal, args.delay, args.max_crossref_records
                )
            except (requests.RequestException, KeyError, ValueError) as exc:
                logging.warning("[%s] Crossref fallback failed: %s", journal["name"], exc)
                fallback = []
            logging.info("[%s] Extracted %d Crossref records", journal["name"], len(fallback))
            all_articles.extend(fallback)

        all_articles = deduplicate(all_articles)
        write_checkpoint(checkpoint, all_articles)
        write_markdown(output, all_articles)
        logging.info("Checkpoint: %d total records in %s", len(all_articles), output)

    missing_abstracts = sum(not article.abstract for article in all_articles)
    logging.info(
        "Done: %d articles (%d without an available abstract)",
        len(all_articles),
        missing_abstracts,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
