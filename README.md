RAG-Based AI Literature Review System

Overview

This project implements a local, reproducible AI research assistant using a Retrieval-Augmented Generation (RAG) pipeline. The system enables semantic search over a curated set of academic papers and generates grounded literature reviews, research gaps, and testable hypotheses using large language models (LLMs), while ensuring citation accuracy and academic integrity.

This tool is designed for repeated use throughout the seminar and doctoral training, including literature reviews, proposal development, and dissertation research.

⸻

Core Principles
	•	Reproducibility: All outputs are traceable to a fixed set of local PDFs.
	•	Citation Discipline: Zotero serves as the single source of truth for references.
	•	No Hallucinations: LLMs are restricted to content retrieved via RAG.
	•	Scalability: The system scales from a few papers to thousands.

⸻

Project Structure

RAG_LitReview_Seminar/
│
├── README.md
│
├── venv/                      # Python virtual environment (local)
│
├── data/
│   ├── zotero_library/        # PDFs copied from Zotero
│   └── query_outputs/         # PDFs selected by RAG
│
├── rag/
│   ├── build_index.py         # Builds semantic index (ChromaDB)
│   ├── query.py               # Queries index and retrieves PDFs
│   ├── requirements.txt       # Python dependencies
│   └── chroma_db/             # Vector database (auto-generated)
│
├── zotero/
│   └── zotero_to_csv.py       # Exports citation log from Zotero
│
├── outputs/
│   ├── literature_review.pdf
│   ├── research_gaps.pdf
│   ├── hypotheses.pdf
│   └── zotero_paper_map.csv
│
└── logs/
    └── run_notes.md           # Optional execution notes


⸻

Requirements
	•	Python 3.9+
	•	VS Code (recommended)
	•	Zotero (desktop + browser connector)
	•	ChatGPT or Claude (for analysis step)

⸻

Setup Instructions

1. Create and Activate Virtual Environment

From the project root:

python3 -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\\Scripts\\activate    # Windows


⸻

2. Install Dependencies

pip install -r rag/requirements.txt


⸻

3. Prepare Zotero PDFs
	•	Create a Zotero collection named Seminar Readings
	•	Ensure each entry has:
	•	Author(s)
	•	Year
	•	Title
	•	Attached PDF
	•	Copy PDFs into:

data/zotero_library/


⸻

4. Build Semantic Index

python rag/build_index.py

This creates embeddings and stores them in rag/chroma_db/.

⸻

5. Run a Semantic Query

python rag/query.py

You will be prompted for:
	•	Research question
	•	top_k (recommended: 8–12)
	•	min_score (recommended: 0.4–0.6)

Relevant PDFs will be copied into:

data/query_outputs/


⸻

6. LLM Analysis (Strict Mode)

Upload only the PDFs from data/query_outputs/ to the LLM.

Generate:
	•	Literature review
	•	Research gaps
	•	Hypotheses

Save outputs as PDFs in:

outputs/

LLMs must not reference any source outside the uploaded PDFs.

⸻

7. Export Citation Log

python zotero/zotero_to_csv.py

Move the generated CSV to:

outputs/zotero_paper_map.csv


⸻

Final Submission Checklist
	•	Research question(s)
	•	Folder of RAG-selected PDFs
	•	Literature review PDF
	•	Research gaps PDF
	•	Hypotheses PDF
	•	Zotero citation log (CSV)

⸻

Notes
	•	Zotero is the source of truth for all citations.
	•	If a citation cannot be verified in Zotero, it must be corrected or removed.
	•	This system is intentionally script-based to ensure full reproducibility.

⸻

Intended Use Beyond This Assignment

This workflow is designed to be reused for:
	•	Group projects
	•	Seminar papers
	•	Dissertation literature reviews
	•	Collaborative research

Once built, it becomes a long-term research asset rather than a one-off assignment.