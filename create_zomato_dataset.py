import argparse
import csv
import random
from pathlib import Path


RESTAURANT_TYPES = ["Dining", "Cafe", "Buffet", "Desserts", "Quick Bites", "Casual Dining"]
AREAS = ["MP Nagar", "Arera Colony", "Kolar Road", "Bairagarh", "TT Nagar", "Indrapuri"]
NAME_ROOTS = ["Spice", "Urban", "Royal", "Green", "Blue", "Tandoor", "Saffron", "Fusion"]
NAME_SUFFIXES = ["Kitchen", "Cafe", "Bistro", "House", "Corner", "Dine", "Hub", "Treats"]

# Type-driven probabilities for online ordering and rough cost/rating behavior.
TYPE_PROFILE = {
    "Dining": {"online_yes": 0.30, "cost_range": (300, 900), "rating_base": 3.7, "votes_range": (80, 450)},
    "Cafe": {"online_yes": 0.75, "cost_range": (200, 600), "rating_base": 3.9, "votes_range": (60, 320)},
    "Buffet": {"online_yes": 0.20, "cost_range": (600, 1400), "rating_base": 3.8, "votes_range": (50, 280)},
    "Desserts": {"online_yes": 0.65, "cost_range": (150, 500), "rating_base": 3.8, "votes_range": (40, 250)},
    "Quick Bites": {"online_yes": 0.70, "cost_range": (120, 450), "rating_base": 3.6, "votes_range": (45, 300)},
    "Casual Dining": {"online_yes": 0.45, "cost_range": (350, 1000), "rating_base": 3.8, "votes_range": (70, 380)},
}

FIELDNAMES = [
    "name",
    "location",
    "listed_in(type)",
    "online_order",
    "votes",
    "rate",
    "approx_cost(for two people)",
]


def generate_dataset(
    output_path: Path,
    row_count: int = 500,
    seed: int = 42,
    preview_rows: int = 10,
    print_preview: bool = True,
) -> list[dict]:
    """Generate a synthetic Zomato-style dataset and save it as CSV."""
    random.seed(seed)
    rows = []

    for i in range(1, row_count + 1):
        rtype = random.choice(RESTAURANT_TYPES)
        profile = TYPE_PROFILE[rtype]

        name = f"{random.choice(NAME_ROOTS)} {random.choice(NAME_SUFFIXES)} {i}"
        location = random.choice(AREAS)
        online_order = "Yes" if random.random() < profile["online_yes"] else "No"
        votes = random.randint(*profile["votes_range"])

        rating = profile["rating_base"] + random.uniform(-0.5, 0.6)
        rating = max(2.8, min(4.9, round(rating, 1)))
        rate = f"{rating}/5"

        cost = random.randint(*profile["cost_range"])
        cost = int(round(cost / 50) * 50)

        rows.append(
            {
                "name": name,
                "location": location,
                "listed_in(type)": rtype,
                "online_order": online_order,
                "votes": votes,
                "rate": rate,
                "approx_cost(for two people)": cost,
            }
        )

    with output_path.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    if print_preview:
        print(f"Created dataset: {output_path}")
        print(f"Rows: {len(rows)}")
        print("\nSample rows:")
        for row in rows[:preview_rows]:
            print(row)

    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic Zomato dataset")
    parser.add_argument("--rows", type=int, default=500, help="Number of rows to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible data")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "zomato_synthetic_dataset.csv",
        help="Output CSV path",
    )
    parser.add_argument("--preview-rows", type=int, default=10, help="Rows to print as preview")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_dataset(
        output_path=args.output,
        row_count=args.rows,
        seed=args.seed,
        preview_rows=args.preview_rows,
        print_preview=True,
    )
