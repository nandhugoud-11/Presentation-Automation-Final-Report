"""Automated data pipeline.

Steps: load raw data -> clean -> save processed data -> calculate KPIs -> export to Excel.
Run:  python pipeline.py
Edit the CONFIG section to match your own dataset.
"""
import logging
from pathlib import Path

import pandas as pd

# ----------------------------- CONFIG ---------------------------------------
BASE_DIR = Path(__file__).parent
RAW_PATH = BASE_DIR / "data" / "raw" / "sales_data.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "cleaned_data.csv"
REPORT_PATH = BASE_DIR / "output" / "kpi_report.xlsx"

SALES_COL = "sales"        # main numeric metric (after cleaning: lower_snake_case)
PROFIT_COL = "profit"      # optional, set to None if you have no profit column
GROUP_COLS = ["region", "category"]  # columns for breakdown tables (optional)
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger("pipeline")


def load_data(path: Path) -> pd.DataFrame:
    """Load raw CSV data."""
    if not path.exists():
        raise FileNotFoundError(f"Raw data not found: {path}")
    df = pd.read_csv(path)
    log.info("Loaded %d rows, %d columns from %s", *df.shape, path.name)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise columns, remove duplicates, fix text, handle missing values."""
    start = len(df)
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
    df = df.drop_duplicates()

    for col in df.select_dtypes(include=["object", "string"]):
        df[col] = df[col].str.strip().str.title()

    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    cat_cols = df.select_dtypes(include=["object", "string"]).columns
    df[cat_cols] = df[cat_cols].fillna("Unknown")

    log.info("Cleaning done: %d -> %d rows", start, len(df))
    return df


def save_processed(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    log.info("Processed data saved to %s", path)


def calculate_kpis(df: pd.DataFrame):
    """Return (summary KPI table, dict of breakdown tables)."""
    rows = [("Total Records", len(df))]
    if SALES_COL in df:
        rows += [
            ("Total Sales", round(df[SALES_COL].sum(), 2)),
            ("Average Sales per Record", round(df[SALES_COL].mean(), 2)),
        ]
    if PROFIT_COL and PROFIT_COL in df:
        rows.append(("Total Profit", round(df[PROFIT_COL].sum(), 2)))
        if SALES_COL in df and df[SALES_COL].sum() != 0:
            margin = df[PROFIT_COL].sum() / df[SALES_COL].sum() * 100
            rows.append(("Profit Margin (%)", round(margin, 2)))
    summary = pd.DataFrame(rows, columns=["KPI", "Value"])

    breakdowns = {}
    metrics = [c for c in (SALES_COL, PROFIT_COL) if c and c in df]
    for g in GROUP_COLS:
        if g in df and metrics:
            breakdowns[f"By {g.title()}"] = (
                df.groupby(g)[metrics].sum().round(2).sort_values(metrics[0], ascending=False).reset_index()
            )
    return summary, breakdowns


def export_excel(df, summary, breakdowns, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="KPIs", index=False)
        for name, table in breakdowns.items():
            table.to_excel(writer, sheet_name=name[:31], index=False)
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)
        for ws in writer.book.worksheets:  # auto-fit column widths
            for col in ws.columns:
                width = max(len(str(c.value)) if c.value is not None else 0 for c in col[:200])
                ws.column_dimensions[col[0].column_letter].width = min(width + 2, 40)
    log.info("Excel report exported to %s", path)


def main() -> None:
    raw = load_data(RAW_PATH)
    clean = clean_data(raw)
    save_processed(clean, PROCESSED_PATH)
    summary, breakdowns = calculate_kpis(clean)
    export_excel(clean, summary, breakdowns, REPORT_PATH)
    log.info("Pipeline finished successfully.\n%s", summary.to_string(index=False))


if __name__ == "__main__":
    main()
