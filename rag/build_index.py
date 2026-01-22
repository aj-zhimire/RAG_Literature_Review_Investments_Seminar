import os
import glob
import uuid
import shutil
from typing import List, Tuple

import pdfplumber
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "zotero_library")
CHROMA_DIR = os.path.join(PROJECT_ROOT, "rag", "chroma_db")
COLLECTION_NAME = "seminar_papers"


def extract_text_by_page(pdf_path: str) -> List[Tuple[int, str]]:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            text = text.replace("\x00", "").strip()
            if text:
                pages.append((i, text))
    return pages


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
        if start >= length:
            break
    return chunks


def main() -> None:
    if not os.path.isdir(DATA_DIR):
        raise SystemExit(f"Missing data directory: {DATA_DIR}")

    pdf_paths = sorted(glob.glob(os.path.join(DATA_DIR, "*.pdf")))
    if not pdf_paths:
        raise SystemExit(
            f"No PDFs found in {DATA_DIR}. Add PDFs from Zotero and rerun."
        )

    os.makedirs(CHROMA_DIR, exist_ok=True)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
        embedding_function=embedding_fn,
    )

    docs = []
    metadatas = []
    ids = []

    for pdf_path in tqdm(pdf_paths, desc="Indexing PDFs"):
        filename = os.path.basename(pdf_path)
        pages = extract_text_by_page(pdf_path)
        for page_num, page_text in pages:
            chunks = chunk_text(page_text)
            for chunk in chunks:
                docs.append(chunk)
                metadatas.append(
                    {"source": filename, "page": page_num, "path": pdf_path}
                )
                ids.append(str(uuid.uuid4()))

    if not docs:
        raise SystemExit("No text extracted from PDFs. Check file integrity.")

    collection.add(documents=docs, metadatas=metadatas, ids=ids)
    print(f"Indexed {len(docs)} chunks from {len(pdf_paths)} PDFs.")
    print(f"ChromaDB stored at: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
