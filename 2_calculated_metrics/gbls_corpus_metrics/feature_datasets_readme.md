# GBLS Feature Datasets

Generated: 2026-06-26 13:28
Articles: 227 | Feature assignments: 3640

## Quick start (Python / Colab)

```python
import pandas as pd

metrics_dir = "2_calculated_metrics/gbls_corpus_metrics"
articles = pd.read_csv(f"{metrics_dir}/articles_core.csv")
features = pd.read_csv(f"{metrics_dir}/article_features_long.csv")
matrix   = pd.read_csv(f"{metrics_dir}/article_feature_matrix.csv")
```

## Key files

| File | Grain | Purpose |
|------|-------|---------|
| `articles_core.csv` | 1 row/article | All metadata fields; pipe-delimited for multi-label |
| `articles.csv` | 1 row/article | Same + full summary text |
| `article_features_long.csv` | 1 row/assignment | Tidy format; filter by `feature_group` |
| `article_feature_matrix.csv` | 1 row/article | Binary columns across all feature groups |
| `feature_counts.csv` | 1 row/value | Article counts and percentages per feature |
| `feature_cooccurrence.csv` | 1 row/pair | Co-occurring feature pairs (≥2 articles) |

## Counting conventions

- Counts represent coded article presence, not prose term frequency.
- Multi-label fields (Conceptual_Theme, Evidence_Confidence, Evidence_Type, Game_Format, Intended_Outcome, Library_Context, Primary_Methodology, Service_Area, Service_Audience, Service_Conditions_Addressed, Source_Type) may contribute multiple assignments per article.
- `article_pct` = article_count / total_articles × 100
- `article_pct_in_year` uses same-year article count as denominator.

## Schema fields

- **Source_Type** (multi-label)
- **Evidence_Type** (multi-label)
- **Primary_Methodology** (multi-label)
- **Conceptual_Theme** (multi-label)
- **Library_Context** (multi-label)
- **Game_Format** (multi-label)
- **Service_Area** (multi-label)
- **Service_Audience** (multi-label)
- **Intended_Outcome** (multi-label)
- **Evidence_Confidence** (multi-label)
- **Service_Conditions_Addressed** (multi-label)

## Undated records

1 article(s) have no year and are labelled `n.d.` in year summaries.
