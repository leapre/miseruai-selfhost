# miseruai-selfhost
AIでSEO対策ができる自社サービスの開発
# ミセルAI 自社ホスティング版

<img src="docs/banner.png" width="600" alt="ミセルAIロゴ">

## 📌 プロジェクト概要
OEM版から脱却し、**SEO記事自動生成 × WordPress自動投稿** を
自社サーバーで完結させるためのコードベースです。

## ✨ 主な機能
- ロングテールキーワード自動収集
- HPコンテンツ学習 (RAG) & ベクトル検索
- Google / X トレンド ➜ 記事ネタ自動取得
- 5,000字 SEO記事を GPT-4o で生成し WP に予約投稿

## 🏃‍♂️ クイックスタート
```bash
git clone <このリポジトリ>
cd miseruai-selfhost
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run.py

## 📂 ディレクトリ
| パス | 役割 |
|------|------|
| `crawler/` | Google サジェスト・HP クロール |
| `pipeline/` | LangGraph フロー・記事生成 |
| `github/workflows/` | GitHub Actions (夜間バッチ) |
| `docs/` | 図・スクリーンショットなど |
| `requirements.txt` | Python 依存パッケージ |

- Python 3.11
- Node.js 18 (LangGraph CLI 用)

- OpenAI (o3)  / langchain-community
- ChromaDB 0.5+
- GitHub Actions
- WordPress REST API

## 💻 ローカル実行

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python crawler/suggest.py   # サジェスト取得テスト
