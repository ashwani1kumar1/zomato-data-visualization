# Restaurant Type Distribution: Updated Walkthrough (2500-row Snapshot)

This file explains chart 1 using the current full dataset.

Dataset used:
- File: zomato_synthetic_dataset.csv
- Size: 2500 rows x 7 columns
- Snapshot date: 2026-03-24

---

## Step-by-Step Pipeline

1. Load CSV into DataFrame

```python
import pandas as pd

df = pd.read_csv("zomato_synthetic_dataset.csv")
```

2. Extract category column

```python
type_series = df["listed_in(type)"]
```

3. Count each category

```python
type_counts = type_series.value_counts()
print(type_counts)
```

Current counts:
- Desserts: 446
- Buffet: 441
- Cafe: 416
- Quick Bites: 408
- Casual Dining: 402
- Dining: 387

4. Plot ordered count chart

```python
import matplotlib.pyplot as plt
import seaborn as sns

order = type_counts.index
plt.figure(figsize=(10, 5))
sns.countplot(x=df["listed_in(type)"], order=order, color="#66c2a5")
plt.xlabel("Type of restaurant")
plt.ylabel("Count")
plt.title("Restaurant Type Distribution")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig("outputs/01_restaurant_type_count.png", dpi=140)
```

---

## Interpretation

- Most common type: Desserts (446, 17.8%)
- Least common type: Dining (387, 15.5%)
- Max/min ratio: 1.15x

This distribution is fairly balanced across all 6 types, with no extreme dominance.

---

## Under-the-Hood Logic

- value_counts scans all rows once: O(n)
- Plotting draws one bar per unique type: O(m)
- For this dataset:
  - n = 2500 rows
  - m = 6 unique categories

---

## Quick Validation Snippet

```python
assert len(df) == 2500
assert type_counts.sum() == len(df)
assert len(type_counts.index) == 6
```

If all assertions pass, chart 1 uses the complete dataset correctly.
