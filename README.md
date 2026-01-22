# RAG-Based AI Literature Review System

## Overview
This project builds a local, reproducible AI research assistant using a Retrieval-Augmented Generation (RAG) pipeline. It enables semantic search over a curated library of academic PDFs, then supports grounded literature reviews, research gaps, and testable hypotheses using an LLM — while keeping citations accurate through Zotero.

## Core Principles
- Reproducibility: Outputs trace back to a fixed set of local PDFs.
- Citation discipline: Zotero is the source of truth for references.
- No hallucinations: LLM outputs are constrained to retrieved papers.
- Scalability: Works from a handful of papers to 1,000+.

## Project Structure
```
RAG_Literature_Review_Investments_Seminar/
├── README.md
├── data/
│   ├── zotero_library/        # PDFs copied from Zotero
│   └── query_outputs/         # PDFs selected by RAG
├── rag/
│   ├── build_index.py         # Build semantic index (ChromaDB)
│   ├── query.py               # Query index and retrieve PDFs
│   ├── requirements.txt       # Python dependencies
│   └── chroma_db/             # Vector database (auto-generated)
├── zotero/
│   ├── zotero_to_csv.py       # Normalize Zotero CSV export
│   └── zotero_export.csv      # (User-provided export from Zotero)
├── outputs/
│   ├── literature_review.pdf
│   ├── research_gaps.pdf
│   ├── hypotheses.pdf
│   └── zotero_paper_map.csv
└── logs/
    └── run_notes.md
```

## Requirements
- Python 3.9+
- Zotero (desktop + browser connector)
- ChatGPT or Claude for analysis step

## Setup (Matches Assignment Steps)

### 1) Prepare Zotero
1. Create a Zotero collection named **Seminar Readings**.
2. Add all assigned papers and attach PDFs.

### 2) Copy PDFs to Local Folder
Copy the PDFs into:
```
data/zotero_library/
```

### 3) Create and Activate a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```

### 4) Install Dependencies
```
pip install -r rag/requirements.txt
```

### 5) Build the Semantic Index
```
python rag/build_index.py
```
This creates embeddings and stores them in `rag/chroma_db/`.

### 6) Run a Query
```
python rag/query.py
```
You will be prompted for:
- Research question
- `top_k` (recommended: 8–12)
- `min_score` (recommended: 0.4–0.6)

RAG copies the most relevant PDFs into:
```
data/query_outputs/
```

### 7) LLM Analysis (Strict Mode)
Upload only the PDFs from `data/query_outputs/` and generate:
- Literature review
- Research gaps
- Hypotheses

Save results to:
```
outputs/
```

### 8) Export Zotero Citation Log
1. In Zotero, export your library/collection to CSV.
2. Save it as:
```
zotero/zotero_export.csv
```
3. Run:
```
python zotero/zotero_to_csv.py
```
This produces:
```
outputs/zotero_paper_map.csv
```

## Submission Checklist
- Research question(s)
- Folder of RAG-selected PDFs (`data/query_outputs/`)
- Literature review PDF
- Research gaps PDF
- Hypotheses PDF
- Zotero citation log (`outputs/zotero_paper_map.csv`)

## Notes
- Verify every citation against Zotero before submission.
- If a citation is missing or incorrect, fix it using Zotero metadata.
- Keep all outputs grounded in the retrieved PDFs only.
