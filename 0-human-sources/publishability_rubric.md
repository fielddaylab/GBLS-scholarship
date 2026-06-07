# Target Journal Evaluator & Alignment Rubric

## 1. System Prompt Execution Guidelines
This rubric automates the evaluation of a comprehensive literature review manuscript analyzing >250 papers on Games-Based Library Services (GBLS), focusing specifically on library mission over technology.

### AI Agent Operational Instructions
1. Parse the manuscript text fully.
2. Cross-reference metrics against the global exclusions and target journal profiles below.
3. Output a structured JSON or Markdown report containing:
   * Target Profile Fit (PASS/FAIL)
   * Hard Constraint Delta (Word/Page counts)
   * Scoring Breakdown per Target Journal (1-5 Scale)
   * Required Corrections Checklist

### Global Manuscript Scope Exclusions (Critical Failure Triggers)
If the AI agent detects any of the following, flag the manuscript for a human rewrite:
* **Tech-Heavy Focus:** Over-indexing on hardware setups, software specifications, or coding mechanics over institutional outcomes.
* **Insufficient Data Synthesis:** Failure to clearly categorize, track, and synthesize the >250 reviewed papers.
* **Missing Mission Alignment:** Failure to explicitly tie GBLS to core library tenets (e.g., civic engagement, public literacy, institutional value, community building).

---

## 2. Quantitative Constraint Engine

### [LQ] The Library Quarterly
* **Source Documentation:** Verifiable via [The Library Quarterly Policies](https://www.journals.uchicago.edu/journals/lq/policies).
* **Measurement Metric:** Double-spaced pages.
* **Hard Limits:** Minimum 25 pages, Maximum 35 pages.
* **Inclusions:** Must include preliminary pages, references, tables, figures, and appendices in the count.
* **Layout Constraints:** Times New Roman font, 1" top/bottom margins, 1.5" margins on each side.

### [JDoc] Journal of Documentation
* **Source Documentation:** Verifiable via [Emerald Publishing Journal of Documentation Guide](https://www.emeraldgrouppublishing.com/journal/jd).
* **Measurement Metric:** Word count.
* **Hard Limits:** Between 4,000 and 10,000 words. 
* **Inclusions:** Total manuscript text, including structured abstract, references, all text in tables, figures, and appendices.

### [LT] Library Trends
* **Measurement Metric:** Word count.
* **Hard Limits:** Minimum 5,000 words, Maximum 8,000 words.
* **Inclusions:** Main body text and references. Appends dense data to external repositories.

### [RSR] Reference Services Review
* **Source Documentation:** Verifiable via [Emerald Publishing Reference Services Review Guide](https://www.emeraldgrouppublishing.com/journal/rsr).
* **Measurement Metric:** Total absolute word count.
* **Hard Limits:** Minimum 4,000 words, Maximum 9,000 words.
* **Inclusions:** Strict complete count inclusive of structured abstract, body, references, appendices, tables, and text inside figures.
* **Layout Constraints:** Explicitly allow and add 280 words to the baseline data layout calculation for every embedded table or figure included.

---

## 3. Qualitative Evaluation Rubrics (1-5 Scale)

### Profile A: The Library Quarterly (LQ)
*Focus: Deep social, cultural, and organizational missions of libraries.*

* **1 - Deficient:** Focuses strictly on operational instructions of games; no sociological or philosophical grounding.
* **2 - Marginal:** Mentions library values passingly, but remains mostly descriptive of GBLS activities.
* **3 - Acceptable:** Connects gaming trends to the library's mission; maintains proper institutional framing.
* **4 - Advanced:** Evaluates how GBLS shapes library policy and advances democratic or civic engagement across a wide body of literature.
* **5 - Exceptional:** Synthesizes the 250+ papers to challenge, redefine, or deeply validate library philosophy regarding community and institutional impact.

### Profile B: Journal of Documentation (JDoc)
*Focus: Methodological rigor, data coding, and information behavior frameworks.*

* **1 - Deficient:** An unstructured narrative summary lacking explicit selection criteria or structural themes.
* **2 - Marginal:** Explains selection but relies on weak coding frameworks; data synthesis feels disconnected.
* **3 - Acceptable:** Explains selection and coding of the 250+ papers clearly; maps findings to broad human information behaviors.
* **4 - Advanced:** Displays deep methodological rigor; uses clear taxonomy and visualization to model the GBLS landscape.
* **5 - Exceptional:** Builds an entirely new conceptual framework or paradigm demonstrating how GBLS impacts information organization and systemic library use.

### Profile C: Library Trends (LT)
*Focus: Landscape shifts, trend forecasting, and macro-level overviews.*

* **1 - Deficient:** Highly localized view focusing on isolated case studies rather than broader industry trends.
* **2 - Marginal:** Identifies basic trends but lacks historical context or long-term industry outlook.
* **3 - Acceptable:** Identifies macro-level landscape shifts in GBLS and provides historical context for its evolution.
* **4 - Advanced:** Effectively synthesizes past and present research to accurately forecast the trajectory of mission-driven GBLS.
* **5 - Exceptional:** Establishes a definitive, authoritative map proving GBLS is a permanent structural shift in how libraries fulfill foundational missions.

### Profile D: Reference Services Review (RSR)
*Focus: High public-service utility mapped to a solid conceptual model.*

* **1 - Deficient:** Strictly conceptual or philosophical with zero practical applications for public services or user engagement.
* **2 - Marginal:** Offers generic advice that front-line librarians cannot easily execute or scale.
* **3 - Acceptable:** Balances high-level synthesis with clear insights that aid front-line public service delivery.
* **4 - Advanced:** Provides highly actionable takeaways from the 250+ paper synthesis to optimize library outreach, reference, or user engagement.
* **5 - Exceptional:** Delivers a masterclass synthesis that directly transforms front-line capabilities while introducing a robust, mission-critical framework.

