import csv
import os
import sys
from typing import List

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DEFAULT_INPUT = os.path.join(PROJECT_ROOT, "zotero", "zotero_export.csv")
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "outputs", "zotero_paper_map.csv")

EXPECTED_COLUMNS = [
    "Title",
    "Author",
    "Year",
    "DOI",
    "Publication Title",
    "Item Type",
]


def read_rows(path: str) -> List[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def normalize_row(row: dict) -> dict:
    return {
        "Title": row.get("Title", "").strip(),
        "Author": row.get("Author", "").strip(),
        "Year": row.get("Year", "").strip(),
        "DOI": row.get("DOI", "").strip(),
        "Publication Title": row.get("Publication Title", "").strip(),
        "Item Type": row.get("Item Type", "").strip(),
    }


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT

    if not os.path.isfile(input_path):
        raise SystemExit(
            "Missing Zotero CSV export. Export your Zotero library as CSV and save it to:\n"
            f"  {DEFAULT_INPUT}\n"
            "Then rerun: python zotero/zotero_to_csv.py"
        )

    rows = read_rows(input_path)
    normalized = [normalize_row(r) for r in rows]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
        writer.writeheader()
        writer.writerows(normalized)

    print(f"Wrote {len(normalized)} rows to {output_path}")


if __name__ == "__main__":
    main()

