# McCulloch, A. (2017). Cataloguing and classifying board and tabletop games.

# Objective Metadata

Citation_Key: mcculloch2017
Year: 2017
Zotero_Item_Key: 7CQMGTW5
Better_BibTeX_Citation_Key: 
Attachment_Key: 

# Structured Extraction

## Purpose
The article aims to demonstrate how library cataloguers and metadata staff can include board and tabletop games in their library’s catalogue by creating machine-readable cataloguing (MARC) records. It focuses on specific fields and terminologies that differ from standard items like books or serials, using the game *Settlers of Catan* as a primary example to illustrate best practices for fixed fields, access points, descriptive cataloguing, subject indexing, and classification.
Evidence: "This article will demonstrate how cataloguers and metadata staff can include these games in their library’s catalogue, by creating machinereadable cataloguing (MARC) records using particular fields and terminologies."
Confidence: high

## Method
The article employs a descriptive instructional approach based on professional practice and existing standards (RDA, MARC21). It does not present empirical data collection or statistical analysis. Instead, it provides a technical guide with specific examples of MARC field usage, drawing on the author's blog post and referencing other industry guidelines such as those from OLAC and UW/SIMM.
Evidence: "This article is based on a post on my blog Cataloguing the Universe... The example MARC fields in this article describe the classic 1980s tabletop game Settlers of Catan."
Confidence: high

## Population and Data
Not applicable. The text does not study a human population or collect empirical data. It analyzes a single artifact (*Settlers of Catan*) as a case study for metadata creation and references general industry trends regarding the underrepresentation of board games in union catalogues.
Evidence: "Slobuski et al. (2017) review the slim pickings... they note that the paucity of records in union catalogues such as OCLC... mean that board games are underrepresented in library catalogues."
Confidence: high

## Findings
The article identifies several key technical findings and recommendations for cataloguing board games:
1.  **Fixed Fields:** Board games should generally be coded with Leader/06 as 'r' (realia/three-dimensional artifact) and Leader/07 as 'm' (monograph/item). The 008 fixed field should use Visual Materials specifications, specifically coding position 33 as 'g' for game.
2.  **Access Points:** Most games are entered under title, but if a creator is prominent (e.g., Klaus Teuber), a 100 Main Entry--Personal Name is appropriate. A 710 Added Entry--Corporate Name for the publisher is recommended due to user search behaviors.
3.  **Descriptive Cataloguing:** The 300 Physical Description field requires detailed piece inventory (e.g., specific counts of cards, tokens, boards) rather than generic descriptions. Key metadata such as player count and duration are currently relegated to uncontrolled 500 General Notes, which limits faceted search capabilities in Integrated Library Systems (ILS).
4.  **Content/Media/Carrier:** The recommended combination is 336 'three-dimensional form', 337 'unmediated', and 338 'object'.
5.  **Subject Indexing:** The 655 Genre/Form field should use Library of Congress Genre/Form Terms (LCGFT) such as "Board games" or "Puzzles and games." The author notes a lack of appropriate form subdivisions in subject headings, proposing the need for a "$v Games" subdivision.
6.  **Classification:** Libraries may choose to shelve games separately (alphabetically) or interfile them using DDC (794) or LCC (GV1312-1469 for board games).
Evidence: "Leader/06 Type of Record is ‘r’ for realia... Leader/07 Bibliographic Level is ‘m’ for monograph/item." / "A 500 note really isn’t ideal for our purposes, as having this kind of data in uncontrolled fields and with uncontrolled vocabulary limits the ability of an ILS developer to create facet searches based on that data."
Confidence: high

## Implications
The article implies that current MARC standards are not optimally designed for board games, leading to suboptimal discoverability. The reliance on uncontrolled fields (500 notes) for critical metadata like player count and duration hinders advanced search functionalities. The author suggests that a dedicated metadata schema for board games, potentially building upon the UW/SIMM Video Game Metadata Schema, would be beneficial. Furthermore, the article highlights the need for innovation in subject heading subdivisions to better distinguish tabletop games from computer games or general topics. Ultimately, proper cataloguing is essential for making these non-traditional items discoverable and accessible to patrons, supporting library efforts to diversify collections.
Evidence: "MARC was patently not designed with board games in mind. However, a dedicated metadata schema for board games could be very useful." / "Board games can be complex works to catalogue, but the result – making games discoverable and accessible to patrons – is hugely rewarding."
Confidence: high

# Summary

Alissa McCulloch’s 2017 article, "Cataloguing and classifying board and tabletop games," serves as a technical guide for library professionals seeking to integrate board and tabletop games into their collections. As libraries increasingly diversify their holdings to include non-traditional items for historical, pedagogical, or recreational value, the accurate cataloguing of these materials becomes essential for patron access. The article addresses the scarcity of scholarly literature on this specific topic, noting that most existing guidance pertains to video games rather than physical tabletop games. It draws upon the author’s prior work and industry standards, including RDA and MARC21, to provide a comprehensive framework for creating machine-readable records.

The methodology is instructional rather than empirical, utilizing the classic game *Settlers of Catan* as a case study to illustrate specific field applications. McCulloch begins by addressing fixed fields, recommending that board games be coded with Leader/06 as 'r' (realia/three-dimensional artifact) and Leader/07 as 'm' (monograph/item). The 008 fixed field should utilize Visual Materials specifications, specifically marking the type of visual material as 'g' for game. While ISBNs are rare, they should be recorded in field 020 if present; publisher-specific catalogue numbers belong in field 028.

Regarding access points, the article notes that while most games are entered under title, prominent designers like Klaus Teuber may warrant a 100 Main Entry--Personal Name. A 710 Added Entry--Corporate Name for the publisher is strongly recommended, as users frequently search by publisher name. In descriptive cataloguing (field 300), McCulloch advocates for exhaustive physical inventories of game components (e.g., specific counts of terrain hexes, cards, and tokens) to aid in loss prevention and identification. A significant limitation identified is the placement of critical metadata—such as player count and duration of play—in uncontrolled 500 General Notes. This practice restricts the ability of Integrated Library Systems (ILS) to generate faceted searches based on these attributes, highlighting a gap in current MARC standards.

For content, media, and carrier types, the article recommends using 'three-dimensional form' (336), 'unmediated' (337), and 'object' (338). Subject indexing relies heavily on the 655 Genre/Form field, utilizing Library of Congress Genre/Form Terms (LCGFT) such as "Board games" or "Puzzles and games." McCulloch points out the inadequacy of existing subject heading subdivisions for tabletop games, noting that the topical subdivision "$x Games" is invalid for this format and "$v Computer games" is inapplicable. She proposes the creation of a form subdivision "$v Games" to improve precision.

Finally, the article discusses classification options. Libraries may choose to shelve games separately in an alphabetical "Board games" section or interfile them using Dewey Decimal Classification (794) or Library of Congress Classification (GV1312-1469). The conclusion emphasizes that while board games present complex cataloguing challenges, accurate metadata creation is vital for discoverability. McCulloch encourages cataloguers to tailor records to their specific ILS capabilities and suggests that future innovation in metadata schemas could better serve this growing collection type.

# Subjective Metadata

Coded_By: Qwen3-14B-AWQ
Version: 1.0

## Source_Type
Value: professional_publication
Confidence: high
Evidence: "This article is based on a post on my blog Cataloguing the Universe..."
Reason_For: The article is published as a blog post and is intended for professional library practitioners, not for scholarly peer review.
Reason_Against: none

## Peer_Review
Value: no
Confidence: high
Evidence: "This article is based on a post on my blog Cataloguing the Universe..."
Reason_For: The source is a blog post and not a peer-reviewed article.
Reason_Against: none

## Evidence_Type
Value:
- practitioner_reflection
Confidence: high
Evidence: "This article is based on a post on my blog Cataloguing the Universe..."
Reason_For: The article provides practical guidance for cataloging board games, based on the author's experience and industry standards.
Reason_Against: none

## Primary_Methodology
Value: none
Confidence: high
Evidence: "This article is based on a post on my blog Cataloguing the Universe..."
Reason_For: The article is not based on empirical research or analysis but provides descriptive, instructional content.
Reason_Against: none

## Library_Context
Value: academic_library
Confidence: medium
Evidence: "In many institutions, board and tabletop games are a growing part of a library’s collection."
Reason_For: The article discusses practices relevant to academic libraries, though it does not explicitly specify the library type.
Reason_Against: The source does not clearly identify a specific library type, such as academic, public, or school.

## Game_Format
Value:
- tabletop_game
Confidence: high
Evidence: "The example MARC fields in this article describe the classic 1980s tabletop game Settlers of Catan."
Reason_For: The article focuses on cataloging tabletop games.
Reason_Against: none

## Service_Area
Value:
- collections_and_access
Confidence: high
Evidence: "This article will demonstrate how cataloguers and metadata staff can include these games in their library’s catalogue..."
Reason_For: The article focuses on cataloging and access to board games in library collections.
Reason_Against: none

## Audience
Value: general_public
Confidence: medium
Evidence: "With libraries diversifying their collections to appeal to a broader cross-section of their user base..."
Reason_For: The article suggests that board games are intended for a general audience.
Reason_Against: The source does not explicitly identify the audience for the games being cataloged.

## Intended_Outcome
Value: equitable_access
Confidence: high
Evidence: "making games discoverable and accessible to patrons"
Reason_For: The article emphasizes the importance of making board games discoverable and accessible to patrons.
Reason_Against: none

## Evidence_Confidence
Value: practitioner_knowledge
Confidence: high
Evidence: "This article is based on a post on my blog Cataloguing the Universe..."
Reason_For: The article is based on the author's professional experience and industry standards.
Reason_Against: none

## Service_Conditions_Addressed
Value:
- access_infrastructure_required
Confidence: medium
Evidence: "MARC was patently not designed with board games in mind."
Reason_For: The article discusses the need for appropriate metadata infrastructure to support the cataloging of board games.
Reason_Against: The source does not explicitly discuss material barriers such as hardware or space.

## Conceptual_Theme
Value:
- games_as_cultural_media
Confidence: medium
Evidence: "board and tabletop games are collected for historical, pedagogical or recreational value"
Reason_For: The article discusses the cultural and educational value of board games.
Reason_Against: The source does not explicitly foreground a theoretical or conceptual framework.

## Coding_Confidence
Value: high

# Potential Contributions to Review

## Collections, Circulation, and Equitable Access
Contribution_Text: This article provides detailed guidance on cataloging board and tabletop games using MARC records, emphasizing the need for specific fields and terminologies to ensure these items are discoverable and accessible to patrons. It highlights the limitations of current MARC standards for board games and suggests potential improvements.

## Description, Discovery, and Games Advisory
Contribution_Text: The article outlines best practices for creating machine-readable cataloging records for board games, including the use of specific MARC fields for access points, descriptive cataloging, and subject indexing. This contributes to the review by offering practical strategies for improving the discoverability of games in library collections.

## Challenges to Cataloging Games
Contribution_Text: The article identifies key challenges in cataloging board games, such as the lack of appropriate subject heading subdivisions and the placement of critical metadata in uncontrolled fields. These insights are valuable for understanding the current limitations in library cataloging practices for games.

## Game Modalities in Library Contexts
Contribution_Text: The article discusses the specific needs of cataloging tabletop games, which are distinct from digital games. It provides a detailed case study of *Settlers of Catan* and offers practical recommendations for integrating these games into library collections.

## Analog, Digital, and Hybrid Affordances
Contribution_Text: The article focuses on the cataloging of analog (tabletop) games and highlights the differences in metadata requirements compared to digital games. This contributes to the review by addressing the unique affordances and challenges of analog game formats in library contexts.

## Cross-Cutting Conditions for Effective Games-Based Library Services
Contribution_Text: The article emphasizes the importance of proper cataloging and metadata practices as a cross-cutting condition for effective games-based library services. It argues that without appropriate metadata, games may not be discoverable or accessible to patrons, limiting their impact.

## Productive Incongruences
No substantial incongruence identified.

# Audit Provenance

Audited: [yes | no]
Audited_By: [paid model name, or "not audited"]
Audit_Action: [confirmed | revised classifications | revised summary | flagged | not audited]
Audit_Notes: [what the auditor checked or changed, or "n/a"]
Sampled_For_Quality: [yes | no]
