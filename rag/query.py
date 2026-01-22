import os
import shutil
from typing import List, Tuple

import chromadb
from chromadb.utils import embedding_functions

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CHROMA_DIR = os.path.join(PROJECT_ROOT, "rag", "chroma_db")
COLLECTION_NAME = "seminar_papers"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "query_outputs")


def normalize_score(distance: float) -> float:
    # Chroma returns cosine distance when configured with hnsw:space=cosine
    # similarity = 1 - distance (bounded roughly 0..1)
    return 1.0 - distance


def get_collection():
    if not os.path.isdir(CHROMA_DIR):
        raise SystemExit(
            "Index not found. Run `python rag/build_index.py` first."
        )
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(
        name=COLLECTION_NAME, embedding_function=embedding_fn
    )


def prompt_value(label: str, default: str) -> str:
    value = input(f"{label} [{default}]: ").strip()
    return value or default


def main() -> None:
    collection = get_collection()

    question = input("Research question: ").strip()
    if not question:
        raise SystemExit("Research question is required.")

    top_k = int(prompt_value("top_k", "10"))
    min_score_raw = prompt_value("min_score (0-1, blank for none)", "")
    min_score = float(min_score_raw) if min_score_raw else None

    results = collection.query(query_texts=[question], n_results=top_k)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    ranked = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        score = normalize_score(dist)
        ranked.append((score, meta))

    ranked.sort(key=lambda x: x[0], reverse=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    copied = set()

    print("\nTop results:")
    for score, meta in ranked:
        if min_score is not None and score < min_score:
            continue
        source = meta.get("source", "unknown")
        page = meta.get("page", "?")
        path = meta.get("path")
        print(f"- {source} (page {page}) score={score:.3f}")
        if path and os.path.isfile(path) and source not in copied:
            shutil.copy2(path, os.path.join(OUTPUT_DIR, source))
            copied.add(source)

    print(f"\nCopied {len(copied)} PDFs to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
