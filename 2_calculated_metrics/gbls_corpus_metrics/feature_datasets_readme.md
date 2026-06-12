# GBLS Feature Datasets

Generated from 200 coded summaries using the live controlled metadata schema.
Counts represent coded article presence, not prose term frequency.

```python
import pandas as pd

metrics_dir = "2-outputs/metrics"
articles = pd.read_csv(f"{metrics_dir}/articles_core.csv")
features = pd.read_csv(f"{metrics_dir}/article_features_long.csv")
matrix = pd.read_csv(f"{metrics_dir}/article_feature_matrix.csv")
```

`article_pct` uses all 200 articles as the denominator.
`article_pct_in_year` uses articles published in that year as the denominator.
There are 1 undated records, represented as `n.d.` in publication-year counts.
