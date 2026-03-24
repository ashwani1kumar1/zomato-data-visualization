"""
Restaurant Type Distribution: Interactive Step-by-Step Walkthrough
This script shows every transformation from raw data to visualization
with detailed output at each stage.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================================
# STEP 1: LOAD THE RAW DATASET
# ============================================================================

print("\n" + "="*80)
print("STEP 1: LOAD RAW DATA FROM CSV")
print("="*80)

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "zomato_synthetic_dataset.csv"

print(f"\nLoading from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

print(f"\nDataset shape: {df.shape}")
print(f"  - Rows (restaurants): {len(df)}")
print(f"  - Columns (features): {len(df.columns)}")

print("\nColumns in the dataset:")
print(f"  {list(df.columns)}")

print("\nFirst 10 rows of raw data:")
print(df.head(10).to_string())

# ============================================================================
# STEP 2: EXAMINE THE 'listed_in(type)' COLUMN
# ============================================================================

print("\n" + "="*80)
print("STEP 2: EXAMINE THE 'listed_in(type)' COLUMN")
print("="*80)

type_column = df["listed_in(type)"]
print(f"\nThe column we're analyzing:")
print(type_column.head(15).to_string())

print(f"\nData type: {type_column.dtype}")
print(f"Total values: {len(type_column)}")

# ============================================================================
# STEP 3: FIND UNIQUE RESTAURANT TYPES
# ============================================================================

print("\n" + "="*80)
print("STEP 3: FIND ALL UNIQUE RESTAURANT TYPES")
print("="*80)

unique_types = df["listed_in(type)"].unique()
print(f"\nNumber of unique types: {len(unique_types)}")
print(f"\nUnique restaurant types:")
for i, rtype in enumerate(unique_types, 1):
    print(f"  {i}. {rtype}")

# ============================================================================
# STEP 4: COUNT OCCURRENCES OF EACH TYPE
# ============================================================================

print("\n" + "="*80)
print("STEP 4: COUNT HOW MANY RESTAURANTS OF EACH TYPE")
print("="*80)

type_counts = df["listed_in(type)"].value_counts()
print("\nValue counts (automatic sorting by frequency):")
print(type_counts)

print("\nDetailed breakdown:")
for restaurant_type, count in type_counts.items():
    percentage = (count / len(df)) * 100
    bar = "█" * int(count / 5)  # 1 block per 5 restaurants
    print(f"  {restaurant_type:20s}: {count:3d} ({percentage:5.1f}%) {bar}")

total_check = type_counts.sum()
print(f"\nTotal: {total_check} (should equal {len(df)})")

# ============================================================================
# STEP 5: GET ORDERED SEQUENCE FOR VISUALIZATION
# ============================================================================

print("\n" + "="*80)
print("STEP 5: PREPARE ORDERING FOR VISUALIZATION")
print("="*80)

order = type_counts.index
print("\nOrder for left-to-right display (by descending frequency):")
for i, rtype in enumerate(order, 1):
    count = type_counts[rtype]
    print(f"  Bar {i}: {rtype:20s} (count={count})")

# ============================================================================
# STEP 6: CREATE THE MATPLOTLIB FIGURE
# ============================================================================

print("\n" + "="*80)
print("STEP 6: CREATE FIGURE AND PLOT")
print("="*80)

print("\nCreating figure with size (10, 5) inches...")
fig, ax = plt.subplots(figsize=(10, 5))

print("Building countplot with seaborn...")
sns.countplot(x=df["listed_in(type)"], order=order, color="#66c2a5", ax=ax)

print("Adding labels and title...")
ax.set_xlabel("Type of restaurant")
ax.set_ylabel("Count")
ax.set_title("Restaurant Type Distribution")
ax.tick_params(axis='x', rotation=25)

print("Adjusting layout for clean appearance...")
plt.tight_layout()

# ============================================================================
# STEP 7: SAVE AND DISPLAY
# ============================================================================

print("\n" + "="*80)
print("STEP 7: SAVE PLOT TO FILE")
print("="*80)

output_path = BASE_DIR / "outputs" / "01_restaurant_type_count.png"
output_path.parent.mkdir(parents=True, exist_ok=True)

print(f"\nSaving to: {output_path}")
plt.savefig(output_path, dpi=140)
print(f"✓ Plot saved successfully!")

plt.close()

# ============================================================================
# STEP 8: WHAT'S HAPPENING UNDER THE HOOD
# ============================================================================

print("\n" + "="*80)
print("STEP 8: HOW COUNTPLOT WORKS UNDER THE HOOD")
print("="*80)

print("\nSeaborn's countplot() performs these steps internally:")
print("\n1. Extract all values from the column:")
all_values = df["listed_in(type)"].tolist()
print(f"   {all_values[:20]}... ({len(all_values)} total)")

print("\n2. For each unique category, count occurrences:")
manual_counts = {}
for category in order:
    count = (df["listed_in(type)"] == category).sum()
    manual_counts[category] = count
    print(f"   {category}: {count}")

print("\n3. Map categories to bar positions and heights:")
for i, category in enumerate(order):
    count = manual_counts[category]
    print(f"   Bar {i} at x={i}, height={count}, label='{category}'")

print("\n4. matplotlib draws rectangles for each bar:")
print("   ┌──────────────────────────────────────────────┐")
for category in order:
    count = manual_counts[category]
    print(f"   │ {category:14s}: {count:4d}                           │")
print("   └──────────────────────────────────────────────┘")

# ============================================================================
# STEP 9: SUMMARY AND INSIGHTS
# ============================================================================

print("\n" + "="*80)
print("STEP 9: SUMMARY AND INSIGHTS")
print("="*80)

max_type = type_counts.index[0]
max_count = type_counts.iloc[0]
min_type = type_counts.index[-1]
min_count = type_counts.iloc[-1]

print(f"\nKey Findings:")
print(f"  • Total restaurants: {len(df)}")
print(f"  • Number of types: {len(type_counts)}")
print(f"\nMost common type: {max_type}")
print(f"  - Count: {max_count}")
print(f"  - Percentage: {(max_count/len(df)*100):.1f}%")

print(f"\nLeast common type: {min_type}")
print(f"  - Count: {min_count}")
print(f"  - Percentage: {(min_count/len(df)*100):.1f}%")

print(f"\nData spread:")
print(f"  - Max to Min ratio: {max_count/min_count:.2f}x")
print(f"  - Difference: {max_count - min_count} restaurants")

print("\nInterpretation:")
print(f"  The distribution is relatively balanced, with {max_type}")
print(f"  being the most prevalent ({(max_count/len(df)*100):.1f}%) and {min_type}")
print(f"  being the least prevalent ({(min_count/len(df)*100):.1f}%). This suggests a diverse")
print(f"  restaurant market with multiple viable categories.")

# ============================================================================
# STEP 10: CODE COMPLEXITY ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("STEP 10: CODE COMPLEXITY ANALYSIS")
print("="*80)

print("\nOperation Complexity:")
print(f"  1. pd.read_csv():        O(n)     - read each row once")
print(f"  2. df['column']:         O(1)     - column access")
print(f"  3. .value_counts():      O(n)     - iterate to count")
print(f"  4. .unique():            O(n)     - scan for uniqueness")
print(f"  5. sns.countplot():      O(n)     - process all rows for plot")
print(f"  6. plt.savefig():        O(1)     - write file (size independent)")
print(f"\nTotal time complexity: O(n) where n={len(df)} rows")
print(f"Total space complexity: O(m) where m={len(type_counts)} unique values")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\nVisualization saved to: {output_path}")
print("\nYou can now view the generated chart to see the distribution.")
