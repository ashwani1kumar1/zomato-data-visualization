# All Zomato Visualizations: Complete Walkthrough (2500-row Snapshot)

This walkthrough explains how each chart is built from the current full dataset.

Dataset used:
- File: zomato_synthetic_dataset.csv
- Size: 2500 rows x 7 columns
- Snapshot date: 2026-03-24

---

## Visualization 1: Restaurant Type Distribution

Transformation:
1. Select listed_in(type)
2. Count each type with value_counts()
3. Plot bar chart ordered by descending frequency

Current counts:
- Desserts: 446
- Buffet: 441
- Cafe: 416
- Quick Bites: 408
- Casual Dining: 402
- Dining: 387

Insight:
- Most common type is Desserts (446, 17.8%).

---

## Visualization 2: Votes by Restaurant Type

Transformation:
1. Group by listed_in(type)
2. Sum votes
3. Sort descending and plot line chart

Current totals:
- Dining: 102843
- Casual Dining: 92771
- Cafe: 78482
- Buffet: 72800
- Quick Bites: 70507
- Desserts: 64699

Insight:
- Dining has the highest total engagement by votes.

---

## Visualization 3: Online vs Offline Availability

Transformation:
1. Count online_order values (Yes/No)
2. Plot 2-bar count chart

Current counts:
- Yes: 1311 (52.4%)
- No: 1189 (47.6%)

Insight:
- Online availability is slightly higher.

---

## Visualization 4: Rating Distribution

Transformation:
1. Convert rate from x.y/5 to float
2. Plot histogram (8 bins)

Current statistics:
- Mean: 3.811
- Median: 3.8
- Min: 3.1
- Max: 4.5

Insight:
- Most ratings are concentrated around 3.5 to 4.1.

---

## Visualization 5: Couple Budget Preference

Transformation:
1. Convert approx_cost(for two people) to int
2. Count by cost points and plot count chart

Current statistics:
- Mode: 350
- Median: 450
- Mean: 550.28
- Min: 100
- Max: 1400

Insight:
- Mid-range pricing dominates; most frequent price point is 350.

---

## Visualization 6: Ratings by Online/Offline

Transformation:
1. Split ratings by online_order
2. Compare distributions with box plot

Current summary:
- Online mean: 3.81
- Offline mean: 3.81
- Online median: 3.8
- Offline median: 3.8

Insight:
- No meaningful difference in rating center between online and offline groups.

---

## Visualization 7: Type vs Order Mode Heatmap

Transformation:
1. Build pivot table: index=type, columns=online_order, values=count
2. Plot heatmap with annotations

Current matrix:
- Buffet: No=347, Yes=94
- Cafe: No=93, Yes=323
- Casual Dining: No=222, Yes=180
- Desserts: No=133, Yes=313
- Dining: No=250, Yes=137
- Quick Bites: No=144, Yes=264

Insight:
- Cafe, Desserts, and Quick Bites skew online.
- Buffet and Dining skew offline.

---

## Output Files

All visuals are saved in outputs/:
- 01_restaurant_type_count.png
- 02_votes_by_type_line.png
- 03_online_order_count.png
- 04_rating_distribution.png
- 05_couple_cost_distribution.png
- 06_rating_boxplot_online_vs_offline.png
- 07_heatmap_type_vs_order_mode.png

Auto-generated report:
- outputs/analysis_report.md
