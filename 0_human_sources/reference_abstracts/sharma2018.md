# Efficiently Processing and Storing Library Linked Data using Apache Spark and Parquet

## Citation Metadata

Title: Efficiently Processing and Storing Library Linked Data using Apache Spark and Parquet
Authors: Kumar Sharma; Ujjal Marjit; Utpal Biswas
Year: 2018
Journal: Information Technology and Libraries
Volume: 37
Issue: 3
Pages: 29-49
DOI: 10.6017/ital.v37i3.10177
URL: https://doi.org/10.6017/ital.v37i3.10177
Full_Citation: Kumar Sharma; Ujjal Marjit; Utpal Biswas (2018). Efficiently Processing and Storing Library Linked Data using Apache Spark and Parquet. Information Technology and Libraries, 37(3), 29-49. https://doi.org/10.6017/ital.v37i3.10177
Source: https://api.crossref.org/journals/2163-5226/works

## Abstract

Resource Description Framework (RDF) is a commonly used data model in the Semantic Web environment. Libraries and various other communities have been using the RDF data model to store valuable data after it is extracted from traditional storage systems. However, because of the large volume of the data, processing and storing it is becoming a nightmare for traditional data-management tools. This challenge demands a scalable and distributed system that can manage data in parallel. In this article, a distributed solution is proposed for efficiently processing and storing the large volume of library linked data stored in traditional storage systems. Apache Spark is used for parallel processing of large data sets and a column-oriented schema is proposed for storing RDF data. The storage system is built on top of Hadoop Distributed File Systems (HDFS) and uses the Apache Parquet format to store data in a compressed form. The experimental evaluation showed that storage requirements were reduced significantly as compared to Jena TDB, Sesame, RDF/XML, and N-Triples file formats. SPARQL queries are processed using Spark SQL to query the compressed data. The experimental evaluation showed a good query response time, which significantly reduces as the number of worker nodes increases.

## Harvest Notes

Harvested from Crossref metadata. Abstract availability depends on publisher deposits.
