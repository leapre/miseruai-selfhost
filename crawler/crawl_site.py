#!/usr/bin/env python3
"""
サイトマップを再帰的にたどり、本文を trafilatura で抽出して
data/corpus.jsonl に保存する。
BASE URL は (優先度) argv1 > 環境変数 SITE_BASE > デフォルト
"""
import os, sys, json, pathlib, requests, tqdm, trafilatura, xml.etree.ElementTree as ET

# ───────────── 設定 ─────────────
BASE = (
    sys.argv[1]                    # 1. コマンドライン引数
    if len(sys.argv) > 1 else
    os.getenv("SITE_BASE")         # 2. Workflow から渡す環境変数
    or "https://example.com"       # 3. デフォルト (ローカルテスト用)
)
SITEMAP_URL = f"{BASE.rstrip('/')}/sitemap.xml"
OUT_FILE    = pathlib.Path("data/corpus.jsonl")
OUT_FILE.parent.mkdir(exist_ok=True)

# ───── サイトマップ再帰取得 ─────
def parse_sitemap(url: str) -> list[str]:
    xml_text = requests.get(url, timeout=10).text
    root = ET.fromstring(xml_text)
    locs = [loc.text for loc in root.iterfind(".//{*}loc")]

    if root.tag.endswith("sitemapindex"):
        urls = []
        for child in locs:
            urls.extend(parse_sitemap(child))   # 再帰
        return urls
    return locs

# ───── メイン処理 ─────
if __name__ == "__main__":
    urls = parse_sitemap(SITEMAP_URL)
    print(f"🌐 {len(urls)} URLs found @ {BASE}")

    with OUT_FILE.open("w", encoding="utf-8") as fh:
        for url in tqdm.tqdm(urls, desc="crawl"):
            html = trafilatura.fetch_url(url)
            if not html:
                continue
            text = trafilatura.extract(html, include_comments=False, include_tables=False)
            if text and len(text) > 200:
                fh.write(json.dumps({"url": url, "text": text}, ensure_ascii=False) + "\n")

    size_kb = OUT_FILE.stat().st_size / 1024
    print(f"✅ saved {OUT_FILE.resolve()} ({size_kb:.1f} KB)")

