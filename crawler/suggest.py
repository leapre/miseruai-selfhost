#!/usr/bin/env python3
import csv, json, time, itertools, requests, os, sys
from datetime import date

BASE   = "https://suggestqueries.google.com/complete/search"
HEAD   = {"User-Agent": "Mozilla/5.0"}
SEED = os.getenv("SEED_KW") or "転職 小売業"  # ← 空文字もフォールバック
OUTDIR = "data"
os.makedirs(OUTDIR, exist_ok=True)
OUTCSV = f"{OUTDIR}/keywords_{date.today()}.csv"

def fetch(term: str) -> list[str]:
    """Googleサジェストを取得してリストで返す"""
    try:
        r = requests.get(BASE,
                         params={"client": "firefox", "hl": "ja", "q": term},
                         headers=HEAD, timeout=10)
        return json.loads(r.text)[1]
    except Exception as e:
        print(f"⚠️  {term}: {e}", file=sys.stderr)
        return []

print(f"🔍 Seed = {SEED}")
seen = set()
with open(OUTCSV, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["keyword"])

    for suffix in itertools.chain("", list("abcdefghijklmnopqrstuvwxyz")):
        kw = f"{SEED} {suffix}".strip()
        for s in fetch(kw):
            if s not in seen:
                w.writerow([s])
                seen.add(s)
        time.sleep(1)        # 1秒スリープでブロック回避

print(f"✅ {len(seen)} keywords saved to {OUTCSV}")

