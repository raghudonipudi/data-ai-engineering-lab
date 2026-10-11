# Data Engineering RAG Assistant

An LLM assistant that answers Spark / Databricks / Delta Lake / AWS Glue
questions grounded in official documentation, with sources cited.

**Week 1 goal:** get retrieval working and see your first grounded answer.

---

## One-time setup

**1. Install Ollama** (the free local LLM runner) from https://ollama.com/download
Then pull a model (≈4–5GB, one-time):
```bash
ollama pull llama3.1
```
Leave Ollama running (it runs as a background service after install).

**2. Set up the Python project:**
```bash
cd de-rag-assistant
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Run it (Week 1)

**Step 1 — ingest the docs** (embeds + stores them in a local vector DB):
```bash
python ingest.py
```
This works immediately on the sample file so you can see it run.

**Step 2 — see retrieval work** (no LLM needed yet):
```bash
python query.py "How do I fix a slow Spark join?" --retrieve-only
```
You should see the most relevant chunks come back. **That's RAG's retrieval
step working — the core of the whole system.**

**Step 3 — full grounded answer** (needs Ollama running):
```bash
python query.py "How do I fix a slow Spark join?"
```
Now the model answers using only the retrieved chunks, citing sources.

---

## Then: add real documentation

Replace `docs/sample_spark_notes.md` with real **public** doc pages. Good
starting sources (copy page text into `.md` or `.txt` files in `docs/`):

- Apache Spark — SQL performance tuning, join hints
- Delta Lake — table basics, OPTIMIZE, VACUUM, MERGE
- Databricks — jobs, clusters, Delta Live Tables (public docs)
- AWS Glue — PySpark job basics, common errors

Aim for ~30–50 pages. Re-run `python ingest.py` after adding files.

> **Rule:** public documentation only. Never ingest TCS code, client data,
> internal URLs, or anything proprietary.

---

## How it works (so you can explain it in interviews)

1. **Chunk** — split docs into overlapping ~800-char pieces (`ingest.py`).
2. **Embed** — turn each chunk into a vector with `all-MiniLM-L6-v2`.
3. **Store** — save vectors + text + source metadata in Chroma.
4. **Retrieve** — embed the question, find the nearest chunks by vector similarity.
5. **Ground** — build a prompt with only those chunks; the LLM answers from them and cites sources.

Being able to walk through these five steps from memory is the Week 1 win.
