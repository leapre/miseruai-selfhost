import os, requests, json, datetime

WP_URL  = os.environ["WP_URL"]
WP_USER = os.environ["WP_USER"]
WP_PASS = os.environ["WP_PASS"]
KW      = os.environ.get("KW", "テストキーワード")

# -------------------------------
# 投稿データ（固定テキストで十分）
# -------------------------------
title   = f"Hello, MiseruAI! {datetime.date.today()}"
content = f"{KW} に関するテスト投稿（{datetime.datetime.now()}）"

payload = {
    "title":   title,
    "content": content,
    "status":  "draft"
}

# ----------- API 送信 -----------
r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts",
    json=payload,
    auth=(WP_USER, WP_PASS)
)

# ----------- デバッグ出力 --------
print("STATUS :", r.status_code)
print("HEADERS:", r.headers)
print("RAW    :", r.text[:500])          # 本文の先頭 500 文字

# Content-Type を確認して JSON ならパース
if r.headers.get("Content-Type", "").startswith("application/json"):
    try:
        print("PARSED :", json.dumps(r.json(), indent=2, ensure_ascii=False))
    except ValueError:
        print("※ JSON デコード失敗（RAW を参照）")
else:
    print("※ JSON ではありません")

# ----------- 終了判定 -----------
if r.status_code != 201:
    raise SystemExit("投稿失敗")
