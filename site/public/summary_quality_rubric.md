# Summary Quality Rubric

Rubric ID: `gbls_summary_quality`

Version: `2.0.0`

This rubric evaluates whether an article summary is suitable for use in the
Games-Based Library Services literature review. Each dimension is scored from
1 to 5. The machine-readable block below is the authoritative definition used
by the coding interface and its server-side validation.

```json rubric
{
  "id": "gbls_summary_quality",
  "version": "2.0.0",
  "scoreMinimum": 1,
  "scoreMaximum": 5,
  "dimensions": [
    {
      "id": "accuracy",
      "label": "Factual Accuracy",
      "description": "How faithfully does the summary represent the source?",
      "levels": [
        {
          "score": 1,
          "label": "Poor",
          "definition": "Contains major inaccuracies, misrepresents key claims, or includes information not supported by the source."
        },
        {
          "score": 2,
          "label": "Fair",
          "definition": "Includes some accurate information but contains notable errors, distortions, or misleading interpretations."
        },
        {
          "score": 3,
          "label": "Adequate",
          "definition": "Generally accurate, though minor inaccuracies or omissions may be present. Core claims are represented correctly."
        },
        {
          "score": 4,
          "label": "Good",
          "definition": "Accurately represents the source with only trivial errors or ambiguities. Key claims and evidence are faithfully conveyed."
        },
        {
          "score": 5,
          "label": "Excellent",
          "definition": "Fully accurate and faithful to the source. No substantive errors, distortions, or unsupported claims."
        }
      ]
    },
    {
      "id": "coverage",
      "label": "Coverage & Completeness",
      "description": "Does the summary capture the source's important purpose, methods, findings, and implications?",
      "levels": [
        {
          "score": 1,
          "label": "Poor",
          "definition": "Omits most major elements of the source and provides an incomplete or misleading picture."
        },
        {
          "score": 2,
          "label": "Fair",
          "definition": "Captures some important elements but misses several key aspects of the purpose, methods, findings, or implications."
        },
        {
          "score": 3,
          "label": "Adequate",
          "definition": "Includes the main points of the source but lacks important details or nuance in one or more areas."
        },
        {
          "score": 4,
          "label": "Good",
          "definition": "Covers nearly all major elements and provides a well-rounded representation of the source."
        },
        {
          "score": 5,
          "label": "Excellent",
          "definition": "Thoroughly captures the source's purpose, methods, findings, and implications with appropriate detail and balance."
        }
      ]
    },
    {
      "id": "clarity",
      "label": "Clarity & Usefulness",
      "description": "Is the summary readable and useful for synthesis?",
      "levels": [
        {
          "score": 1,
          "label": "Poor",
          "definition": "Difficult to understand, poorly organized, or not useful for informing further analysis or synthesis."
        },
        {
          "score": 2,
          "label": "Fair",
          "definition": "Somewhat understandable but contains organizational, readability, or coherence issues that limit usefulness."
        },
        {
          "score": 3,
          "label": "Adequate",
          "definition": "Clear enough to understand and generally useful, though improvements in organization, conciseness, or emphasis would help."
        },
        {
          "score": 4,
          "label": "Good",
          "definition": "Well-written, logically organized, and useful for synthesis or literature review purposes."
        },
        {
          "score": 5,
          "label": "Excellent",
          "definition": "Exceptionally clear, concise, and well-structured; highly useful for comparison, synthesis, and decision-making."
        }
      ]
    }
  ]
}
```

## Versioning

Increment the version whenever a dimension, description, score label, or scoring
range changes. Use a major-version increment when scores from the revised rubric
should not be compared directly with earlier scores.
