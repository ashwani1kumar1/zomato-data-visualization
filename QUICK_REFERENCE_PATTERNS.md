# Restaurant Type Distribution: Quick Reference (Updated)

Current snapshot:
- Dataset size: 2500 rows x 7 columns
- Restaurant type categories: 6

---

## Pattern 1: Load CSV

```python
import pandas as pd

df = pd.read_csv("zomato_synthetic_dataset.csv")
```

Output:
- DataFrame shape: (2500, 7)

---

## Pattern 2: Select One Column

```python
type_col = df["listed_in(type)"]
```

Output:
- Series length: 2500

---

## Pattern 3: Count Category Frequency

```python
type_counts = type_col.value_counts()
```

Current output:
- Desserts: 446
- Buffet: 441
- Cafe: 416
- Quick Bites: 408
- Casual Dining: 402
- Dining: 387

---

## Pattern 4: Ordered Count Plot

```python
import matplotlib.pyplot as plt
import seaborn as sns

order = type_counts.index
plt.figure(figsize=(10, 5))
sns.countplot(x=type_col, order=order, color="#66c2a5")
plt.xlabel("Type of restaurant")
plt.ylabel("Count")
plt.title("Restaurant Type Distribution")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig("outputs/01_restaurant_type_count.png", dpi=140)
```

---

## Complexity

- read_csv: O(n)
- value_counts: O(n)
- countplot prep: O(n)
- n = 2500, m = 6

---

## Sanity Checks

```python
assert len(df) == 2500
assert type_counts.sum() == 2500
assert len(type_counts) == 6
```
