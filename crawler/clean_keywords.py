#!/usr/bin/env python3
import csv, sys, pathlib

# === 入出力ファイル ===
latest_csv = sorted(pathlib.Path("data").glob("keywords_*.csv"))[-1]
out_csv    = pathlib.Path("data/clean_keywords.csv")
ng_file    = pathlib.Path("crawler/ng_words.txt")

# === NG ワードセット ===
ng_words = {w.strip() for w in ng_file.read_text(encoding="utf-8").splitlines() if w.strip()}

seen   = set()
kept   = []

with latest_csv.open(encoding="utf-8") as f:
    rdr = csv.reader(f)
    next(rdr)  # skip header
    for row in rdr:
        kw = row[0].strip()
        if kw in seen:
            continue
        if any(ng in kw for ng in ng_words):
            continue
        seen.add(kw)
        kept.append([kw])

out_csv.write_text("keyword\n", encoding="utf-8")
with out_csv.open("a", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerows(kept)

print(f"✅ {len(kept)} keywords kept → {out_csv}")
