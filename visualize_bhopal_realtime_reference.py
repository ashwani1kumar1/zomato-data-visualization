from __future__ import annotations

import re
from pathlib import Path

import matplotlib
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).parent
RAW_PATH = BASE_DIR / "bhopal_realtime_reference_raw.txt"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)


def parse_reviews_count(text: str) -> int:
    token = text.strip().upper().replace(",", "")
    if token.endswith("K"):
        return int(float(token[:-1]) * 1000)
    return int(float(token))


def infer_locality(address: str) -> str:
    key_map = {
        "shyamla hills": "Shyamla Hills",
        "hamidia": "Hamidia Road",
        "mp nagar": "MP Nagar",
        "shahpura": "Shahpura",
        "vip road": "VIP Road",
        "rohit nagar": "Rohit Nagar",
        "gulmohar": "Gulmohar",
        "narmadapuram": "Narmadapuram Road",
        "kerwa": "Kerwa Road",
        "kohefiza": "Kohefiza",
        "lalghati": "Lalghati",
        "airport rd": "Airport Road",
        "sultania": "Sultania Road",
        "jk rd": "JK Road",
        "jumerati": "Jumerati",
        "bypass road": "Bypass Road",
        "iqbal maidan": "Iqbal Maidan",
        "vanvihar": "Van Vihar Road",
        "service road": "Service Road",
        "minto hall": "Minto Hall",
        "model ground": "Model Ground",
        "karbala": "Karbala Road",
    }
    lowered = address.lower()
    for needle, locality in key_map.items():
        if needle in lowered:
            return locality
    return "Other Bhopal"


def parse_blocks(raw_text: str) -> pd.DataFrame:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", raw_text) if b.strip()]
    rows: list[dict] = []

    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 3:
            continue

        name = lines[0]
        meta = lines[1]
        address = lines[2]

        rating_match = re.search(r"(\d\.\d)\(([^\)]+)\)", meta)
        if not rating_match:
            continue

        rating = float(rating_match.group(1))
        reviews = parse_reviews_count(rating_match.group(2))

        parts = [p.strip() for p in meta.split("·") if p.strip()]
        cuisine = parts[-1] if parts else "Unknown"

        # Proxy score gives more weight to restaurants with both high rating and high review count.
        popularity_score = round(rating * reviews, 2)

        rows.append(
            {
                "name": name,
                "rating": rating,
                "reviews": reviews,
                "cuisine": cuisine,
                "address": address,
                "locality": infer_locality(address),
                "popularity_score": popularity_score,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    raw_text = RAW_PATH.read_text(encoding="utf-8")
    df = parse_blocks(raw_text)

    if df.empty:
        raise RuntimeError("No rows parsed from realtime reference data.")

    parsed_path = OUT_DIR / "10_bhopal_realtime_parsed_restaurants.csv"
    df.to_csv(parsed_path, index=False)

    locality_summary = (
        df.groupby("locality", as_index=False)
        .agg(
            restaurants=("name", "count"),
            avg_rating=("rating", "mean"),
            total_reviews=("reviews", "sum"),
            popularity_score=("popularity_score", "sum"),
        )
        .sort_values("popularity_score", ascending=False)
    )
    locality_summary["avg_rating"] = locality_summary["avg_rating"].round(2)

    summary_path = OUT_DIR / "10_bhopal_realtime_locality_summary.csv"
    locality_summary.to_csv(summary_path, index=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=locality_summary,
        x="locality",
        y="popularity_score",
        color="#4daf4a",
    )
    plt.title("Bhopal Realtime Reference: Locality vs Popularity")
    plt.xlabel("Locality")
    plt.ylabel("Popularity score (rating × reviews)")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    chart_path = OUT_DIR / "10_bhopal_realtime_locality_vs_popularity.png"
    plt.savefig(chart_path, dpi=140)
    plt.close()

    avg_rating_plot_data = locality_summary.sort_values("avg_rating", ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=avg_rating_plot_data,
        x="locality",
        y="avg_rating",
        color="#377eb8",
    )
    plt.title("Bhopal Realtime Reference: Locality vs Average Rating")
    plt.xlabel("Locality")
    plt.ylabel("Average rating")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    avg_rating_chart_path = OUT_DIR / "11_bhopal_realtime_locality_vs_avg_rating.png"
    plt.savefig(avg_rating_chart_path, dpi=140)
    plt.close()

    reviews_plot_data = locality_summary.sort_values("total_reviews", ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=reviews_plot_data,
        x="locality",
        y="total_reviews",
        color="#ff7f00",
    )
    plt.title("Bhopal Realtime Reference: Locality vs Total Reviews")
    plt.xlabel("Locality")
    plt.ylabel("Total reviews")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    total_reviews_chart_path = OUT_DIR / "12_bhopal_realtime_locality_vs_total_reviews.png"
    plt.savefig(total_reviews_chart_path, dpi=140)
    plt.close()

    print(f"Parsed rows: {len(df)}")
    print(f"Saved parsed data: {parsed_path}")
    print(f"Saved locality summary: {summary_path}")
    print(f"Saved chart: {chart_path}")
    print(f"Saved chart: {avg_rating_chart_path}")
    print(f"Saved chart: {total_reviews_chart_path}")
    print("\nTop localities by popularity score:")
    print(locality_summary.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
