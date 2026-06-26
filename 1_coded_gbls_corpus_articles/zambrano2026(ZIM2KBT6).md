# Zambrano, A. F., Wei, Z., Zhang, J., Baker, R. S., Ocumpaugh, J., Barany, A., Liu, X., Ginger, J., Paquette, L., Zhou, Y., & Borchers, C. (2026). Data Plus Theory Equals Codebook: Leveraging LLMs for Human-AI Codebook Development. Journal of Educational Data Mining, 18(1), 25–45.

# Objective Metadata

Citation_Key: Zambrano+2026
Year: 2026
Zotero_Item_Key: ZIM2KBT6
Better_BibTeX_Citation_Key: 
Attachment_Key: 

# Structured Extraction

## Purpose
The article investigates the potential of Large Language Models (LLMs), specifically GPT-4o, to support theory-informed qualitative codebook development. It aims to determine how effectively GPT can generate high-quality, theory-aligned codebooks when guided by specific educational theories and to identify which prompting strategies best facilitate this collaboration between human researchers and AI.
Evidence: "This paper investigates the potential of GPT-4o to support theory-informed codebook development across two educational contexts... Specifically, we investigate the following research questions: (RQ1) How effectively can GPT contribute to the qualitative codebook development process when guided by specific learning theories? (RQ2) What prompting approaches best guide GPT to apply specific theoretical frameworks in collaboration with human researchers during codebook development?"
Confidence: high

## Method
The study employs a mixed-methods experimental design involving two distinct studies. Study 1 uses a three-step iterative process (Theory-only, Theory+Data, Human Refinement) to develop a codebook for Self-Regulated Learning (SRL). Study 2 replicates this process for Interest Development (ID) and expands it to compare four prompting strategies: no theory provided, theory named only, full references provided, and full-text theory papers supplied. GPT-4o was used via API with temperature set to 0. Human researchers reviewed and refined all AI-generated outputs.
Evidence: "In the first study, we employ a three-step approach... In the second study, we extend this approach to a STEM game-based learning context... We compare four prompting strategies: no theories provided, theories named, full references given, and full-text theory papers supplied."
Confidence: high

## Population and Data
Study 1 utilized an open dataset of think-aloud transcripts from 15 students (14 undergraduate, 1 graduate) interacting with intelligent tutoring systems for stoichiometry and formal logic. Study 2 analyzed 144 interview transcripts from 14 middle-school students participating in a Minecraft-based astronomy summer camp (WHIMC project).
Evidence: "Fourteen undergraduate students and one graduate student participated... The dataset consists of think-aloud transcripts from students working within three intelligent tutoring systems... we analyzed 144 interview transcripts from 14 middle-school students who participated in a 5-day... summer camp... leveraging Minecraft’s Java Edition."
Confidence: high

## Findings
In Study 1 (SRL), GPT-4o effectively identified SRL constructs when provided with theory references and data, though initial outputs contained overlapping constructs requiring human refinement. In Study 2 (ID), providing full-text theory papers enhanced theoretical alignment but reduced practical applicability due to overly broad or abstract codes. Naming the theory without providing full references produced the most practical and usable codebook. GPT struggled with discriminant validity for nuanced constructs (e.g., distinguishing situational vs. individual interest emotions) and occasionally generated misleading examples for social interaction codes. Human refinement remained essential for merging overlapping codes and ensuring operational feasibility.
Evidence: "Human evaluations show that naming the theory without including full references produced the most practical and usable codebook, while supplying full papers to the prompt enhanced theoretical alignment but reduced applicability... GPT struggled to identify actual instances in the data that meaningfully differentiate these categories... human review remains essential for code merging and codebook refinement."
Confidence: high

## Implications
The authors conclude that LLMs can be valuable partners in theory-driven qualitative research when grounded in well-established frameworks, but prompt design is critical. They recommend that researchers explicitly specify theoretical lenses to mitigate implicit biases from training data. The study suggests that while LLMs excel at generating concrete, content-grounded codes, human expertise is required for interpretive nuance and final codebook validation. The authors provide open-source code and prompts to support replication.
Evidence: "These findings suggest that GPT-4o can be a valuable partner in theory-driven qualitative research when grounded in well-established frameworks, but that attention to prompt design is required... Our results show that widely available foundation models... can effectively distill established educational theories to support qualitative research and codebook development."
Confidence: high

# Summary

This article by Zambrano et al. (2026) addresses a gap in Educational Data Mining (EDM) literature regarding the use of Large Language Models (LLMs) for qualitative codebook development. While prior research has demonstrated LLMs' utility in inductive, bottom-up coding, this study focuses on deductive, theory-informed approaches. The authors argue that grounding codebooks in established theoretical frameworks is essential for consistency and replicability, yet previous LLM studies often neglected this aspect. The primary objective was to evaluate GPT-4o’s ability to generate high-quality, theory-aligned codebooks and to determine optimal prompting strategies for human-AI collaboration.

The study comprises two empirical investigations. Study 1 focused on Self-Regulated Learning (SRL), utilizing Winne & Hadwin’s and Zimmerman’s theories. The data consisted of think-aloud transcripts from 15 students using intelligent tutoring systems for stoichiometry and logic. The methodology involved a three-step process: first, prompting GPT with theory references only; second, providing both theory and data; and third, human refinement of the resulting codebook. Results indicated that GPT-4o could accurately identify key SRL constructs from its internal knowledge base. However, initial outputs contained significant conceptual overlap (e.g., distinguishing between self-monitoring and reflective thinking) and included constructs irrelevant to the specific dataset (e.g., social environment codes in individual work contexts). Providing data alongside theory improved specificity and filtered out inapplicable codes, but human intervention was still required to merge overlapping constructs and ensure operational clarity.

Study 2 extended this inquiry to Interest Development (ID), guided by Hidi & Renninger’s four-phase model. The dataset comprised 144 interview transcripts from 14 middle-school students engaged in a Minecraft-based astronomy learning environment. This study compared four prompting strategies: no theory, theory named only, full references provided, and full-text theory papers supplied. The findings revealed a trade-off between theoretical alignment and practical usability. Supplying full-text theory papers resulted in codebooks that were theoretically accurate but too abstract for practical coding of individual utterances. Conversely, merely naming the theory produced the most usable codebook, balancing theoretical grounding with operational feasibility. GPT struggled with discriminant validity for nuanced constructs, such as differentiating between emotions associated with situational versus individual interest, and occasionally misclassified social interactions.

The authors conclude that LLMs are effective tools for distilling established educational theories into qualitative codes, particularly when prompts explicitly specify the theoretical lens. However, they emphasize that LLMs are not replacements for human expertise. Human researchers remain critical for refining code definitions, resolving conceptual overlaps, and ensuring that codes are practically applicable to the specific data context. The study highlights the importance of prompt engineering in mitigating implicit biases and enhancing the relevance of AI-generated outputs. All prompts and codebooks developed during the study were made available for replication, supporting transparency in human-AI collaborative research methods.

# Subjective Metadata

Coded_By: Qwen3-14B-AWQ
Version: 1.0

## Source_Type
Value: peer_reviewed_journal_article
Confidence: high
Evidence: "Journal of Educational Data Mining, Volume 18, No 1, 2026"
Reason_For: The article is published in a scholarly journal and includes peer review elements such as structured methodology, empirical findings, and detailed analysis.
Reason_Against: none

## Peer_Review
Value: yes
Confidence: high
Evidence: "Journal of Educational Data Mining, Volume 18, No 1, 2026"
Reason_For: The article is published in a peer-reviewed journal, indicating it has undergone formal peer review.
Reason_Against: none

## Evidence_Type
Value:
- empirical_study
Confidence: high
Evidence: "Results indicate that GPT-4o can effectively leverage its knowledge base to identify SRL constructs reflected in student problem-solving behavior."
Reason_For: The study presents empirical findings based on the analysis of datasets and human evaluations.
Reason_Against: none

## Primary_Methodology
Value: mixed_methods
Confidence: high
Evidence: "In the first study, we employ a three-step approach... In the second study, we extend this approach to a STEM game-based learning context... We compare four prompting strategies: no theories provided, theories named, full references given, and full-text theory papers supplied."
Reason_For: The study combines qualitative analysis of codebooks with quantitative evaluation of human assessments and empirical data.
Reason_Against: none

## Library_Context
Value: non_library_context
Confidence: high
Evidence: "The study comprises two empirical investigations. Study 1 focused on Self-Regulated Learning (SRL), utilizing Winne & Hadwin’s and Zimmerman’s theories. The data consisted of think-aloud transcripts from 15 students using intelligent tutoring systems for stoichiometry and logic."
Reason_For: The study focuses on educational data mining and uses datasets from intelligent tutoring systems and game-based learning environments, which are not directly related to library contexts.
Reason_Against: none

## Game_Format
Value:
- digital_game
- game_creation
Confidence: medium
Evidence: "The dataset comprises 144 interview transcripts from 14 middle-school students who participated in a 5-day... summer camp... leveraging Minecraft’s Java Edition."
Reason_For: The study involves Minecraft, a digital game, and discusses game-based learning environments.
Reason_Against: The article does not explicitly focus on library services or game formats directly related to libraries.

## Service_Area
Value:
- learning_and_literacy
Confidence: high
Evidence: "The study comprises two empirical investigations. Study 1 focused on Self-Regulated Learning (SRL), utilizing Winne & Hadwin’s and Zimmerman’s theories."
Reason_For: The study focuses on learning processes and educational theories related to self-regulated learning and interest development.
Reason_Against: none

## Audience
Value: students
Confidence: high
Evidence: "Fourteen undergraduate students and one graduate student participated... The dataset consists of think-aloud transcripts from students working within three intelligent tutoring systems... we analyzed 144 interview transcripts from 14 middle-school students who participated in a 5-day... summer camp..."
Reason_For: The study involves students at various educational levels, including middle school, undergraduate, and graduate students.
Reason_Against: none

## Intended_Outcome
Value: learning_and_literacy
Confidence: high
Evidence: "The study comprises two empirical investigations. Study 1 focused on Self-Regulated Learning (SRL), utilizing Winne & Hadwin’s and Zimmerman’s theories."
Reason_For: The study aims to understand and support learning processes through the development of codebooks grounded in educational theories.
Reason_Against: none

## Evidence_Confidence
Value: demonstrated_outcome
Confidence: high
Evidence: "Results indicate that GPT-4o can effectively leverage its knowledge base to identify SRL constructs reflected in student problem-solving behavior."
Reason_For: The study presents rigorous findings with validated measures and human evaluations.
Reason_Against: none

## Service_Conditions_Addressed
Value:
- skilled_facilitation_required
- evaluation_or_reflection
Confidence: medium
Evidence: "Human evaluations show that naming the theory without including full references produced the most practical and usable codebook, while supplying full papers to the prompt enhanced theoretical alignment but reduced applicability."
Reason_For: The study emphasizes the need for human facilitation and evaluation in refining codebooks generated by AI.
Reason_Against: The article does not explicitly address other service conditions such as access infrastructure or inclusive design.

## Conceptual_Theme
Value:
- educational_psychology
- information_behavior_and_practice
Confidence: high
Evidence: "The study comprises two empirical investigations. Study 1 focused on Self-Regulated Learning (SRL), utilizing Winne & Hadwin’s and Zimmerman’s theories."
Reason_For: The study applies educational psychology frameworks and examines information behavior through the lens of self-regulated learning and interest development.
Reason_Against: none

## Coding_Confidence
Value: high

# Potential Contributions to Review

## Conceptual Terrain: Games, Play, and Library Service
Contribution_Text: This article contributes to the conceptual terrain by examining the theoretical grounding of codebook development in educational contexts, which can inform how games and play are conceptualized in library services. The study highlights the importance of theoretical frameworks in shaping qualitative research, which is relevant to understanding how games are used in educational and library settings.

## Game Modalities in Library Contexts
Contribution_Text: The study discusses the use of digital games (Minecraft) in educational contexts, which can be extended to library services. The findings on the effectiveness of prompting strategies for AI in generating codebooks can inform how libraries might use similar approaches to analyze and understand the impact of game-based learning in their services.

## Libraries as Playful Spaces and Service Environments
Contribution_Text: The article's focus on game-based learning environments can be relevant to how libraries design and implement playful spaces and services. The study's insights into the role of theoretical frameworks in shaping qualitative analysis can help libraries better understand and evaluate the effectiveness of their game-based programs.

## Service Purposes and Library Functions
Contribution_Text: The study's emphasis on learning and literacy outcomes can inform how libraries frame their services around educational goals. The findings on the importance of human facilitation and evaluation in refining AI-generated codebooks can be applied to how libraries assess and refine their game-based learning initiatives.

## Research, Scholarship, and Creative Production
Contribution_Text: The article contributes to the understanding of how AI can be used in research and scholarship, particularly in the context of qualitative codebook development. This has implications for how libraries support research and creative production involving games and play.

## Cross-Cutting Conditions for Effective Games-Based Library Services
Contribution_Text: The study's findings on the importance of prompt design and human facilitation in AI-assisted codebook development can inform cross-cutting conditions for effective games-based library services. The emphasis on theoretical alignment and practical applicability is relevant to ensuring that library services are both theoretically sound and practically effective.

## Productive Incongruences
No substantial incongruence identified.

# Audit Provenance

Audited: [yes | no]
Audited_By: [paid model name, or "not audited"]
Audit_Action: [confirmed | revised classifications | revised summary | flagged | not audited]
Audit_Notes: [what the auditor checked or changed, or "n/a"]
Sampled_For_Quality: [yes | no]
