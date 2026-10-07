"""Creates a small, messy sample dataset so the pipeline runs out of the box.
Replace data/raw/sales_data.csv with your own dataset (e.g. the one from Task 3)."""
import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
n = 500
df = pd.DataFrame({
    "Order ID": range(1001, 1001 + n),
    "Order Date": pd.date_range("2025-01-01", periods=n, freq="D").strftime("%Y-%m-%d"),
    "Region": rng.choice(["North", "South", "East", "West", " east", "WEST "], n),
    "Category": rng.choice(["Electronics", "Furniture", "Clothing", "Grocery"], n),
    "Quantity": rng.integers(1, 10, n).astype(float),
    "Sales": rng.normal(250, 90, n).round(2),
    "Profit": rng.normal(45, 30, n).round(2),
})
# inject common data problems: missing values and duplicates
df.loc[rng.choice(n, 15, replace=False), "Sales"] = np.nan
df.loc[rng.choice(n, 10, replace=False), "Region"] = np.nan
df = pd.concat([df, df.sample(8, random_state=1)], ignore_index=True)

out = Path(__file__).parent / "data" / "raw" / "sales_data.csv"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False)
print(f"Sample data written to {out}")
