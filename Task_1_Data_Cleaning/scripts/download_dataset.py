from pathlib import Path
from ucimlrepo import fetch_ucirepo

OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

print("Fetching UCI Online Retail II...")
dataset = fetch_ucirepo(id=502)

# UCI exposes the data as pandas DataFrames.
# Online Retail II can contain more than one year/file; concatenate available frames.
frames = []
if hasattr(dataset.data, "features") and dataset.data.features is not None:
    frames.append(dataset.data.features)

if not frames:
    raise RuntimeError("No feature dataframe was returned by UCI.")

import pandas as pd
df = pd.concat(frames, ignore_index=True)

path = OUT / "online_retail_ii_raw.csv"
df.to_csv(path, index=False)
print(f"Saved {len(df):,} rows to {path}")
