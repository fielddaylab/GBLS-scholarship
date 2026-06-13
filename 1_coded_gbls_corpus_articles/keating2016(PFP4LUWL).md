## 108. Keating, S. A. (2016). Organizing videogame metadata in CollectiveAccess. In *iConference 2016 Proceedings*. iSchools. https://doi.org/10.9776/16479

### Metadata
Citation_Key: keatingOrganizingVideogameMetadata2016
Year: 2016
Zotero_Item_Key: PFP4LUWL
Better_BibTeX_Citation_Key: keatingOrganizingVideogameMetadata2016
Attachment_Key: PPI57EKM

Source_Type: conference_paper
Peer_Review: editorial_reviewed
Evidence_Type:
- implementation_case
- instrument_or_framework_development
Primary_Methodology: case_or_design_study
Library_Context: cultural_heritage_institution
Game_Format: digital_game

Service_Area: collections_and_access
Audience: not_applicable

Intended_Outcome:
- discovery_and_advisory
- cultural_stewardship_and_preservation
- creativity_and_production
Coding_Confidence: high

### Contributions
- Target_Section: Major Areas of Game-Based Library Service > Cataloging, Metadata, and Discovery
  Contribution_Text: Keating (2016) turns the GAMER Group's relationship metadata into an
    implementation test by attempting to represent VGMS in CollectiveAccess. The case shows that
    open-source collection systems may support flexible element labels and granular schemas while
    still failing at game-specific discovery when relationships are fixed, hierarchical, difficult
    to modify without code, or not linkable to other relationships; for GBLS, that makes platform
    data models and search reactivity part of collection access, not merely back-end technical
    detail.
### Summary
# **Keating, S. A. (2016). Organizing videogame metadata in CollectiveAccess. In *iConference 2016 Proceedings*. iSchools. https://doi.org/10.9776/16479**

Keating examines whether CollectiveAccess, an open-source collection management system used by museums and cultural heritage organizations, can represent the complex metadata needs of video game collections. The paper is a short iConference poster, but it is directly relevant to the GBLS review because it turns the GAMER Group's Video Game Metadata Schema (VGMS) from a conceptual schema into an implementation problem. The core question is practical: can off-the-shelf digital collection software support specialized digital cultural heritage collections with complex attributes and relationships, or do game collections require more customized infrastructure?

The case study begins from the appeal of CollectiveAccess. CA was designed for special collections, has been praised by cultural heritage professionals, supports granular metadata, and lets administrators create and modify metadata schemas. Those features made it a plausible candidate for representing VGMS, which was created to describe video games and interactive media more fully than ordinary bibliographic systems. Keating evaluates CA through two sets of concerns: whether it can manage the special collection schema and relationships required by VGMS, and whether its design is usable enough for administrators and end users.

The implementation produced mixed results. CA made some metadata-management work easy. Changing element codes or labels was trivial, and the system propagated those changes throughout the site in an intuitive and visually understandable way. This matters for GBLS because game collections need flexible description: platforms, genres, versions, visual styles, relationships, hardware requirements, and distribution models often change or require local adaptation. A system that allows elements to be reordered, added, removed, and presented clearly is valuable for small institutions that cannot build custom software from scratch.

The major problem was relationship modeling. VGMS depends on relationships among games and related entities: series, franchises, universes, versions, ports, remakes, sequels, inspirations, downloadable content, and other connections that do not fit neatly into one hierarchy. Keating found that CollectiveAccess allowed some creation and contextualization of relationships, but top-level relationships were established by the system from the outset and could not be modified without code-level changes. Relationships were organized hierarchically, while the VGMS needed non-hierarchical and relationship-to-relationship linking. In Keating's conclusion, the inability to connect relationships to one another ultimately made CA insufficient for the GAMER Group's needs.

Keating also evaluates CA through modularity and reactivity. Drawing on design criteria from Norman and Bates, the paper argues that complex systems need modular interfaces and responsive user interaction. CA offered high-level modular features, but the VGMS implementation needed lower-level relationship functionality that was not exposed through the same easy interface. In the Pawtucket front end, search behavior was also frustrating because the system obscured how it performed searches; even known-item searches could be difficult. For end users, this weak reactivity would undermine discovery even if the metadata schema were theoretically rich.

For the larger GBLS project, Keating's contribution is infrastructural. Game-based library services depend not only on programs, collections, and events, but also on whether games and related cultural objects can be described, related, searched, and retrieved. A game collection that cannot distinguish versions, platforms, related works, relationship types, or complex series/franchise structures will be less useful for players, researchers, preservationists, educators, and creators. Keating therefore complements Lee, Clarke, Sacchi, and Jett's relationship metadata work and the later Keating et al. visual-style study: the former shows what relationships game metadata needs, the latter shows what descriptive facets users may require, and this poster shows how a real open-source platform strains when asked to implement those requirements.

The source also offers a useful caution for libraries considering open-source collection tools. Open source and schema flexibility are not enough. A platform must expose the right levels of control, model non-hierarchical relationships, make relationship creation understandable to administrators, and provide reactive search interfaces for end users. Otherwise, a system can appear customizable while still failing at the exact structures that make game metadata distinctive.

The limitations are significant. This is a poster paper, not a full implementation study or user evaluation. It does not report a large dataset, live public catalog, usability testing with patrons, or long-term maintenance outcomes. Still, it belongs in the review because it captures an early implementation test of video game metadata infrastructure and names a concrete barrier that matters for GBLS: game discovery is limited by the data models and interfaces available to local institutions.
