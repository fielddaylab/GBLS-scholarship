## 169. Robson, D., Sassen, C., Thomale, J., & Yanowski, K. (2019). Enhancing the discovery of tabletop games. *Library Resources & Technical Services, 63*(3), 199-215. https://doi.org/10.5860/lrts.63n3.199

### Metadata
Citation_Key: robsonEnhancingDiscoveryTabletop2019
Year: 2019
Zotero_Item_Key: 53WHCDML
Better_BibTeX_Citation_Key: robsonEnhancingDiscoveryTabletop2019
Attachment_Key: CPAW4VPK

Source_Type: peer_reviewed_journal_article
Peer_Review: peer_reviewed
Evidence_Type: implementation_case
Primary_Methodology: case_or_design_study
Library_Context: unspecified_library_context
Game_Format: tabletop_game

Service_Area: collections_and_access
Audience: not_applicable

Intended_Outcome: discovery_and_advisory
Coding_Confidence: high

Contributions:
- Target_Section: unspecified
  Target_Section_Raw: "unspecified"
  Placement: unspecified
  Contribution_Text: >
    Section and exact location: `Cataloging, Metadata, and Discovery`, immediately before Dong, Moreno,
    Rodrigues, and Stone (2025), after the tabletop/game-description sources by Bianchini and Munini
    (2025), Hobart (2024), and Smith (2024). Suggested text: Robson, Sassen, Thomale, and Yanowski
    (2019) provide a concrete tabletop-game implementation of enhanced cataloging and faceted discovery
    at the University of North Texas Libraries. Working with a collection of more than 600 board games,
    dice games, collectible card games, and role-playing games, they combine RDA core records, MARC
    identifiers and carrier fields, designer and publisher access points, local `Genre Terms for
    Tabletop Games`, and MARC 590 codes for duration of play, number of players, and recommended age.
    Their Solr/Blacklight implementation translates those codes into patron-facing facets, showing that
    GBLS metadata must connect cataloger-entered game characteristics to discovery interfaces that
    support actual selection questions rather than leaving games findable only by title or broad
    subject.

### Summary
# **Robson, D., Sassen, C., Thomale, J., & Yanowski, K. (2019). Enhancing the discovery of tabletop games. *Library Resources & Technical Services, 63*(3), 199-215. https://doi.org/10.5860/lrts.63n3.199**

Robson, Sassen, Thomale, and Yanowski present a detailed University of North Texas Libraries project for making a large tabletop game collection discoverable through both bibliographic metadata and a locally customized discovery layer. The article treats tabletop games as three-dimensional materials whose library value is limited when they are uncataloged, minimally cataloged, or visible only through staff memory and shelf browsing. The UNT Media Library had a collection of more than six hundred tabletop games, including board games, dice games, collectible card games, and role-playing games. The authors' central question is practical: what cataloging and interface work would let users discover games by the characteristics that matter when choosing something to play, teach with, or research?

The article first frames cataloging as access infrastructure. It draws on cataloging, genre/form, and faceted-navigation literature to argue that tabletop games need full bibliographic records, genre/form terms, and facets rather than title-only or local-memory access. The authors connect their work to prior evidence that many libraries with tabletop collections do not always catalog them, partly because games are perceived as complex objects with insufficient standards. They also connect tabletop game discovery to wider non-book cataloging problems: catalogs often need local enhancements when standard description does not capture how patrons select or interpret unfamiliar formats.

The cataloging guidance is unusually concrete. The authors explain how UNT created RDA core records for tabletop games while treating the game itself as one whole resource. They discuss preferred sources of information, identifiers such as ISBNs and UPCs, designer and publisher access points, titles and edition statements, publication and copyright information, physical description, content/media/carrier fields, notes, summaries, intended audience notes, duration of play, number of players, language notes, and expansion or edition relationships. They also note advanced fields such as creation date and country of producing entity. This matters because tabletop games are not simply books in boxes: component inventories, player counts, age ranges, play duration, designers, publishers, expansions, and editions all affect whether a patron can identify, compare, borrow, replace, or research a game.

A second major contribution is the locally developed `Genre Terms for Tabletop Games`. UNT created fifty genre terms because existing headings were not sufficient for a growing tabletop collection. The authors wanted terms broad enough for novice users but close enough to tabletop gamer language to support experienced searchers. They used BoardGameGeek's type, category, and mechanism lists as a practical source while adding education-related terms aligned with the library's curriculum and research support goals. Each term received an authority record, broader and narrower relationships where appropriate, use notes, and source information. The result is a local controlled vocabulary that can serve the local collection while also giving other libraries a starting point for tabletop game genre access.

The most important discovery-layer contribution is the faceting model. UNT identified three patron-facing selection dimensions that ordinary catalog records do not typically expose as facets: duration of play, number of players, and recommended age of players. Because these values are often printed on boxes but appear in nonstandard free-text form, the authors created local groupings and codes: for example, player-count ranges, play-duration ranges, and age ranges. Catalogers recorded semicolon-separated codes in a MARC 590 local note field. Existing records were reviewed through a master spreadsheet and batch-enhanced with MarcEdit. The local Solr indexing process then extracted valid 590 codes into a multivalued `game_facet` field, and Blacklight translated the codes into user-facing facets with readable labels such as Games - Duration, Games - Number of Players, and Games - Recommended Age.

For the larger GBLS project, this article is a core cataloging and discovery source because it shows how game-based library service depends on metadata workflows, not just acquisitions or programs. A circulating tabletop collection cannot fully function as a service if patrons cannot discover games by play constraints, audience, format, genre, or advisory-relevant characteristics. Robson et al. also show that this work crosses departmental boundaries: media librarians, catalogers, systems librarians, user-interface developers, and IT staff all had to coordinate so that cataloger-entered metadata could become meaningful public-facing filters. The article therefore provides a bridge between collection management, technical services, readers' advisory, curricular support, and public discovery interfaces. It also cautions that libraries without UNT's technical capacity may need scaled versions of the same principle: start by cataloging the games, then add local terms or interface supports when the collection size and user needs justify the effort.
