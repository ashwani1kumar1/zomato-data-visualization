# Zomato Data Analysis Project: Complete Index
## Current State (Updated for 2500-row dataset)

---

## Project Structure

```text
zomato-data- analysis/
|-- create_zomato_dataset.py
|-- zomato_analysis_detailed.py
|-- restaurant_type_walkthrough_interactive.py
|-- all_visualizations_walkthrough_interactive.py
|-- zomato_analysis_notebook.ipynb
|-- zomato_synthetic_dataset.csv
|-- zomato_synthetic_dataset_cleaned.csv
|-- outputs/
|   |-- 01_restaurant_type_count.png
|   |-- 02_votes_by_type_line.png
|   |-- 03_online_order_count.png
|   |-- 04_rating_distribution.png
|   |-- 05_couple_cost_distribution.png
|   |-- 06_rating_boxplot_online_vs_offline.png
|   |-- 07_heatmap_type_vs_order_mode.png
|   `-- analysis_report.md
|-- RESTAURANT_TYPE_ANALYSIS_WALKTHROUGH.md
|-- ALL_VISUALIZATIONS_WALKTHROUGH.md
|-- QUICK_REFERENCE_PATTERNS.md
`-- PROJECT_INDEX.md
```

---

## Dataset Snapshot

- Source file: zomato_synthetic_dataset.csv
- Current size: 2500 rows x 7 columns
- Current update date: 2026-03-24

### Current Key Results

1. Online delivery availability:
- Yes: 1311 (52.4%)
- No: 1189 (47.6%)

2. Most favored type by total votes:
- Dining (102843 votes)

3. Couple budget preference:
- Most common approx cost for two: 350

4. Most common restaurant type by count:
- Desserts (446 restaurants)

---

## Run Commands

### Full analysis on current dataset

```bash
c:/Users/ashwa/OneDrive/Apps/.venv/Scripts/python.exe zomato_analysis_detailed.py --input zomato_synthetic_dataset.csv --output-dir outputs --cleaned-output zomato_synthetic_dataset_cleaned.csv
```

### Regenerate synthetic dataset from scratch

```bash
c:/Users/ashwa/OneDrive/Apps/.venv/Scripts/python.exe zomato_analysis_detailed.py --regenerate --rows 2500 --seed 42
```

### Run interactive walkthroughs

```bash
c:/Users/ashwa/OneDrive/Apps/.venv/Scripts/python.exe restaurant_type_walkthrough_interactive.py
c:/Users/ashwa/OneDrive/Apps/.venv/Scripts/python.exe all_visualizations_walkthrough_interactive.py
```

---

## Documentation Map

- RESTAURANT_TYPE_ANALYSIS_WALKTHROUGH.md
Detailed step-by-step walkthrough for chart 1 (type distribution).

- ALL_VISUALIZATIONS_WALKTHROUGH.md
Updated walkthrough for all 7 visualizations using 2500-row metrics.

- QUICK_REFERENCE_PATTERNS.md
Reusable code patterns and complexity notes (updated for current snapshot).

- outputs/analysis_report.md
Auto-generated report from the latest processing run.

---

## Notes

- Walkthrough scripts now compute insights dynamically from the dataset.
- If dataset size changes again, rerun zomato_analysis_detailed.py and the walkthrough scripts to refresh outputs.
