"""
Week 2 — fetch_docs.py
Downloads a curated list of PUBLIC documentation pages, strips the HTML down to
readable text, and saves each as a clean .md file in docs/ — ready for ingest.py.

Pure-Python libraries only (requests + BeautifulSoup with the built-in parser),
so no compiled binaries that an Application Control policy could block.

Run:  python fetch_docs.py
Then: python ingest.py   (re-chunks and re-embeds the new docs)

Public documentation only. Never add internal/proprietary URLs here.
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup

DOCS_DIR = "docs"

# Curated public docs. Add/remove freely. (Spark + Delta pages are static HTML
# and clean up nicely; a few may come back thin — that's fine, just delete them.)
URLS = {
    "spark-sql-performance-tuning": "https://spark.apache.org/docs/latest/sql-performance-tuning.html",
    "spark-tuning-guide":           "https://spark.apache.org/docs/latest/tuning.html",
    "spark-sql-join-hints":         "https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html",
    "spark-rdd-programming":        "https://spark.apache.org/docs/latest/rdd-programming-guide.html",
    "delta-batch-reads-writes":     "https://docs.delta.io/latest/delta-batch.html",
    "delta-optimize-zorder":        "https://docs.delta.io/latest/optimizations-oss.html",
    "delta-update-merge-delete":    "https://docs.delta.io/latest/delta-update.html",
    "delta-concurrency-control":    "https://docs.delta.io/latest/concurrency-control.html",
    "delta-table-utilities":        "https://docs.delta.io/latest/delta-utility.html",
    "delta-streaming":              "https://docs.delta.io/latest/delta-streaming.html",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; de-rag-assistant/1.0; learning project)"}

# tags that are never content — stripped before we extract text
JUNK_TAGS = ["script", "style", "nav", "header", "footer", "aside", "form", "button", "svg"]


def html_to_text(html):
    """Strip HTML down to readable headings + paragraphs."""
    soup = BeautifulSoup(html, "html.parser")

    # remove obvious non-content
    for tag in soup(JUNK_TAGS):
        tag.decompose()

    # prefer the main content region if the page marks one, else the whole body
    main = (soup.find("main")
            or soup.find("article")
            or soup.find(attrs={"role": "main"})
            or soup.body
            or soup)

    # get text with line breaks between block elements
    text = main.get_text(separator="\n")

    # collapse runs of blank lines and trailing spaces
    lines = [ln.rstrip() for ln in text.splitlines()]
    cleaned = []
    blank = 0
    for ln in lines:
        if ln.strip() == "":
            blank += 1
            if blank <= 1:
                cleaned.append("")
        else:
            blank = 0
            cleaned.append(ln)
    return "\n".join(cleaned).strip()


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    saved = 0
    for name, url in URLS.items():
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            text = html_to_text(resp.text)
            if len(text) < 200:
                print(f"  SKIP  {name}: page came back too thin ({len(text)} chars) — maybe JS-rendered")
                continue
            path = os.path.join(DOCS_DIR, f"{name}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Source: {url}\n\n{text}\n")
            print(f"  OK    {name}.md  ({len(text):,} chars)")
            saved += 1
        except Exception as e:
            print(f"  FAIL  {name}: {e}")
        time.sleep(1)  # be polite — one second between requests

    print(f"\nSaved {saved} of {len(URLS)} pages into {DOCS_DIR}/")
    print("Next: delete docs/sample_spark_notes.md, then run  python ingest.py")


if __name__ == "__main__":
    main()
