# Prompt: Discover and Acquire New GBLS Literature

This is a self-contained agent prompt for identifying Games-Based Library
Services (GBLS) literature that is not already present in the IMLS Zotero
group library. Do not rely on prior conversation context. Work autonomously
except when user authentication, multifactor approval, CAPTCHA completion, or
another explicitly human-only action is required.

## Run Configuration

```text
PROJECT_ROOT: /Users/djgagnon/Library/CloudStorage/GoogleDrive-djgagnon@wisc.edu/.shortcut-targets-by-id/1P-yeNAX497qAu3txZnKjZZ1ztx8V2nSJ/Phase I - Research, Needs Assessment, and Lit Review Resources/GBLS Lit Review Working Docs

ZOTERO_LIBRARY: IMLS Games and Libraries
ZOTERO_GROUP_ID: 5899078
ZOTERO_LOCAL_LIBRARY_ID: 4
ZOTERO_LOCAL_API_BASE: http://127.0.0.1:23119/api
ZOTERO_DATABASE: /Users/djgagnon/Zotero/zotero.sqlite
ZOTERO_STORAGE_ROOT: /Users/djgagnon/Zotero/storage
DESTINATION_COLLECTION: Incoming

DISCOVERY_SOURCE: Google Scholar
UW_LIBRARY_HOME: https://www.library.wisc.edu/
UW_LIBRARY_SEARCH: https://search.library.wisc.edu/

MAX_SCHOLAR_RESULT_PAGES_PER_QUERY: 3
MAX_CANDIDATES_FOR_ABSTRACT_SCREENING: 40
MAX_NEW_ITEMS_PER_RUN: 15
PUBLICATION_LANGUAGE: English

REPORT_FILE: ${PROJECT_ROOT}/3_article_outputs/audits_and_synthetic_reviews/google_scholar_discovery_report.md
```

Treat these values as variables. Resolve live Zotero collection keys and
project files at runtime instead of assuming remembered keys or stale names.

## Objective

Use Google Scholar to locate credible GBLS publications that are not already
present anywhere in `${ZOTERO_LIBRARY}`. Screen candidates at title-and-
abstract level for alignment with the project's live scope. For candidates
that pass preliminary screening, obtain the best lawful full-text PDF,
using open-access copies first and UW-Madison Libraries or its authorized
proxy when needed. Import a complete parent record and readable PDF attachment
into `${ZOTERO_LIBRARY}`, and add the parent item to the Zotero collection
`${DESTINATION_COLLECTION}`.

This is a discovery, preliminary-screening, and acquisition workflow. Do not
create coded summaries, modify the review manuscript, or place items in
`GPT Summary Complete` during this run.

## Required Tools and Operating Rules

1. Use the installed Browser capability for Google Scholar, publisher,
   repository, and UW Libraries navigation.
2. Use the installed Zotero skill/helper and the local Zotero API for library
   inventory, duplicate checks, collection discovery, item verification, and
   supported writes.
3. Use browser interaction at a human pace. Do not scrape Scholar result pages
   in bulk, evade rate limits, rotate identities, bypass CAPTCHA, or use
   undocumented Scholar endpoints.
4. If Scholar presents a CAPTCHA or temporary block, pause and ask the user to
   complete it in the visible browser. Do not attempt circumvention.
5. Never ask the user to reveal a UW NetID password, Duo code, recovery code,
   session cookie, or other authentication secret.
6. Never read, store, log, copy, or transmit credentials or browser session
   tokens.
7. When UW authentication, Duo, CAPTCHA, terms acceptance, or another
   human-only action appears, make the browser visible, clearly state what the
   user needs to complete, and wait. Resume only after the user confirms or
   the authenticated page is visibly available.
8. Use only access to which the user is legitimately entitled. Do not bypass
   paywalls, DRM, license restrictions, robots controls, download limits, or
   publisher security.
9. Do not upload licensed PDFs to third-party services. Store them only as
   Zotero attachments in the configured library.
10. Do not modify the live Zotero SQLite database while Zotero is running.
    Prefer supported Zotero APIs, connector operations, or trusted existing
    project scripts. Preserve all existing item and collection data.

## Runtime Project Contract

Before searching:

1. Enumerate non-hidden documents in `${PROJECT_ROOT}/0_human_sources`.
2. Identify by contents, not filename alone:
   - the baseline structure and prose;
   - the explicit project values;
   - the metadata schema and controlled lexicon;
   - the publishability or quality rubric.
3. Read the sections that define GBLS, review scope, inclusion boundaries,
   exclusions, service areas, library contexts, evidence types, and project
   priorities.
4. Treat those live files as the authority. Do not rely on scope language
   remembered from this prompt.
5. Inspect `${PROJECT_ROOT}/1_coded_summaries` only for duplicate detection
   and coverage awareness. Do not edit existing summaries.

At minimum, interpret GBLS as library or library-connected work involving
games, play, gameful design, game collections, facilitation, spaces,
technologies, expertise, or partnerships used to advance library purposes.
The live project documents override this shorthand.

## Zotero Preparation

1. Run the Zotero helper's `status --json` command first. If the local API is
   disabled or Zotero is closed, use the helper's supported enable/start
   workflow once, then leave Zotero open.
2. Verify that the connected group is `${ZOTERO_LIBRARY}` with
   `${ZOTERO_GROUP_ID}` and `${ZOTERO_LOCAL_LIBRARY_ID}`.
3. Paginate the entire top-level item inventory. Do not treat an API page
   limit as the complete library.
4. Build a normalized duplicate index for every non-deleted top-level item,
   including:
   - DOI, normalized to lowercase without URL prefixes;
   - PMID, ISBN, ISSN, arXiv identifier, or other stable identifier when
     available;
   - normalized title;
   - first author or responsible organization;
   - publication year;
   - journal or container title;
   - Zotero parent key.
5. Also index identifiers and normalized citations from every Markdown file
   in `${PROJECT_ROOT}/1_coded_summaries`.
6. Resolve `${DESTINATION_COLLECTION}` by exact collection name in the group
   library. If it does not exist, create exactly one top-level collection
   named `Incoming` through a supported Zotero write route, then refetch and
   verify it. Do not create duplicate `Incoming` collections.
7. Preserve unrelated Zotero collection memberships. Filing in `Incoming`
   means adding that collection key to the parent item's existing collection
   list, never replacing the list.

## Discovery Strategy

Search Google Scholar using several complementary query families rather than
one broad query. Derive additional terms from the live baseline and controlled
lexicon. Begin with combinations such as:

```text
"games-based library services"
"game-based library services"
libraries games programming
library gaming programs
"video games" libraries programming
"tabletop games" libraries
"board games" libraries programming
"role-playing games" libraries
TTRPG libraries
"escape room" library instruction
gamification libraries information literacy
games academic libraries orientation
games public libraries community
games school libraries literacy
games library collections cataloging
video game preservation libraries archives
game metadata libraries discovery
```

For each query:

1. Review no more than
   `${MAX_SCHOLAR_RESULT_PAGES_PER_QUERY}` result pages.
2. Record the exact query and search date.
3. Inspect result title, authors, year, venue, snippet, cited-by count, and
   available abstract or landing-page metadata.
4. Follow promising `Cited by`, `Related articles`, and reference-chain leads
   selectively when they are likely to reveal distinct GBLS publications.
5. Prefer sources that add evidence, settings, formats, populations, service
   models, or historical coverage not already prominent in the library.
6. Do not use citation count as a relevance or quality threshold. Recent,
   local, professional, and implementation literature may be relevant despite
   low citation counts.
7. Stop collecting new candidates after
   `${MAX_CANDIDATES_FOR_ABSTRACT_SCREENING}` unique, non-duplicate candidates
   have been assembled or the configured searches are exhausted.

## Candidate Deduplication

Perform duplicate checking before substantive screening and again immediately
before import.

Classify a candidate as already present when any of these conditions holds:

1. Exact DOI or other stable identifier match.
2. Exact normalized title match.
3. High-confidence fuzzy title match combined with compatible author and year.
4. Matching author, year, journal, volume, and first page or article number.
5. A coded summary contains the same Zotero-independent identifier or clearly
   represents the same publication.

Treat preprints, accepted manuscripts, conference papers, and later journal
articles as potentially distinct versions. Do not import a second version
automatically. Record the relationship and import only when the newer or
different version has independent scholarly value or materially different
content. Prefer the version of record for metadata and a lawful accepted
manuscript for the attachment when necessary.

When uncertain, mark `Possible duplicate` and do not import until the conflict
is resolved.

## Preliminary Abstract-Level Screening

Retrieve the fullest lawful abstract available from Scholar, Crossref,
publisher metadata, an institutional repository, or another authoritative
bibliographic source. Do not infer an abstract from the title or Scholar
snippet.

Screen each unique candidate against the live project scope and assign one
decision:

- `Include`: clear, direct alignment with GBLS and sufficient bibliographic
  confidence to seek full text.
- `Maybe`: plausible alignment, but the abstract is missing, ambiguous, or
  does not establish a direct library connection.
- `Exclude`: clearly outside the live scope.
- `Duplicate`: already present in Zotero or the coded-summary corpus.
- `Possible duplicate`: unresolved version or identity conflict.

Assess and record:

1. **Library connection:** Is the setting a library, archive, cultural
   heritage institution, library school, or program directly connected to
   library services?
2. **Game specificity:** Are games, gaming, role-play, game creation,
   gamification, or gameful design a substantive object, intervention,
   collection, or service rather than a passing metaphor?
3. **Service relevance:** Does the source address collections, access,
   discovery, advisory, programming, facilitation, instruction, literacy,
   community, inclusion, outreach, professional capacity, preservation,
   research support, space, or infrastructure?
4. **Publication fit:** Is it an English-language, text-based publication
   appropriate to the live review scope?
5. **Evidence contribution:** What kind of evidence or knowledge could it add:
   empirical study, implementation case, synthesis, artifact analysis,
   framework, historical analysis, or practitioner reflection?
6. **Novelty to the corpus:** Does it add a setting, population, method,
   format, outcome, tension, or historical precedent not already well
   represented?
7. **Abstract confidence:** Is the decision based on a full abstract,
   structured summary, authoritative metadata, or only a limited snippet?

Do not exclude a publication merely because it challenges project values or
current review arguments. Do not treat practitioner reflections as empirical
outcome evidence. Do not treat broad game-based learning research without a
library connection as GBLS evidence.

For every decision, write a concise rationale grounded in the available
abstract and metadata. Never claim to have reviewed the full text during this
stage.

## Full-Text Acquisition Order

Attempt full-text retrieval only for `Include` candidates. A `Maybe` candidate
may be promoted to `Include` if an accessible landing page or preview supplies
enough information to resolve scope ambiguity. Otherwise leave it in the
report without importing it.

Use this acquisition order:

1. Publisher-provided open-access PDF.
2. Author or institutional repository accepted manuscript.
3. Subject repository or stable public archive.
4. UW-Madison Libraries availability or article-linking service.
5. Authorized UW-Madison proxy access to the publisher.

For UW access:

1. Begin at `${UW_LIBRARY_HOME}` or `${UW_LIBRARY_SEARCH}` when practical.
2. Search by DOI first, then exact title.
3. Use UW's licensed full-text or `Find It` path rather than constructing
   speculative proxy URLs.
4. If a legitimate UW proxy link is already supplied by the library, follow
   it. Do not invent or repeatedly mutate proxy URLs.
5. When authentication appears, make the browser visible and pause for the
   user to complete NetID and Duo authentication.
6. After authentication, resume from the resulting authorized page.
7. If licensed access is unavailable, record the access failure. Do not seek
   unauthorized copies or bypass controls.

Before accepting a download, verify:

- HTTP content or file signature identifies a PDF;
- the file opens and is not an HTML login or error page renamed `.pdf`;
- title and first author match the candidate;
- the PDF is complete enough for later review;
- it is the article, not supplementary material, a table of contents, or a
  one-page preview.

Use a temporary download location until Zotero import succeeds. Remove
temporary duplicate files after verification.

## Zotero Import and Filing

For each successfully acquired `Include` candidate:

1. Re-run duplicate detection against the live group library immediately
   before writing.
2. Create or import one complete top-level bibliographic record in
   `${ZOTERO_LIBRARY}` using DOI metadata, a publisher-supported translator,
   RIS, BibTeX, or another authoritative source.
3. Prefer metadata from the version of record. Verify:
   - title and subtitle;
   - complete author list and order;
   - publication year and date;
   - item type;
   - journal, conference, book, or publisher;
   - volume, issue, pages, or article number;
   - DOI and canonical URL;
   - abstract when available;
   - language.
4. Do not invent missing metadata. Flag uncertain fields in the report.
5. Attach the verified full-text PDF as a stored Zotero attachment under the
   parent item. Use a descriptive attachment title such as `Full Text PDF`.
6. Add the parent item to `${DESTINATION_COLLECTION}` while preserving all
   other collection memberships.
7. File only the parent item in `Incoming`; leave child attachment collection
   state unchanged.
8. Refetch the parent and its children. Verify:
   - the parent is in the intended group library;
   - the `Incoming` collection key is present;
   - exactly one intended parent record was created;
   - the PDF child exists and has MIME type `application/pdf`;
   - the attachment file is readable from Zotero storage or indexed full text;
   - title, DOI, and author-year still match the candidate.
9. If metadata import succeeds but PDF attachment fails, keep the parent in
   `Incoming`, report `PDF pending`, and state the precise access or write
   blocker.
10. If a duplicate appears during import, preserve the better existing record,
    attach the PDF to it only when appropriate, add that parent to `Incoming`,
    and remove no records without explicit user approval.

Do not add imported items to `GPT Summary Complete`, topical review
collections, or exclusion collections during this workflow.

## Discovery Report

Create or replace `${REPORT_FILE}`. The report must not contain credentials,
cookies, proxy session URLs, or licensed full-text content.

Use this structure:

```markdown
# Google Scholar GBLS Discovery Report

## Run Summary

- Search date:
- Scholar queries completed:
- Unique candidates screened:
- Existing-library duplicates:
- Included and imported:
- Included but PDF pending:
- Maybe:
- Excluded:
- Possible duplicates:

## Search Log

| Query | Result pages reviewed | Candidates retained | Notes |
|---|---:|---:|---|

## Imported to Incoming

| Citation | DOI or stable ID | Abstract-level rationale | Evidence type | PDF source route | Zotero parent key | PDF attachment key | Verification |
|---|---|---|---|---|---|---|---|

## Include, Acquisition Blocked

| Citation | DOI or stable ID | Rationale | Access attempts | Exact blocker |
|---|---|---|---|---|

## Maybe

| Citation | Available evidence | Uncertainty | Recommended next step |
|---|---|---|---|

## Excluded

| Citation | Exclusion reason |
|---|---|

## Duplicates and Version Conflicts

| Candidate | Existing Zotero key | Match basis | Resolution |
|---|---|---|---|

## Coverage Observations

Briefly identify recurring search gaps, underrepresented library contexts,
game formats, populations, service areas, methods, or publication types. Keep
these observations preliminary and do not modify the project scope or schema.
```

Use stable public DOI or publisher URLs in the report where useful. Do not
record expiring UW proxy links.

## Completion and Stopping Rules

Stop when any of the following occurs:

1. `${MAX_NEW_ITEMS_PER_RUN}` new parent items have been imported and verified.
2. `${MAX_CANDIDATES_FOR_ABSTRACT_SCREENING}` unique candidates have been
   screened.
3. All configured query families and defensible citation-chain leads are
   exhausted.
4. Scholar blocks further searching and the user cannot complete the required
   human check.
5. UW authentication or licensed access cannot be completed.
6. Zotero writes cannot be performed safely.

Do not count duplicates, excluded candidates, or unresolved `Maybe` candidates
toward `${MAX_NEW_ITEMS_PER_RUN}`.

## Final Quality Check

Before reporting completion, verify:

- every imported publication was absent from Zotero before import;
- every imported item passed abstract-level GBLS screening;
- every imported parent is in exactly one verified `Incoming` collection;
- every claimed PDF is a readable full-text PDF attached to the correct
  parent;
- no credentials, cookies, session tokens, or licensed text appear in project
  files or logs;
- no existing coded summary or review manuscript was modified;
- no item was added to `GPT Summary Complete`;
- ambiguous candidates remain clearly labeled `Maybe` or
  `Possible duplicate`;
- evidence claims in the report do not exceed abstract-level review;
- unrelated Zotero records, collections, and project files were preserved.

## Final Response

Report:

- search queries and result pages reviewed;
- candidates screened by decision category;
- each item imported with Zotero parent and attachment keys;
- items blocked by access or PDF retrieval;
- duplicate and version-conflict findings;
- whether user authentication was required;
- the exact path to `${REPORT_FILE}`;
- confirmation that imported parents were filed in `${DESTINATION_COLLECTION}`.

Begin immediately with the configured defaults. Ask the user only when a
human-only authentication, CAPTCHA, consent, or unresolved identity decision
prevents safe progress.
