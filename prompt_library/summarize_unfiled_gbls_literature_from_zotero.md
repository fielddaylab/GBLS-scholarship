# Prompt: Summarize One Unfiled GBLS Article from Zotero Queue

Self-contained, single-article workflow for processing unfiled Games-Based Library Services (GBLS) literature from the Zotero group library. This prompt processes one randomly-selected unfiled article with PDF attachment per execution, moving it from unfiled to filed status upon completion. Do not rely on prior context.

## KEY CONCEPT: "Unfiled" Status

In the Zotero group library (5899078), articles begin in "unfiled" status when their `collections` array is empty. This workflow processes unfiled articles one at a time, moving each article to "filed" status by adding it to the "Summary Complete" collection (and section-specific collections) after the summary is written.

## CONFIGURATION

ZOTERO_GROUP_ID: 5899078
ZOTERO_LIBRARY: "IMLS Games and Libraries"
PROJECT_ROOT: /Users/djgagnon/development/gameBasedLibraryServicesLiterature
SUMMARY_FOLDER: ${PROJECT_ROOT}/1_coded_gbls_corpus_articles
HUMAN_SOURCES_FOLDER: ${PROJECT_ROOT}/0_human_sources
METADATA_SCHEMA_FILE: ${HUMAN_SOURCES_FOLDER}/metadata-schema-and-lexicon.md
BASELINE_FILE: ${HUMAN_SOURCES_FOLDER}/current_manuscript.md

COLLECTION_COMPLETE_NAME: "Summary Complete"
TOOL_SCRIPT: ${PROJECT_ROOT}/tools/fetch_unfiled.py

PROTECTED_DIRECTORIES: ${HUMAN_SOURCES_FOLDER} (read-only; no modifications)

## OBJECTIVE: Process One Unfiled Article

1. Execute `${TOOL_SCRIPT}` to fetch all unfiled articles (with PDF attachments) from `${ZOTERO_GROUP_ID}`.
2. Select one unfiled article at random from the results.
3. Retrieve the article's PDF from Zotero.
4. Read the article carefully and classify it using `${METADATA_SCHEMA_FILE}` controlled vocabulary (all fields required).
5. Write a single standalone summary markdown file in `${SUMMARY_FOLDER}` following the naming convention.
6. File the processed article in Zotero by adding it to "Summary Complete" collection and any section-specific collections that match its contributions (moving it from unfiled to filed status).

## FILENAME CONVENTION

Pattern: `{author_lastname}{year}({zotero_item_key}).md`

Example: `baker2024(R55LL85J).md`

Rules:
- Normalize author's last name to lowercase ASCII; remove spaces, punctuation, apostrophes, hyphens.
- Use only the first author's last name. For organizational authors, use a concise filesystem-safe name.
- Use publication year or "nd" if unavailable.
- Preserve parentheses around the Zotero key and the `.md` extension.
- Do not overwrite an existing file. If a filename collision occurs with a different article, stop and investigate.

## QUICK CHECKLIST

Before starting:
- [ ] Zotero credentials in `project-config.json` (ZOTERO_USER_ID, ZOTERO_API_KEY)
- [ ] Python venv activated: `source venv/bin/activate`
- [ ] `requests` library installed: `pip install requests`
- [ ] Both reference files readable: `metadata-schema-and-lexicon.md`, `current_manuscript.md`

After completing workflow:
- [ ] Summary file exists in `1_coded_gbls_corpus_articles/` with correct filename
- [ ] All metadata fields populated with only controlled values (no invented values)
- [ ] APA citation complete and accurate
- [ ] No duplicate filename in corpus
- [ ] Zotero collections updated (Summary Complete + section-specific)

## ZOTERO COLLECTION MAPPING

When filing articles, map "Suggested Review Contributions" sections to the corresponding Zotero collections. Use this reference table:

| Manuscript Section | Zotero Collection | Collection Key |
| --- | --- | --- |
| Games as Mainstream Cultural Media | Games as Mainstream Cultural Media | AA79VNPC |
| Games as Participatory and Expressive Media | Games as Participatory and Expressive Media | (manual: search in Zotero) |
| Libraries as Playful Spaces | Libraries as Playful Spaces | (manual: search in Zotero) |
| Collections, Circulation, and Equitable Access | Collections, Circulation, and Access | ARXDAJN9 |
| Description, Discovery, and Games Advisory | Cataloging, Metadata, and Discovery | CWG9IH2A |
| Instruction, Orientation, and Information Literacy | Instruction, Orientation, and Information Literacy | 958P2U9Y |
| Community, Belonging, Wellness, and the Public Commons | Community, Belonging, and the Public Commons | 63VME7T7 |
| Programming Formats and Service Models | Programming Formats and Service Models | H4ZJFKBR |
| Escape Rooms and Breakout Boxes | Escape Rooms and Breakout Boxes | QX6WR59G |
| TTRPG and LARP Programs | TTRPG and LARP Programs | 8ZPAY526 |
| Cross-Cutting Conditions | Cross-Cutting Lessons for Game-Based Library Services | LTVNZ7LP |
| Professional Practice, Education, Training Gaps | Professional Practice and Training Gaps | 5XHGTLBV |
| Summary Complete (required) | Summary Complete | XDJU2DNT |

**If a section doesn't match the above table exactly:** Search the Zotero group (5899078) in the web interface for the collection name, copy its key from the URL, and document it here for future use.

## EDGE CASES AND EXAMPLES

**Unknown Publication Date:**
- If `data.date` is missing or unclear, use "nd" (no date) in the filename.
- Example: `smith(nd)(ABC123XY).md` if author is Smith but year unknown.
- In the metadata section, set `Year: nd`.

**Multiple Authors:**
- Use only the first author's last name.
- Example: If authors are "Zhang, Lee, and Kim", use `zhang` in filename.

**Organizational or Corporate Author:**
- If no individual author is listed (e.g., "Association of College and Research Libraries"), use a short, filesystem-safe abbreviation.
- Example: `acrl2020(87ZB9FSP).md` for ACRL-published work.

**Unparseable Zotero Metadata:**
- If title is in non-Latin script, use author + year only.
- If author is genuinely unknown, note in "Productive Incongruences" and assign filename as `unknown{year}({key}).md`.

**No PDF Attachment:**
- If an article shows 1+ children but no PDF file is present, skip it and select a different unfiled article.
- Document in final report: "Skipped {key} — no PDF child found."

**Multiple PDF Attachments:**
- If an article has more than one PDF child, use the first one (likely the article itself, not supplementary materials).

## WORKFLOW

### Step 1: Fetch Unfiled Articles
Execute: `python3 ${TOOL_SCRIPT}`

This returns a JSON array of all unfiled articles with PDF children. Count the remaining unfiled articles and report the total.

### Step 2: Select One Article at Random
From the JSON results, select one article at random. Extract:
- `SOURCE_ZOTERO_ITEM_KEY`: the item's `key` field
- `SOURCE_AUTHOR_LASTNAME`: normalized first author's last name (lowercase, no spaces/punctuation)
- `SOURCE_YEAR`: publication year from `data.date` or "nd" if unavailable
- `SOURCE_APA_CITATION`: full APA citation constructed from Zotero metadata

Before proceeding, verify that no summary file already exists in `${SUMMARY_FOLDER}` matching this article's Zotero key.

### Step 3: Retrieve and Read the PDF
Locate the PDF in the article's Zotero children. Extract the PDF content using `pdftotext` or equivalent PDF parser. Read the entire article carefully, noting:
- Purpose, scope, and central arguments
- Methods and evidence type
- Participant context (library type, audience, setting)
- Game formats discussed
- Library services or outcomes described
- Limitations and cautions in the evidence

### Step 4: Classify Using Metadata Schema
Using `${METADATA_SCHEMA_FILE}` as your only source of controlled values, assign:
- `Source_Type`: one controlled value (e.g., peer_reviewed_journal_article, book, case_study, etc.)
- `Peer_Review`: controlled value from the schema
- `Evidence_Type`: controlled value matching the research approach
- `Primary_Methodology`: controlled value for the research method
- `Library_Context`: controlled value for the setting
- `Game_Format`: one or more controlled values
- `Service_Area`: one or more controlled values describing the library service
- `Audience`: controlled value if applicable
- `Intended_Outcome`: controlled value if applicable
- `Evidence_Confidence`: controlled value describing the strength and rigor of evidence claims (demonstrated_outcome, promising_evidence, practitioner_knowledge, descriptive_only, theoretical_or_conceptual, or not_applicable)
- `Service_Conditions_Addressed`: one or more controlled values identifying prerequisites or design principles discussed (access_infrastructure_required, skilled_facilitation_required, community_assessment_needed, sustainable_operations, inclusive_design_or_accessibility, evaluation_or_reflection, other, or not_applicable)
- `Conceptual_Theme`: one or more controlled values capturing theoretical or philosophical grounding (games_as_cultural_media, participatory_culture_and_production, game_literacy, service_ecology, conditional_benefits, information_behavior_and_practice, educational_psychology, social_equity_and_access, multiple_themes, or not_identified)
- `Coding_Confidence`: high, medium, or low (your assessment of classification certainty)

**Important**: Use ONLY values present in `${METADATA_SCHEMA_FILE}`. Do not invent new values. If no perfect match exists, select the closest defensible value and note the mismatch in the summary. If a source addresses a Service_Condition not covered by existing categories, assign "other" and document the condition in the "Productive Incongruences" section.

### Step 5: Write Summary File
Create filename: `${SOURCE_AUTHOR_LASTNAME}${SOURCE_YEAR}(${SOURCE_ZOTERO_ITEM_KEY}).md`

Write the summary in the article's own language and voice, approximately 500–800 words covering:
- What the article argues or reports
- Evidence, methods, and findings
- Relevance to games-based library services
- Any productive incongruences with the baseline review structure or metadata schema

Use this structure:

```
# ${SOURCE_APA_CITATION}

## Metadata
Citation_Key: [key]
Year: [year]
Zotero_Item_Key: [key]
Source_Type: [value]
Peer_Review: [value]
Evidence_Type: [value]
Primary_Methodology: [value]
Library_Context: [value]
Game_Format: [value or list]
Service_Area: [value or list]
Audience: [value]
Intended_Outcome: [value]
Evidence_Confidence: [value]
Service_Conditions_Addressed: [value or list]
Conceptual_Theme: [value or list]
Coding_Confidence: [confidence]

## Summary
[Prose summary in the article's own language, covering purpose, arguments, evidence, and relevance.]

## Productive Incongruences and Challenges
[Description of any mismatch with metadata schema, baseline structure, or review scope. Include here any Service_Condition assigned "other" value. Or state: "No substantial incongruence identified."]

## Suggested Review Contributions
[List contributions by Target_Section matching exact headings from ${BASELINE_FILE}. Include Contribution_Text with concise, review-ready prose. Or state: "No review contribution warranted."]
```

### Step 6: File in Zotero
After the summary file is written and verified:

1. Add the article to the "Summary Complete" collection in Zotero.
2. For each suggested review contribution, identify the corresponding collection in Zotero that matches the baseline structure section. Add the article to all applicable collections.
3. Preserve all existing collection memberships.

**Python code for adding collections:**

```python
import json
import requests

# Load credentials
with open("project-config.json") as f:
    config = json.load(f)

zotero_key = config["ZOTERO_API_KEY"]
group_id = 5899078
item_key = "87ZB9FSP"  # Replace with the article's Zotero key

# Collections to add
collection_keys = [
    "XDJU2DNT",  # Summary Complete (always add)
    "AA79VNPC",  # Example: Games as Cultural Media
    # Add more collection keys as needed from the mapping table
]

headers = {"Zotero-API-Key": zotero_key, "Content-Type": "application/json"}

# GET current item data
url = f"https://api.zotero.org/groups/{group_id}/items/{item_key}"
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Error fetching item: {response.status_code}")
    exit(1)

item_data = response.json()

# Add new collections while preserving existing ones
current_collections = item_data.get('data', {}).get('collections', [])
new_collections = list(set(current_collections + collection_keys))

# PATCH the item with updated collections
item_data['data']['collections'] = new_collections
response = requests.patch(url, json=item_data['data'], headers=headers)

if response.status_code in [200, 204]:
    print(f"Successfully added collections: {new_collections}")
else:
    print(f"Error updating item: {response.status_code}")
```

## READING AND CLASSIFICATION GUIDANCE

**Do not invent or distort.** Read the article's own claims, methods, and evidence. Classify based on what the article actually does, not what you wish it did. Use `medium` or `low` confidence for uncertain classifications.

**Best-guess metadata.** Use `${METADATA_SCHEMA_FILE}` as your guide. When an article does not fit perfectly, select the closest defensible value and document any mismatch in the "Productive Incongruences" section.

**Writing the summary:** Use the article's own voice and language to describe its arguments and evidence. Write approximately 500–800 words covering purpose, findings, and relevance to games-based library services. Distinguish:
- What the article claims or reports
- What the article actually found or measured
- Your synthesis for the GBLS project

When interpreting the article's relevance to GBLS, signal that shift explicitly: "For the larger GBLS project..." or "Read in relation to GBLS...".

**Identifying contributions.** Review the exact section headings in `${BASELINE_FILE}`. Match contributions to the most specific applicable section. Synthesize rather than quote the summary. If no section fits, propose a new section and explain why.

**Productive incongruences.** Describe any meaningful misalignment between the article and the metadata schema, baseline structure, or review scope. Examples:
- The article cannot be represented adequately by existing controlled values.
- The article supplies evidence that complicates a project assumption.
- The article addresses a gap in the baseline structure.

If no incongruence exists, state: "No substantial incongruence identified."

## PROTECTED DIRECTORIES

**Do not modify `${HUMAN_SOURCES_FOLDER}`.** This directory contains the authoritative metadata schema, baseline structure, and values framework. Read these files to inform your work; do not edit them.

## QUALITY VERIFICATION

Before completing the workflow:
- The summary file exists in `${SUMMARY_FOLDER}` with the correct naming pattern.
- The metadata uses only controlled values from `${METADATA_SCHEMA_FILE}`.
- The APA citation is complete and accurate (verify against the PDF title page if uncertain).
- No existing summary file for this article appears elsewhere in `${SUMMARY_FOLDER}`.
- Zotero collections have been updated to include "Summary Complete" and any section-specific collections.

## COMMON ISSUES AND SOLUTIONS

**Issue: "ModuleNotFoundError: No module named 'requests'"**
- Solution: Activate venv and install: `pip install requests`

**Issue: "Config file not found at project-config.json"**
- Solution: Ensure `project-config.json` exists in project root with ZOTERO_USER_ID and ZOTERO_API_KEY
- Example:
  ```json
  {
    "ZOTERO_USER_ID": "5357448",
    "ZOTERO_API_KEY": "xxxxxxxxxxxxxxxx"
  }
  ```

**Issue: "Error: 401 Unauthorized" when calling Zotero API**
- Solution: Check API key in project-config.json is correct (copy from Zotero account settings)

**Issue: "PDF cannot be extracted" or "pdftotext not found"**
- Solution: Install poppler-utils (contains pdftotext): `brew install poppler` (macOS) or `apt install poppler-utils` (Linux)

**Issue: "APA citation is incomplete" (missing title, author, or year)**
- Solution: Check Zotero item metadata. If title/author is missing in Zotero, manually edit the citation in the summary file's metadata section. Document this in "Productive Incongruences."

**Issue: "No collection found with name 'X in Zotero'"**
- Solution: Search the Zotero group web interface (https://www.zotero.org/groups/5899078) for the collection, copy its key from the URL, and add to the mapping table.

**Issue: "Article filename collision: a different article has the same author+year"**
- Solution: Check if the existing file is truly the same article (compare Zotero keys). If different, modify the author's last name (e.g., use middle initial: `smithj2020(KEY).md` instead of `smith2020(KEY).md`). Document in "Productive Incongruences."

**Issue: "Summary file exists but Zotero collections not updated"**
- Solution: The workflow is incomplete. Rerun the collection-filing Python code (Step 6). Then proceed to FINAL REPORT.

**Issue: "Metadata field value not in controlled vocabulary"**
- Solution: Do not invent values. Either:
  - Select the closest defensible value from the schema
  - If no match exists and none is close, assign `other` for Service_Conditions_Addressed, and document the missing value in "Productive Incongruences"
  - For other fields, use "not_applicable" or "unspecified_*" variant if available

## FINAL REPORT

Report on successful workflow completion:
- Article processed (author, year, Zotero key)
- Summary file created with full path
- Article moved from unfiled → filed status (collections assigned in Zotero)
- Remaining unfiled count (from the original tool output)

If the workflow encounters a blocking issue (e.g., PDF cannot be extracted, Zotero is locked, collection name cannot be found), stop, document the specific blocker, and report it without making partial changes. The article remains in unfiled status.
