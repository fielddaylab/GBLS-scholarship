# Kumar Sharma; Ujjal Marjit; Utpal Biswas (2018). Efficiently Processing and Storing Library Linked Data using Apache Spark and Parquet. Information Technology and Libraries, 37(3), 29-49. https://doi.org/10.6017/ital.v37i3.10177

# Objective Metadata

Citation_Key: 
Year: 2018
Zotero_Item_Key: 
Better_BibTeX_Citation_Key: 
Attachment_Key: 

Title: Efficiently Processing and Storing Library Linked Data using Apache Spark and Parquet
Authors: Kumar Sharma; Ujjal Marjit; Utpal Biswas
Journal: Information Technology and Libraries
Volume: 37
Issue: 3
Pages: 29-49
DOI: 10.6017/ital.v37i3.10177
URL: https://doi.org/10.6017/ital.v37i3.10177
Full_Citation: Kumar Sharma; Ujjal Marjit; Utpal Biswas (2018). Efficiently Processing and Storing Library Linked Data using Apache Spark and Parquet. Information Technology and Libraries, 37(3), 29-49. https://doi.org/10.6017/ital.v37i3.10177

## Abstract

Resource Description Framework (RDF) is a commonly used data model in the Semantic Web environment. Libraries and various other communities have been using the RDF data model to store valuable data after it is extracted from traditional storage systems. However, because of the large volume of the data, processing and storing it is becoming a nightmare for traditional data-management tools. This challenge demands a scalable and distributed system that can manage data in parallel. In this article, a distributed solution is proposed for efficiently processing and storing the large volume of library linked data stored in traditional storage systems. Apache Spark is used for parallel processing of large data sets and a column-oriented schema is proposed for storing RDF data. The storage system is built on top of Hadoop Distributed File Systems (HDFS) and uses the Apache Parquet format to store data in a compressed form. The experimental evaluation showed that storage requirements were reduced significantly as compared to Jena TDB, Sesame, RDF/XML, and N-Triples file formats. SPARQL queries are processed using Spark SQL to query the compressed data. The experimental evaluation showed a good query response time, which significantly reduces as the number of worker nodes increases.

# Subjective Metadata

Coded_By: Qwen/Qwen3-14B-AWQ
Version: 2.0.0-reference-abstract
Coding_Basis: citation_and_abstract_only

## Source_Type
Value: peer_reviewed_journal_article
Confidence: high
Evidence: Published in *Information Technology and Libraries* (peer-reviewed journal)
Reason_For: Journal is explicitly identified as peer-reviewed
Reason_Against: none

## Evidence_Type
Value: empirical_study
Confidence: high
Evidence: "Experimental evaluation showed... query response time... as the number of worker nodes increases"
Reason_For: Describes controlled comparison of storage formats and performance metrics
Reason_Against: none

## Primary_Methodology
Value: experimental_study
Confidence: high
Evidence: "Experimental evaluation showed... query response time... as the number of worker nodes increases"
Reason_For: Directly references experimental testing and comparative analysis
Reason_Against: none

## Library_Context
Value: academic_library
Confidence: high
Evidence: Focus on "library linked data" and technical infrastructure for data management
Reason_For: Context is explicitly about library data systems and processing needs
Reason_Against: none

## Game_Format
Value: unspecified_game_format
Confidence: high
Evidence: No mention of games, play formats, or game-related technologies
Reason_For: Abstract focuses on data processing, not games or play
Reason_Against: none

## Service_Area
Value: not_applicable
Confidence: high
Evidence: No mention of library services, collections, programming, or user engagement
Reason_For: Focus is on technical infrastructure for data management
Reason_Against: none

## Audience
Value: not_applicable
Confidence: high
Evidence: No specific audience or user group is discussed
Reason_For: Abstract focuses on technical implementation, not end-users
Reason_Against: none

## Intended_Outcome
Value: not_applicable
Confidence: high
Evidence: No explicit outcomes related to library services or user impact are stated
Reason_For: Focus is on technical performance metrics, not service outcomes
Reason_Against: none

## Evidence_Confidence
Value: demonstrated_outcome
Confidence: high
Evidence: "Experimental evaluation showed... storage requirements were reduced significantly... query response time"
Reason_For: Reports quantifiable results from controlled comparisons
Reason_Against: none

## Service_Conditions_Addressed
Value: not_applicable
Confidence: high
Evidence: No discussion of implementation conditions, accessibility, or sustainability
Reason_For: Focus is on technical architecture, not service delivery contexts
Reason_Against: none

## Conceptual_Theme
Value: not_identified
Confidence: high
Evidence: No theoretical or conceptual framework is discussed
Reason_For: Abstract focuses on technical implementation, not conceptual foundations
Reason_Against: none

## Coding_Confidence
Value: high
Confidence: high
Evidence: All coding decisions supported by explicit text in abstract/citation
Reason_For: No ambiguous or missing information in source description
Reason_Against: none

# Audit Provenance

Audited: no
Audited_By: not audited
Audit_Action: not audited
Audit_Notes: n/a
Sampled_For_Quality: no
