# Robson, Diane, Catherine Sassen, Jason Thomale, and Kevin Yanowski. "Enhancing the Discovery of Tabletop Games." *Library Resources & Technical Services* 63, no. 3 (July 2019): 199–214.

# Objective Metadata

Citation_Key: robson2019
Year: 2019
Zotero_Item_Key: 53WHCDML
Better_BibTeX_Citation_Key: 
Attachment_Key: 

# Structured Extraction

## Purpose
The article aims to document the strategies employed by librarians at the University of North Texas (UNT) Libraries to enhance the discovery and access of a collection of over 600 tabletop games. The authors argue that three-dimensional materials are often poorly discoverable due to inadequate metadata and lack of cataloging standards. The paper outlines how applying relevant cataloging standards (RDA), developing local genre terms, and implementing custom faceted search capabilities in a Blacklight/Solr discovery layer can improve user access.
Evidence: "This paper outlines how librarians at the University of North Texas Libraries used these strategies to increase access to a large collection of tabletop games." (p. 199)
Confidence: high

## Method
The study is a descriptive case study and technical implementation report. It details the workflow for cataloging tabletop games according to Resource Description and Access (RDA) standards, the development of a local controlled vocabulary of genre terms, and the technical configuration of Apache Solr and Blacklight to support custom facets based on game-specific metadata (duration, player count, age). The authors describe the collaboration between catalogers, systems librarians, and IT staff.
Evidence: "This paper documents the collective effort required at the authors’ institution to enhance access to their tabletop game collection." (p. 200); "The authors implemented the tabletop game record enhancements as custom Blacklight facets." (p. 199)
Confidence: high

## Population and Data
The primary data consists of the UNT Media Library’s collection of over 600 tabletop games, including board games, dice games, collectible card games, and role-playing games. The authors also reference a literature review of cataloging practices and user studies regarding faceted navigation. No empirical user testing or statistical analysis of search behavior was conducted as part of this specific report; the findings are based on the successful implementation of the system in a prerelease version.
Evidence: "This paper focuses on the library’s collection of over six hundred tabletop games..." (p. 199); "Although that system was still under development at the time of writing, the Libraries’ programmers built and deployed the described enhancements in a working, prerelease version." (p. 199)
Confidence: high

## Findings
The authors found that improving access to three-dimensional collections requires close collaboration between catalogers and technologists. They successfully created a local genre term list of 50 terms derived from Board Game Geek and tailored to UNT’s collection needs. They developed a coding system for game-specific attributes (duration, number of players, age) stored in MARC field 590. These codes were indexed into Solr as string fields and configured in Blacklight to display human-readable facet labels. The implementation allowed users to filter search results by these specific game characteristics. The authors note that while faceted navigation is generally helpful, terminology clarity and interface design are critical for usability.
Evidence: "Through their efforts, the authors learned that improving access to collections via discovery interfaces requires close collaboration between catalogers, technologists, and systems librarians." (p. 200); "The authors created a set of fifty genre terms in an open access resource entitled Genre Terms for Tabletop Games." (p. 207)
Confidence: high

## Implications
The article implies that libraries with specialized non-book collections should consider local enhancements to metadata and discovery interfaces to improve usability. It highlights the necessity of organizational structures that facilitate collaboration between cataloging and IT departments. The authors suggest that while not all libraries have the resources for custom development, the principles of enhanced metadata and faceted search are broadly applicable. They emphasize that uncataloged or minimally cataloged collections remain hidden from users, violating Ranganathan’s first law of library science.
Evidence: "If a library values providing its users with systems and services tailored to their needs, it must find vendors willing to provide that level of customization or it must provide explicit organizational support for performing and maintaining in-house customization." (p. 211)
Confidence: high

# Summary

This article by Robson, Sassen, Thomale, and Yanowski presents a case study from the University of North Texas (UNT) Libraries regarding the enhancement of discovery tools for a collection of over 600 tabletop games. The authors identify a broader problem in library science: three-dimensional materials are often poorly cataloged or left uncataloged due to perceived complexity and a lack of standardized guidance, rendering them invisible to users in digital catalogs. To address this, UNT librarians implemented a multi-faceted approach involving rigorous descriptive cataloging, the creation of local genre terms, and the technical customization of their discovery layer.

The methodology begins with adherence to Resource Description and Access (RDA) standards for creating core bibliographic records. The authors detail specific MARC field applications for tabletop games, including recording identifiers (ISBN/UPC), physical descriptions (carrier type, extent, dimensions), and access points for designers and publishers. They emphasize that while RDA provides a baseline, local enhancements are necessary for optimal discovery. Consequently, the team developed a controlled vocabulary of 50 genre terms specific to tabletop games, drawing from the crowd-sourced database Board Game Geek but tailored to reflect both novice and expert terminology. These terms were assigned as authorized access points in MARC field 655.

A significant portion of the article focuses on the implementation of faceted search capabilities. Recognizing that standard metadata fields did not capture key user decision factors—specifically duration of play, number of players, and recommended age—the authors created a custom coding system. These attributes were encoded into MARC field 590 (Local Note) using standardized tokens (e.g., "d30t59" for 30-59 minutes). This data was then indexed into Apache Solr, an open-source search engine, where the codes were mapped to human-readable labels. The Blacklight discovery interface was configured to present these as filterable facets, allowing users to narrow search results by game characteristics.

The authors highlight that this technical achievement relied heavily on interdisciplinary collaboration between catalogers, systems librarians, and IT staff. They argue that catalogers must understand technological constraints to create useful metadata, while technologists must understand metadata structures to build effective interfaces. The article notes that the system was deployed in a prerelease version at the time of writing, so empirical user data on search success rates is not provided. However, the authors assert that the implementation successfully addressed the discoverability issues inherent in three-dimensional collections.

The implications for games-based library services are significant. The study demonstrates that effective access to game collections requires more than mere acquisition; it demands robust metadata strategies and discovery interface customization. The authors caution that such customizations require sustained institutional support and resources, which may not be available to all libraries. Nevertheless, they advocate for the principle of enhancing metadata to meet user needs, suggesting that even libraries without custom development capabilities can benefit from improved cataloging practices and genre term assignments. The article serves as a technical guide for other institutions seeking to improve access to non-traditional library materials through integrated cataloging and systems work.

# Subjective Metadata

Coded_By: Qwen3-14B-AWQ
Version: 1.0

## Source_Type
Value: peer_reviewed_journal_article
Confidence: high
Evidence: "Library Resources & Technical Services" is a peer-reviewed journal.
Reason_For: The article is published in a peer-reviewed journal.
Reason_Against: none

## Evidence_Type
Value:
- empirical_study
Confidence: medium
Evidence: The authors implemented the tabletop game record enhancements as custom Blacklight facets.
Reason_For: The study describes a specific implementation and its outcomes.
Reason_Against: The study does not include empirical user testing or statistical analysis of search behavior.

## Primary_Methodology
Value: case_or_design_study
Confidence: high
Evidence: This paper documents the collective effort required at the authors’ institution to enhance access to their tabletop game collection.
Reason_For: The study is a descriptive case study and technical implementation report.
Reason_Against: none

## Library_Context
Value: academic_library
Confidence: high
Evidence: The University of North Texas is the largest public university in the Dallas-Fort Worth area.
Reason_For: The study is conducted at an academic library.
Reason_Against: none

## Game_Format
Value:
- tabletop_game
Confidence: high
Evidence: The paper focuses on the library’s collection of over six hundred tabletop games.
Reason_For: The study is about tabletop games.
Reason_Against: none

## Service_Area
Value:
- collections_and_access
- discovery_and_advisory
Confidence: high
Evidence: The authors implemented the tabletop game record enhancements as custom Blacklight facets.
Reason_For: The study is about improving access to collections and discovery.
Reason_Against: none

## Audience
Value: general_public
Confidence: medium
Evidence: The study is about improving access to collections for all users.
Reason_For: The study is about improving access to collections for all users.
Reason_Against: The specific audience is not clearly identified.

## Intended_Outcome
Value: equitable_access
Confidence: high
Evidence: The authors implemented the tabletop game record enhancements as custom Blacklight facets.
Reason_For: The study is about improving access to collections.
Reason_Against: none

## Evidence_Confidence
Value: descriptive_only
Confidence: medium
Evidence: The system was deployed in a prerelease version at the time of writing, so empirical user data on search success rates is not provided.
Reason_For: The study is a descriptive case study and technical implementation report.
Reason_Against: The study does not include empirical user testing or statistical analysis of search behavior.

## Service_Conditions_Addressed
Value:
- access_infrastructure_required
- skilled_facilitation_required
Confidence: high
Evidence: The authors learned that improving access to collections via discovery interfaces requires close collaboration between catalogers, technologists, and systems librarians.
Reason_For: The study is about improving access to collections and the need for skilled facilitation.
Reason_Against: none

## Conceptual_Theme
Value:
- games_as_cultural_media
- service_ecology
Confidence: medium
Evidence: The study is about improving access to collections and the need for skilled facilitation.
Reason_For: The study is about improving access to collections and the need for skilled facilitation.
Reason_Against: The conceptual themes are not clearly identified.

## Coding_Confidence
Value: medium

# Potential Contributions to Review

## Collections, Circulation, and Equitable Access
Contribution_Text: This article provides a detailed case study on how to improve the discoverability of tabletop games in academic libraries through the application of relevant cataloging standards and controlled vocabularies. The authors describe the implementation of custom Blacklight facets to allow filtering based on game-specific metadata, which can be a valuable resource for other libraries looking to enhance access to their non-traditional collections.

## Discovery_and_advisory
Contribution_Text: The article outlines strategies for enhancing the discovery of tabletop games through the use of genre terms and faceted search capabilities. This can inform the development of discovery interfaces in libraries that aim to improve user access to non-traditional materials.

## Service_ecology
Contribution_Text: The study emphasizes the importance of collaboration between catalogers, technologists, and systems librarians to improve access to collections. This highlights the need for a service ecology that supports the integration of metadata and discovery systems to enhance user experience.

## Productive Incongruences
No substantial incongruence identified.

# Audit Provenance

Audited: [yes | no]
Audited_By: [paid model name, or "not audited"]
Audit_Action: [confirmed | revised classifications | revised summary | flagged | not audited]
Audit_Notes: [what the auditor checked or changed, or "n/a"]
Sampled_For_Quality: [yes | no]
