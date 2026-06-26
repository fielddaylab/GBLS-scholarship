# Windleharth, T. W., Jett, J., Schmalz, M., & Lee, J. H. (2016). Full Steam Ahead: A Conceptual Analysis of User-Supplied Tags on Steam. Cataloging & Classification Quarterly, 54(7), 418–441.

# Objective Metadata

Citation_Key: windleharth2016
Year: 2016
Zotero_Item_Key: ZAX7YVFU
Better_BibTeX_Citation_Key: 
Attachment_Key: 

# Structured Extraction

## Purpose
The article aims to conduct a conceptual analysis of user-generated tags on the Steam video game distribution platform to identify gaps between user terminology and existing library metadata standards. Specifically, it seeks to compare these tags with the Video Game Metadata Schema (VGMS) developed by the GAMER Group to inform revisions and improvements to the schema for digitally distributed games.
Evidence: "The objective of our study is to compare user-contributed Steam tags with metadata elements in the Video Game Metadata Schema (VGMS)... to inform revisions to it." (Introduction)
Confidence: high

## Method
The researchers employed a conceptual analysis method, utilizing custom Ruby scripts to scrape all publicly accessible games on Steam via HTTP calls and XPath queries. The resulting dataset of user-generated tags was organized through a card-sorting activity using the Trello application. This process involved sorting 294 unique tags into categories to understand their context and usage, comparing them against existing VGMS elements.
Evidence: "The research team scraped all user-generated tags available on Steam and then conducted a conceptual analysis of the tags, sorting them into categories..." (Abstract); "We employed conceptual analysis as a guiding method for the card-sorting activity." (Study design and methods)
Confidence: high

## Population and Data
The data consists of 294 unique user-generated tags applied to 4,495 computer games available on the Steam platform. The dataset was collected on March 11, 2015. The population is limited to PC-based digital distribution titles; console, handheld, and mobile games are not represented.
Evidence: "From this data, a total of 294 unique tags were identified." (Study design and methods); "The final data set... contained a total of 294 tags, applied to the 4,495 games." (Data and discussion)
Confidence: high

## Findings
The analysis categorized tags into 29 distinct groups. Key findings include:
1. **Alignment with VGMS:** Most categories mapped closely to existing VGMS elements, particularly gameplay genre and narrative genre.
2. **New Elements Identified:** The study identified significant user interest in "Mechanics" (e.g., "Match 3," "6DOF"), "User Interactions" (e.g., input methods like "Mouse Only," multiplayer types like "Local Co-op"), and "Evaluation" (e.g., "Story Rich," "Experimental").
3. **Ambiguity:** Many tags were ambiguous or polysemous (e.g., "Abstract" could refer to genre, visual style, or theme), posing challenges for controlled vocabulary development.
4. **Granularity:** Users provided finer granularity than official categories, such as distinguishing between "Open World" (spatial freedom) and "Sandbox" (mechanical freedom).
Evidence: "Based on our analysis of Steam tags, we recommend adding three elements to the VGMS: Mechanics, User Interactions, and Evaluation." (Recommendations); "A total of 29 categories emerged from the conceptual analysis." (Data and discussion)
Confidence: high

## Implications
The authors recommend updating the VGMS to include new metadata elements for Mechanics, User Interactions, and Evaluation. They suggest that user tags serve as valuable "desire lines" that can refine formal taxonomies. The study highlights the need for linked data principles to manage term ambiguity and suggests future research should explore cross-cultural tagging behaviors and additional sources beyond Steam.
Evidence: "Based on our analysis of Steam tags, we recommend adding three elements to the VGMS..." (Recommendations); "In our work, we aim for the third approach, seeking to identify the desire lines through analysis of user-generated tags to help us make decisions regarding changes to the VGMS." (Background and related work)
Confidence: high

# Summary

This article presents a conceptual analysis of user-generated tags on Steam, a major digital distribution platform for video games, with the goal of refining the Video Game Metadata Schema (VGMS). The authors argue that while video game consumption is growing rapidly, existing metadata systems often fail to capture the specific terminology and descriptors users employ when searching for or describing games. By analyzing user-contributed tags, the study aims to bridge the gap between user vernacular and formal library cataloging practices.

The methodology involved scraping data from Steam on March 11, 2015, using custom Ruby scripts. The dataset comprised 4,495 PC-based video games and 294 unique user-generated tags. These tags were subjected to a conceptual analysis via a card-sorting activity conducted in Trello, allowing the researchers to categorize terms and interpret their contextual meanings. A primary limitation acknowledged by the authors is that the data reflects only PC games available on Steam, excluding console, handheld, and mobile titles, which may possess unique tagging behaviors. Additionally, Steam’s filtering of inappropriate content means some user perspectives are absent from the dataset.

The analysis resulted in 29 categories of tags. The majority aligned with existing VGMS elements, particularly gameplay genre (the most common category) and narrative genre. However, the study identified significant areas where user terminology diverged from or expanded upon the current schema. Notably, users frequently tagged games based on specific mechanics (e.g., "Match 3," "6DOF"), which are not currently a distinct element in the VGMS. The authors also found strong evidence for categorizing "User Interactions," encompassing input methods (e.g., "Mouse Only") and multiplayer dynamics (e.g., "Local Co-op," "PvP"). Furthermore, evaluative terms such as "Story Rich" or "Experimental" were prevalent, suggesting a need for an "Evaluation" element to capture user judgments on replay value and novelty.

The authors highlight significant challenges in organizing these tags, primarily due to ambiguity. Many terms, such as "Abstract" or "America," carried multiple meanings depending on context (e.g., genre, theme, setting), complicating their integration into controlled vocabularies. The study also noted that users often distinguished between concepts currently conflated in the VGMS, such as separating "Open World" (spatial freedom) from "Sandbox" (mechanical creativity).

In conclusion, the authors recommend adding Mechanics, User Interactions, and Evaluation as new elements to the VGMS. They advocate for adopting linked data principles to manage term ambiguity and improve information retrieval systems. The study positions user tags not as replacements for professional cataloging but as complementary "desire lines" that reveal user priorities, thereby enhancing the accessibility and relevance of video game metadata in library and archival contexts.

# Subjective Metadata

Coded_By: Qwen3-14B-AWQ
Version: 1.0

## Source_Type
Value: peer_reviewed_journal_article
Confidence: high
Evidence: "Cataloging & Classification Quarterly, ISSN: 0163-9374 (Print) 1544-4554 (Online) Journal homepage: http://www.tandfonline.com/loi/wccq20"
Reason_For: The article is published in a scholarly journal and includes peer review information.
Reason_Against: none

## Evidence_Type
Value:
- empirical_study
Confidence: high
Evidence: "The research team scraped all user-generated tags available on Steam and then conducted a conceptual analysis of the tags, sorting them into categories..."
Reason_For: The study involved collecting and analyzing user-generated tags from Steam, which is an empirical study.
Reason_Against: none

## Primary_Methodology
Value: content_analysis
Confidence: high
Evidence: "The research team scraped all user-generated tags available on Steam and then conducted a conceptual analysis of the tags, sorting them into categories..."
Reason_For: The study involved a conceptual analysis of user-generated tags.
Reason_Against: none

## Library_Context
Value: non_library_context
Confidence: high
Evidence: "Steam is one of the most popular online digital game distribution platforms."
Reason_For: The study focuses on Steam, a digital game distribution platform, which is not a library or library-related context.
Reason_Against: none

## Game_Format
Value:
- digital_game
Confidence: high
Evidence: "Steam is one of the most popular online digital game distribution platforms."
Reason_For: The study focuses on digital games distributed through Steam.
Reason_Against: none

## Service_Area
Value:
- cultural_heritage_and_research
Confidence: medium
Evidence: "The study is one effort to reduce that gap—to help researchers understand the tags and terms game users ﬁnd useful—in an effort to inform game metadata systems."
Reason_For: The study contributes to the understanding of game metadata, which can be related to cultural heritage and research.
Reason_Against: The primary focus is on metadata systems rather than cultural heritage or research.

## Audience
Value: not_applicable
Confidence: low
Evidence: "The study is one effort to reduce that gap—to help researchers understand the tags and terms game users ﬁnd useful—in an effort to inform game metadata systems."
Reason_For: The study focuses on researchers and metadata systems rather than a specific audience.
Reason_Against: The article does not clearly identify a specific audience for the service or intervention.

## Intended_Outcome
Value: other
Confidence: low
Evidence: "The study is one effort to reduce that gap—to help researchers understand the tags and terms game users ﬁnd useful—in an effort to inform game metadata systems."
Reason_For: The intended outcome is to inform game metadata systems, which is not clearly categorized in the schema.
Reason_Against: The outcome is not clearly aligned with the predefined categories.

## Evidence_Confidence
Value: demonstrated_outcome
Confidence: high
Evidence: "Based on our analysis of Steam tags, we recommend adding three elements to the VGMS: Mechanics, User Interactions, and Evaluation."
Reason_For: The study presents specific recommendations based on the analysis, indicating a demonstrated outcome.
Reason_Against: none

## Service_Conditions_Addressed
Value:
- access_infrastructure_required
Confidence: low
Evidence: "The key limitation of this data source is that any tags that might be uniquely relevant to mobile, handheld, or console games might not be represented in this study."
Reason_For: The study acknowledges limitations in the data source, which could be related to access infrastructure.
Reason_Against: The study does not explicitly discuss access infrastructure requirements.

## Conceptual_Theme
Value:
- information_behavior_and_practice
Confidence: high
Evidence: "User tags represent both opportunities and challenges for catalogers."
Reason_For: The study focuses on how users interact with information through tagging, which is related to information behavior and practice.
Reason_Against: none

## Coding_Confidence
Value: medium

# Potential Contributions to Review

## Conceptual Terrain: Games, Play, and Library Service
Contribution_Text: This article contributes to the conceptual terrain by examining how user-generated tags on Steam can inform and enhance library metadata systems for video games. It highlights the importance of aligning user terminology with formal metadata schemas to improve information retrieval and access.

## Game Modalities in Library Contexts
Contribution_Text: The study provides insights into the modalities of digital games and their representation in metadata systems, which is relevant to how libraries can integrate and manage digital game collections.

## Analog, Digital, and Hybrid Affordances
Contribution_Text: The article discusses the affordances of digital game metadata and the challenges of representing user-generated tags, which can inform the design of hybrid metadata systems that combine user and professional perspectives.

## Libraries as Playful Spaces and Service Environments
Contribution_Text: While the study does not directly address libraries as playful spaces, it contributes to the understanding of how game metadata can be structured to support playful and interactive library services.

## Research, Scholarship, and Creative Production
Contribution_Text: The study contributes to the field of research and scholarship by providing a framework for analyzing user-generated metadata and its potential applications in library and information science.

## Cross-Cutting Conditions for Effective Games-Based Library Services
Contribution_Text: The article highlights the importance of considering user-generated metadata and the challenges of aligning it with formal metadata schemas, which is a cross-cutting condition for effective games-based library services.

## Productive Incongruences
No substantial incongruence identified.

# Audit Provenance

Audited: [yes | no]
Audited_By: [paid model name, or "not audited"]
Audit_Action: [confirmed | revised classifications | revised summary | flagged | not audited]
Audit_Notes: [what the auditor checked or changed, or "n/a"]
Sampled_For_Quality: [yes | no]
