#!/usr/bin/env python3
"""
corpus.jsonl → OpenAI embeddings → ChromaDB(persist_directory="chroma")
"""

import os, json, pathlib, tiktoken, openai, chromadb
import hnswlib
if not hasattr(hnswlib.Index, "file_handle_count"):
    hnswlib.Index.file_handle_count = 0    # chromadb ≥0.4.14 対策
from tqdm import tqdm

DATA_PATH   = pathlib.Path("data/corpus.jsonl")
CHROMA_DIR  = pathlib.Path("chroma")
EMB_MODEL   = "text-embedding-3-small"          # *コスト低*
CHUNK_TOKS  = 800                               # 1チャンク上限

openai.api_key = os.environ["OPENAI_API_KEY"]

tok = tiktoken.encoding_for_model(EMB_MODEL)

def chunk_text(text: str, limit: int = CHUNK_TOKS):
    tokens = tok.encode(text)
    for i in range(0, len(tokens), limit):
        yield tok.decode(tokens[i:i+limit])

# 1. ChromaDB 初期化
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(
    name="website",
    metadata={"hnsw:space": "cosine"}
)

# 2. コーパス読込み & 埋め込み
with DATA_PATH.open() as f:
    docs = [json.loads(l) for l in f]

ids, embeds, metas = [], [], []

for doc in tqdm(docs, desc="embedding"):
    url = doc["url"]
    for j, chunk in enumerate(chunk_text(doc["text"])):
        resp = openai.embeddings.create(model=EMB_MODEL, input=chunk)
        ids.append(f"{url}#{j}")
        embeds.append(resp.data[0].embedding)
        metas.append({"url": url, "chunk": j, "text": chunk})

# 3. Upsert
collection.upsert(
    ids=ids,
    embeddings=embeds,
    metadatas=metas
)

print(f"✅ {len(ids)} chunks indexed → {CHROMA_DIR}")
