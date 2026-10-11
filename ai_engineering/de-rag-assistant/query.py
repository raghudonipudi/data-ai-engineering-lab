"""
Week 1 — query.py  ("hello RAG")
Embeds your question with Ollama, finds the most relevant chunks from the
vector DB, and either (a) just shows them [--retrieve-only], or (b) asks a local
Ollama model to answer USING ONLY those chunks, with sources cited.

Needs Ollama running + models pulled once:
    ollama pull nomic-embed-text      (for embeddings)
    ollama pull llama3.1              (for the answer)

Run (retrieval only — no answer generated):
    python query.py "How do I tune a slow Spark join?" --retrieve-only

Run (full RAG):
    python query.py "How do I tune a slow Spark join?"
"""

import sys
import chromadb
import ollama

DB_DIR = "chroma_db"
COLLECTION = "de_docs"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.1"
TOP_K = 4


def embed(text):
    resp = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return resp["embedding"]


def retrieve(question, k=TOP_K):
    client = chromadb.PersistentClient(path=DB_DIR)
    col = client.get_collection(COLLECTION)
    q_emb = embed(question)
    res = col.query(query_embeddings=[q_emb], n_results=k)
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]
    return list(zip(docs, metas, dists))


def build_prompt(question, hits):
    context = "\n\n".join(
        f"[Source {i+1}: {m['source']} #{m['chunk']}]\n{d}"
        for i, (d, m, _) in enumerate(hits)
    )
    return f"""You are a data-engineering assistant. Answer the QUESTION using ONLY the CONTEXT below.
If the answer is not in the context, say "I don't have that in the provided docs."
Cite the sources you used like [Source 1], [Source 2].

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    retrieve_only = "--retrieve-only" in sys.argv
    if not args:
        print('Usage: python query.py "your question" [--retrieve-only]')
        return
    question = " ".join(args)

    hits = retrieve(question)

    print(f"\nQ: {question}\n")
    print("=== Retrieved chunks (closest first) ===")
    for i, (doc, meta, dist) in enumerate(hits, 1):
        preview = doc[:200].replace("\n", " ")
        print(f"\n[{i}] {meta['source']} #{meta['chunk']}  (distance {dist:.3f})")
        print(f"    {preview}...")

    if retrieve_only:
        print("\n(retrieve-only mode — no answer generated)")
        return

    prompt = build_prompt(question, hits)
    print("\n=== Grounded answer ===")
    resp = ollama.chat(model=CHAT_MODEL, messages=[{"role": "user", "content": prompt}])
    print(resp["message"]["content"])


if __name__ == "__main__":
    main()
