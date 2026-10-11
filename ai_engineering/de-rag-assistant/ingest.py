"""
Week 1 — ingest.py
Loads every .md / .txt file in docs/, splits them into overlapping chunks,
embeds each chunk with Ollama (local, no cloud), and stores them in a local
Chroma vector database.

Needs Ollama running + the embedding model pulled once:
    ollama pull nomic-embed-text

Run:  python ingest.py
"""

import os
import glob
import chromadb
import ollama

DOCS_DIR = "docs"
DB_DIR = "chroma_db"
COLLECTION = "de_docs"
EMBED_MODEL = "nomic-embed-text"   # pull once with: ollama pull nomic-embed-text
CHUNK_SIZE = 800                   # characters per chunk
CHUNK_OVERLAP = 150                # characters of overlap between chunks


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Simple character-based chunking with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += size - overlap
    return chunks


def embed(text):
    """Get one embedding vector from Ollama."""
    resp = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return resp["embedding"]


def main():
    # 1. fresh Chroma collection
    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(COLLECTION)

    # 2. read docs, chunk, embed, store
    files = glob.glob(os.path.join(DOCS_DIR, "*.md")) + glob.glob(os.path.join(DOCS_DIR, "*.txt"))
    if not files:
        print(f"No .md or .txt files found in {DOCS_DIR}/. Add some doc pages and re-run.")
        return

    total = 0
    for path in files:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        source = os.path.basename(path)
        chunks = chunk_text(text)
        if not chunks:
            continue
        # embed each chunk via Ollama
        embeddings = [embed(c) for c in chunks]
        ids = [f"{source}-{i}" for i in range(len(chunks))]
        metadatas = [{"source": source, "chunk": i} for i in range(len(chunks))]
        col.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)
        print(f"  {source}: {len(chunks)} chunks embedded + stored")
        total += len(chunks)

    print(f"\nDone. Stored {total} chunks from {len(files)} file(s) in {DB_DIR}/")


if __name__ == "__main__":
    main()
