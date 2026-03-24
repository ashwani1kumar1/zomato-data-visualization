import argparse
from datetime import datetime
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

# Use a non-interactive backend so plots can be generated in any environment.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from create_zomato_dataset import generate_dataset


BASE_DIR = Path(__file__).parent



def section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)



def save_plot(filename: str) -> None:
    plot_path = OUTPUT_DIR / filename
    plt.tight_layout()
    plt.savefig(plot_path, dpi=140)
    plt.close()
    print(f"Saved plot -> {plot_path}")



def handle_rate(value) -> float:
    """Convert ratings like '4.1/5' into numeric float values such as 4.1."""
    value = str(value).strip()
    if "/" in value:
        value = value.split("/")[0]
    return float(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run detailed Zomato data analysis")
    parser.add_argument(
        "--input",
        type=Path,
        default=BASE_DIR / "zomato_synthetic_dataset.csv",
        help="Input dataset CSV path",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=BASE_DIR / "outputs",
        help="Directory where plots and report will be saved",
    )
    parser.add_argument(
        "--cleaned-output",
        type=Path,
        default=BASE_DIR / "zomato_synthetic_dataset_cleaned.csv",
        help="Path to save the cleaned dataset",
    )
    parser.add_argument("--rows", type=int, default=500, help="Rows for generation when dataset is missing or regenerated")
    parser.add_argument("--seed", type=int, default=42, help="Random seed used for dataset generation")
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="Regenerate the synthetic input dataset before analysis",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=None,
        help="Markdown report path; default is output-dir/analysis_report.md",
    )
    return parser.parse_args()


def build_report(
    report_path: Path,
    online_yes: int,
    online_no: int,
    most_favored_type_by_votes: str,
    most_common_cost: int,
    max_votes: int,
    restaurants_with_max_votes: pd.DataFrame,
    grouped_votes: pd.DataFrame,
    locality_sales: pd.DataFrame,
    locality_avg_sales: pd.DataFrame,
    pivot_table: pd.DataFrame,
    cleaned_path: Path,
    dataset_path: Path,
) -> None:
    max_votes_table = restaurants_with_max_votes.to_string(index=False)
    grouped_votes_table = grouped_votes.to_string(index=False)
    locality_sales_table = locality_sales.to_string(index=False)
    locality_avg_sales_table = locality_avg_sales.to_string(index=False)
    pivot_table_text = pivot_table.to_string()

    report_lines = [
        "# Zomato Synthetic Data Analysis Report",
        "",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Input dataset: {dataset_path}",
        f"Cleaned dataset: {cleaned_path}",
        "",
        "## Key Business Answers",
        "",
        "1. Do more restaurants provide online delivery compared to offline services?",
        f"   - Online: {online_yes}",
        f"   - Offline-only: {online_no}",
        "",
        "2. Which types of restaurants are most favored by the general public?",
        f"   - Most favored by total votes: {most_favored_type_by_votes}",
        "",
        "3. What price range do couples prefer for dining out?",
        f"   - Most frequent approx cost for two: {most_common_cost}",
        "",
        "## Most Voted Restaurant",
        "",
        f"Maximum votes: {max_votes}",
        "```text",
        max_votes_table,
        "```",
        "",
        "## Votes by Restaurant Type",
        "",
        "```text",
        grouped_votes_table,
        "```",
        "",
        "## Locality vs Sales (Votes Proxy)",
        "",
        "Using total votes by locality as a proxy for sales/engagement.",
        "```text",
        locality_sales_table,
        "```",
        "",
        "## Locality vs Sales (Average Votes per Restaurant)",
        "",
        "Normalized view: average votes per restaurant in each locality.",
        "```text",
        locality_avg_sales_table,
        "```",
        "",
        "## Type vs Online Order Preference",
        "",
        "```text",
        pivot_table_text,
        "```",
        "",
        "## Output Visuals",
        "",
        "- 01_restaurant_type_count.png",
        "- 02_votes_by_type_line.png",
        "- 03_online_order_count.png",
        "- 04_rating_distribution.png",
        "- 05_couple_cost_distribution.png",
        "- 06_rating_boxplot_online_vs_offline.png",
        "- 07_heatmap_type_vs_order_mode.png",
        "- 08_locality_vs_sales.png",
        "- 09_locality_avg_sales_per_restaurant.png",
    ]
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Saved report -> {report_path}")


def main() -> None:
    args = parse_args()

    dataset_path = args.input
    output_dir = args.output_dir
    output_dir.mkdir(exist_ok=True)

    global OUTPUT_DIR
    OUTPUT_DIR = output_dir

    section("Step 1: Importing necessary Python libraries")
    print("Libraries imported: pandas, numpy, matplotlib, seaborn")
    print("Purpose:")
    print("- pandas/numpy: data processing")
    print("- matplotlib/seaborn: data visualization")

    section("Step 2: Reading dataset into DataFrame")
    if args.regenerate or not dataset_path.exists():
        reason = "regenerate flag enabled" if args.regenerate else "dataset not found"
        print(f"Dataset generation triggered because: {reason}")
        generate_dataset(
            output_path=dataset_path,
            row_count=args.rows,
            seed=args.seed,
            preview_rows=5,
            print_preview=False,
        )
        print(f"Generated dataset at: {dataset_path}")

    df = pd.read_csv(dataset_path)
    print(f"Dataset loaded from: {dataset_path}")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())

    section("Step 3: Data Cleaning and Preparation")
    print("3.1 Converting 'rate' column from text (e.g., 4.1/5) to float")
    df["rate"] = df["rate"].apply(handle_rate)

    print("3.2 Cleaning and converting 'approx_cost(for two people)' to integer")
    df["approx_cost(for two people)"] = (
        df["approx_cost(for two people)"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(int)
    )

    print("3.3 Normalizing categorical text values")
    df["listed_in(type)"] = df["listed_in(type)"].astype(str).str.strip()
    df["online_order"] = df["online_order"].astype(str).str.strip().str.title()

    print("\nData types after cleaning:")
    print(df.dtypes)
    print("\nDataset summary:")
    print(df.info())
    print("\nMissing values per column:")
    print(df.isnull().sum())

    # Light sanity checks for reliable analysis.
    assert set(df["online_order"].unique()).issubset({"Yes", "No"}), "Unexpected online_order values found"
    assert df["rate"].between(0, 5).all(), "Rate values out of expected 0-5 range"
    assert (df["approx_cost(for two people)"] > 0).all(), "Cost must be positive"

    cleaned_path = args.cleaned_output
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cleaned_path, index=False)
    print(f"\nCleaned dataset saved -> {cleaned_path}")

    section("Step 4: Exploring Restaurant Types")
    print("Goal: identify which restaurant categories are most common.")

    plt.figure(figsize=(10, 5))
    order = df["listed_in(type)"].value_counts().index
    sns.countplot(x=df["listed_in(type)"], order=order, color="#66c2a5")
    plt.xlabel("Type of restaurant")
    plt.ylabel("Count")
    plt.title("Restaurant Type Distribution")
    plt.xticks(rotation=25)
    save_plot("01_restaurant_type_count.png")

    print("Restaurant type counts:")
    print(df["listed_in(type)"].value_counts())
    print("Interpretation: The category with the highest count is the most prevalent in this dataset.")

    section("Step 5: Votes by Restaurant Type")
    print("Goal: identify which type receives the highest public engagement via votes.")

    grouped_votes = (
        df.groupby("listed_in(type)", as_index=False)["votes"].sum().sort_values("votes", ascending=False)
    )

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=grouped_votes, x="listed_in(type)", y="votes", marker="o", color="green")
    plt.xlabel("Type of restaurant")
    plt.ylabel("Total votes")
    plt.title("Total Votes by Restaurant Type")
    plt.xticks(rotation=25)
    save_plot("02_votes_by_type_line.png")

    print("Total votes by type:")
    print(grouped_votes)
    print("Interpretation: The type with maximum total votes is most favored by the public in terms of engagement.")

    section("Step 6: Identify the Most Voted Restaurant")
    max_votes = df["votes"].max()
    restaurants_with_max_votes = df.loc[df["votes"] == max_votes, ["name", "listed_in(type)", "votes"]]

    print(f"Maximum votes found: {max_votes}")
    print("Restaurant(s) with maximum votes:")
    print(restaurants_with_max_votes)

    section("Step 7: Online Order Availability")
    print("Goal: compare how many restaurants accept online orders versus offline only.")

    plt.figure(figsize=(6, 5))
    sns.countplot(data=df, x="online_order", color="#8da0cb")
    plt.xlabel("Online order available")
    plt.ylabel("Count")
    plt.title("Online vs Offline Order Availability")
    save_plot("03_online_order_count.png")

    online_counts = df["online_order"].value_counts()
    print("Counts:")
    print(online_counts)

    if "Yes" in online_counts and "No" in online_counts:
        if online_counts["Yes"] > online_counts["No"]:
            print("Interpretation: More restaurants provide online delivery.")
        else:
            print("Interpretation: More restaurants rely on offline service.")

    section("Step 8: Analyze Ratings Distribution")
    print("Goal: understand where most ratings are concentrated.")

    plt.figure(figsize=(8, 5))
    plt.hist(df["rate"], bins=8, color="#377eb8", edgecolor="black")
    plt.title("Ratings Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of restaurants")
    save_plot("04_rating_distribution.png")

    print("Rating statistics:")
    print(df["rate"].describe())
    print("Interpretation: The densest rating range represents where most restaurants are clustered.")

    section("Step 9: Approximate Cost for Couples")
    print("Goal: find the most preferred budget range for dining for two people.")

    plt.figure(figsize=(11, 5))
    cost_order = df["approx_cost(for two people)"].value_counts().sort_index().index
    sns.countplot(data=df, x="approx_cost(for two people)", order=cost_order, color="#fdae61")
    plt.xlabel("Approx cost for two people")
    plt.ylabel("Count")
    plt.title("Preferred Couple Budget Range")
    plt.xticks(rotation=45)
    save_plot("05_couple_cost_distribution.png")

    most_common_cost = int(df["approx_cost(for two people)"].mode().iloc[0])
    print(f"Most common couple cost: {most_common_cost}")
    print("Interpretation: This cost is the most frequently chosen budget range by customers.")

    section("Step 10: Ratings Comparison - Online vs Offline")
    print("Goal: compare rating spread for restaurants with and without online orders.")

    plt.figure(figsize=(7, 6))
    sns.boxplot(data=df, x="online_order", y="rate", color="#fc8d62")
    plt.title("Ratings by Online Order Availability")
    plt.xlabel("Online order")
    plt.ylabel("Rating")
    save_plot("06_rating_boxplot_online_vs_offline.png")

    median_by_mode = df.groupby("online_order")["rate"].median().sort_values(ascending=False)
    print("Median rating by order mode:")
    print(median_by_mode)
    print("Interpretation: Higher median indicates better central rating performance.")

    section("Step 11: Heatmap - Order Mode Preferences by Restaurant Type")
    print("Goal: understand how order preference (Yes/No) changes by restaurant type.")

    pivot_table = df.pivot_table(
        index="listed_in(type)", columns="online_order", aggfunc="size", fill_value=0
    )

    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt="d")
    plt.title("Heatmap: Type vs Online Order Availability")
    plt.xlabel("Online Order")
    plt.ylabel("Restaurant Type")
    save_plot("07_heatmap_type_vs_order_mode.png")

    print("Pivot table used for heatmap:")
    print(pivot_table)

    section("Step 12: Locality vs Sales (Votes Proxy)")
    print("Goal: compare locality-wise sales potential using total votes as a proxy.")

    locality_sales = (
        df.groupby("location", as_index=False)["votes"].sum().sort_values("votes", ascending=False)
    )

    plt.figure(figsize=(10, 5))
    sns.barplot(data=locality_sales, x="location", y="votes", color="#e78ac3")
    plt.title("Locality vs Sales (Total Votes Proxy)")
    plt.xlabel("Locality")
    plt.ylabel("Total votes (sales proxy)")
    plt.xticks(rotation=25)
    save_plot("08_locality_vs_sales.png")

    print("Locality-wise total votes:")
    print(locality_sales)
    print("Interpretation: Higher total votes indicate stronger sales/engagement potential.")

    section("Step 13: Locality vs Normalized Sales")
    print("Goal: compare locality performance after normalizing for restaurant count.")

    locality_avg_sales = (
        df.groupby("location", as_index=False)["votes"].mean().sort_values("votes", ascending=False)
    )
    locality_avg_sales["votes"] = locality_avg_sales["votes"].round(2)

    plt.figure(figsize=(10, 5))
    sns.barplot(data=locality_avg_sales, x="location", y="votes", color="#a6d854")
    plt.title("Locality vs Average Sales (Votes per Restaurant)")
    plt.xlabel("Locality")
    plt.ylabel("Average votes per restaurant")
    plt.xticks(rotation=25)
    save_plot("09_locality_avg_sales_per_restaurant.png")

    print("Locality-wise average votes per restaurant:")
    print(locality_avg_sales)
    print("Interpretation: This controls for locality size and shows per-restaurant performance.")

    section("Final Answers to Business Questions")

    online_yes = int((df["online_order"] == "Yes").sum())
    online_no = int((df["online_order"] == "No").sum())
    print("1) Do more restaurants provide online delivery compared to offline services?")
    if online_yes > online_no:
        print(f"   Yes. Online: {online_yes}, Offline-only: {online_no}")
    else:
        print(f"   No. Offline-only: {online_no}, Online: {online_yes}")

    most_favored_type_by_votes = grouped_votes.iloc[0]["listed_in(type)"]
    print("2) Which types of restaurants are most favored by the general public?")
    print(f"   By total votes, most favored type: {most_favored_type_by_votes}")

    print("3) What price range do couples prefer for dining out?")
    print(f"   Most common approximate cost for two: {most_common_cost}")

    report_path = args.report_path or (output_dir / "analysis_report.md")
    build_report(
        report_path=report_path,
        online_yes=online_yes,
        online_no=online_no,
        most_favored_type_by_votes=most_favored_type_by_votes,
        most_common_cost=most_common_cost,
        max_votes=max_votes,
        restaurants_with_max_votes=restaurants_with_max_votes,
        grouped_votes=grouped_votes,
        locality_sales=locality_sales,
        locality_avg_sales=locality_avg_sales,
        pivot_table=pivot_table,
        cleaned_path=cleaned_path,
        dataset_path=dataset_path,
    )

    print("\nAnalysis complete. All visual outputs and report are saved in the output folder.")


if __name__ == "__main__":
    main()
