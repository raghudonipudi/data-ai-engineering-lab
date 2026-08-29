"""
Exercise 6: Pandas ETL - Sanitize, Normalize, Aggregate
See README.md in this folder for the full task description.

Fill in the functions below. Run with:
    python exercise.py
"""

import pandas as pd

INPUT_FILE = "raw_orders.csv"
CLEAN_ORDERS_FILE = "clean_orders.csv"
SUMMARY_FILE = "region_month_summary.csv"

def load_raw(path):
    """Read raw_orders.csv into a DataFrame."""
    df = pd.read_csv(path)
    return df


def sanitize(df):
    """
    Trim whitespace and standardize casing on customer_name/region,
    drop duplicate order_ids, drop rows with unusable price or
    quantity <= 0. Print what got dropped and why.
    """

    df["customer_name"] = df["customer_name"].str.strip().str.lower().str.title()
    df["region"] = df["region"].str.strip().str.lower().str.title()
    bad_dup_df = df[df.duplicated(subset=["order_id"], keep="first")]
    df = df.drop_duplicates(subset=["order_id"])
    df["price"] = df["price"].str.strip().str.replace(",", "", regex=False).str.replace("$", "", regex=False)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    bad_price_df = df[df["price"].isna()]
    df = df.dropna(subset=["price"])
    bad_quantity_df = df[df["quantity"] <= 0]
    df = df[df["quantity"] > 0]

    bad_rows = pd.concat([bad_dup_df, bad_price_df, bad_quantity_df])
    for idx, row in bad_rows.iterrows():
        if row["order_id"] in bad_dup_df["order_id"].values:
            print(f"{row["order_id"]} dropped due to duplicates")
        elif row["order_id"] in bad_price_df["order_id"].values:
            print(f"{row["order_id"]} dropped due to wrong price values")
        elif row["order_id"] in bad_quantity_df["order_id"].values:
            print(f"{row["order_id"]} dropped due to wrong quantity values")

    return df


def normalize(df):
    """
    Convert price to numeric, parse order_date into a single consistent
    date type (handle both input formats), add a computed total column.
    """
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")
    df["total"] = df["price"] * df["quantity"]
    return df


def aggregate(df):
    """Return total `total` revenue grouped by region and month."""
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month

    agg_df = df.groupby(["region", "year", "month"]).agg(total = ("total", "sum")).reset_index()
    return agg_df


def main():
    raw = load_raw(INPUT_FILE)
    clean = sanitize(raw)
    normalized = normalize(clean)
    normalized.to_csv(CLEAN_ORDERS_FILE, index=False)
    summary = aggregate(normalized)
    summary.to_csv(SUMMARY_FILE, index=False)
    print(summary)


if __name__ == "__main__":
    main()
