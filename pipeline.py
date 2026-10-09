"""Drug Tariff pipeline: monthly NHSBSA files -> SQLite -> dashboard.json

Put one file per month in data/raw/, named with the month, e.g. drug_tariff_2026-10.csv
(.csv or .xlsx). Optional extras:
  data/raw/concessions_2026-10.csv   price concession list with a product-name column
  data/portfolio.txt                 one product-name fragment per line (Dr. Reddy's products)
Run:  python drug_tariff_pipeline.py
"""
import json
import os
import re
import sqlite3
from pathlib import Path

import pandas as pd

DATA = Path(os.environ.get("DATA_DIR", "data"))
RAW, DB, OUT, PORTFOLIO = DATA / "raw", DATA / "tariff.db", DATA / "dashboard.json", DATA / "portfolio.txt"
PRICE_IN_PENCE = True   # Drug Tariff prices are published in pence; set False if your file is in pounds
MAX_PRODUCTS = 60       # dashboard lane stays readable: portfolio first, then biggest movers

# Header names vary between releases. Extend these lists to match your files.
COLS = {
    "product": ["medicine", "product", "drug name"],
    "pack": ["pack size", "pack"],
    "category": ["drug tariff category", "category"],
    "price": ["basic price", "price"],
}


def month_of(path: Path) -> str:
    m = re.search(r"(\d{4})[-_]?(\d{2})", path.stem)
    if not m:
        raise ValueError(f"No YYYY-MM in file name: {path.name}")
    return f"{m[1]}-{m[2]}"


def read(path: Path) -> pd.DataFrame:
    return pd.read_excel(path) if path.suffix in (".xlsx", ".xls") else pd.read_csv(path)


def find(df: pd.DataFrame, names: list) -> str:
    lower = {c.lower().strip(): c for c in df.columns}
    for n in names:
        for k, c in lower.items():
            if n in k:
                return c
    raise KeyError(f"None of {names} found in columns {list(df.columns)}")


def load():
    rows, conc = [], []
    for p in sorted(RAW.glob("*")):
        if p.suffix not in (".csv", ".xlsx", ".xls"):
            continue
        df, month = read(p), month_of(p)
        if "concession" in p.name.lower():
            conc.append(pd.DataFrame({"month": month, "product": df[find(df, COLS["product"])].astype(str).str.strip()}))
            continue
        rows.append(pd.DataFrame({
            "month": month,
            "product": df[find(df, COLS["product"])].astype(str).str.strip(),
            "pack": df[find(df, COLS["pack"])].astype(str).str.strip(),
            "category": df[find(df, COLS["category"])].astype(str).str.strip().str[-1].str.upper(),
            "price": pd.to_numeric(df[find(df, COLS["price"])], errors="coerce") / (100 if PRICE_IN_PENCE else 1),
        }))
    if not rows:
        raise FileNotFoundError("No tariff files found yet. Upload a monthly Drug Tariff file first.")
    return pd.concat(rows), (pd.concat(conc) if conc else pd.DataFrame(columns=["month", "product"]))


def build(prices: pd.DataFrame, conc: pd.DataFrame) -> pd.DataFrame:
    prices = prices.dropna(subset=["price"])
    prices = prices[prices.category.isin(list("ACM"))].copy()
    prices["key"] = prices["product"] + "|" + prices["pack"]
    prices = prices.drop_duplicates(["month", "key"]).sort_values(["key", "month"])
    flagged = set(zip(conc["month"], conc["product"].str.lower()))
    prices["concession"] = [(m, p.lower()) in flagged for m, p in zip(prices["month"], prices["product"])]
    g = prices.groupby("key")
    prices["mom_change"] = g["price"].pct_change()
    prices["category_changed"] = g["category"].shift().notna() & g["category"].shift().ne(prices["category"])
    return prices


def export(prices: pd.DataFrame) -> dict:
    terms = [t.strip().lower() for t in PORTFOLIO.read_text().splitlines() if t.strip()] if PORTFOLIO.exists() else []
    months = sorted(prices["month"].unique())
    wide = lambda col: prices.pivot(index="key", columns="month", values=col).reindex(columns=months)
    price, cat = wide("price").ffill(axis=1).bfill(axis=1), wide("category").ffill(axis=1).bfill(axis=1)
    con = wide("concession").fillna(False)
    meta = prices.drop_duplicates("key").set_index("key")
    in_pf = lambda k: any(t in meta.at[k, "product"].lower() for t in terms)
    movers = prices.groupby("key")["mom_change"].last().abs().fillna(0).sort_values(ascending=False)
    keys = [k for k in price.index if in_pf(k)] + [k for k in movers.index if not in_pf(k)]
    products = [{
        "n": meta.at[k, "product"], "pk": meta.at[k, "pack"], "pf": in_pf(k),
        "pr": [round(float(v), 2) for v in price.loc[k]],
        "ct": [str(v) for v in cat.loc[k]],
        "cn": [bool(v) for v in con.loc[k]],
    } for k in keys[:MAX_PRODUCTS]]
    return {"months": [pd.to_datetime(m).strftime("%b %y") for m in months], "products": products}


def run() -> str:
    prices = build(*load())
    DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as con:
        prices.drop(columns="key").to_sql("prices", con, if_exists="replace", index=False)
    OUT.write_text(json.dumps(export(prices)))
    return f"Processed {prices['key'].nunique()} products across {prices['month'].nunique()} months."


if __name__ == "__main__":
    print(run())
