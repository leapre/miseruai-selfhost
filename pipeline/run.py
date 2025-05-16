import os, requests, json, datetime

WP_URL  = os.environ["WP_URL"]
WP_USER = os.environ["WP_USER"]
WP_PASS = os.environ["WP_PASS"]
KW      = os.environ.get("KW", "テストキーワード")

# 例：OpenAI に依存しない最小テンプレ（記事は固定）
title = f"Hello, MiseruAI! {datetime.date.today()}"
content = f"{KW} に関するテスト投稿（{datetime.datetime.now()}）"

payload = {
    "title":   title,
    "content": content,
    "status":  "draft"
}

r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts",
                  json=payload,
                  auth=(WP_USER, WP_PASS))

print("STATUS", r.status_code)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))
if r.status_code != 201:
    raise SystemExit("投稿失敗")

r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts",
                  json=payload,
                  auth=(WP_USER, WP_PASS))

print("STATUS", r.status_code)
print("BODY  :", r.text)           # ← 追加
r.raise_for_status()               # 4xx/5xx で例外

print("STATUS:", r.status_code)
print("RAW  :", r.text[:500])          # 最初の 500 文字だけ表示
try:
    j = r.json()
    print("PARSED:", json.dumps(j, indent=2, ensure_ascii=False))
except ValueError:
    print("※JSON ではありません")
