"""
Week 3 — evaluate.py
A small, honest evaluation of the RAG assistant. For each test question it checks:

  1. RETRIEVAL  — did the expected source document appear in the retrieved chunks?
  2. ANSWER     — did the generated answer contain the expected key fact?
                  (and for out-of-scope questions, did it correctly REFUSE?)

It reuses retrieve() / build_prompt() from query.py, so it tests the real pipeline.

Run:  python evaluate.py
Writes a per-question table to the screen and saves eval_results.json.

Edit TESTS below to match the docs you actually ingested. If a question's
expected source didn't get fetched, the script warns you at the top.
"""

import json
import chromadb
import ollama
import query  # reuse the real retrieve + prompt-building

DB_DIR = "chroma_db"
COLLECTION = "de_docs"

# Each test: the question, the source file we expect to answer it (stem, no .md),
# and a keyword the correct answer should contain. Out-of-scope questions set
# expect_refusal=True instead — the assistant should say it doesn't have that.
TESTS = [
    {"q": "How can I speed up repeated Spark SQL queries on the same data?",
     "expect_source": "spark-sql-performance-tuning", "expect_keywords": ["cache"]},
    {"q": "How do I force Spark to broadcast a small table in a join?",
     "expect_source": "spark-sql-join-hints", "expect_keywords": ["broadcast"]},
    {"q": "What can I do to reduce memory pressure and GC in Spark?",
     "expect_source": "spark-tuning-guide", "expect_keywords": ["memory"]},
    {"q": "How do I compact many small files in a Delta table?",
     "expect_source": "delta-optimize-zorder", "expect_keywords": ["optimize"]},
    {"q": "What does Z-Ordering do in Delta Lake?",
     "expect_source": "delta-optimize-zorder", "expect_keywords": ["z-order"]},
    {"q": "How do I upsert data into a Delta table?",
     "expect_source": "delta-update-merge-delete", "expect_keywords": ["merge"]},
    {"q": "How do I delete rows from a Delta table based on a condition?",
     "expect_source": "delta-update-merge-delete", "expect_keywords": ["delete"]},
    {"q": "How do I remove old files no longer referenced by a Delta table?",
     "expect_source": "delta-table-utilities", "expect_keywords": ["vacuum"]},
    {"q": "What isolation guarantees does Delta Lake give for concurrent writes?",
     "expect_source": "delta-concurrency-control", "expect_keywords": ["isolation"]},
    {"q": "How do I overwrite data when writing a DataFrame to a Delta table?",
     "expect_source": "delta-batch-reads-writes", "expect_keywords": ["overwrite"]},
    {"q": "Can I use a Delta table as a streaming source?",
     "expect_source": "delta-streaming", "expect_keywords": ["stream"]},
    {"q": "What is an RDD in Spark?",
     "expect_source": "spark-rdd-programming", "expect_keywords": ["rdd"]},
    {"q": "How does Adaptive Query Execution improve Spark performance?",
     "expect_source": "spark-sql-performance-tuning", "expect_keywords": ["adaptive"]},

    # --- HARDER: indirect / paraphrased wording (no keyword in the question) ---
    {"q": "My job shuffles a huge amount of data when it joins a tiny lookup table. What's the fix?",
     "expect_source": "spark-sql-join-hints", "expect_keywords": ["broadcast"]},
    {"q": "I run the same transformation repeatedly and Spark recomputes it every time. How do I avoid that?",
     "expect_source": "spark-sql-performance-tuning", "expect_keywords": ["cache"]},
    {"q": "What's the lowest-level distributed collection abstraction in Spark?",
     "expect_source": "spark-rdd-programming", "expect_keywords": ["rdd"]},
    {"q": "Can Spark change the number of shuffle partitions automatically at runtime?",
     "expect_source": "spark-sql-performance-tuning", "expect_keywords": ["adaptive"]},
    {"q": "How do I insert new rows and update existing ones in a single Delta operation?",
     "expect_source": "delta-update-merge-delete", "expect_keywords": ["merge"]},

    # --- HARDER: ambiguous between related docs (either source is acceptable) ---
    {"q": "Reads on my Delta table got slow after lots of tiny writes. How do I make them fast again?",
     "expect_source": ["delta-optimize-zorder", "delta-table-utilities"], "expect_keywords": ["optimize"]},

    # --- HARDER: multi-doc (spans concurrency + optimize) ---
    {"q": "If two jobs write to the same Delta table while one runs OPTIMIZE, what can go wrong?",
     "expect_source": ["delta-concurrency-control", "delta-optimize-zorder"], "expect_keywords": ["conflict"]},

    # --- out-of-scope: the assistant SHOULD refuse, not make something up ---
    {"q": "How do I create an Amazon EC2 instance?", "expect_refusal": True},
    {"q": "What is the capital of France?", "expect_refusal": True},
    # sounds in-domain, but there are NO AWS Glue docs in the corpus -> must refuse
    {"q": "How do I configure an AWS Glue job bookmark?", "expect_refusal": True},
]

REFUSAL_MARKERS = ["don't have", "do not have", "not in the provided", "no information"]


def ingested_sources():
    """All source file stems currently in the vector DB."""
    client = chromadb.PersistentClient(path=DB_DIR)
    col = client.get_collection(COLLECTION)
    metas = col.get(include=["metadatas"])["metadatas"]
    return {m["source"].replace(".md", "") for m in metas}


def main():
    have = ingested_sources()
    print(f"Sources in the vector DB ({len(have)}): {', '.join(sorted(have))}\n")

    # warn about tests whose expected source(s) weren't ingested
    for t in TESTS:
        src = t.get("expect_source")
        if not src:
            continue
        expected = src if isinstance(src, list) else [src]
        if not any(e in have for e in expected):
            print(f"  ! warning: none of {expected} in DB — that question will likely MISS. "
                  f"Fetch it or edit the test.")
    print()

    retr_hits = retr_total = ans_ok = ans_total = 0
    rows = []

    for t in TESTS:
        hits = query.retrieve(t["q"])
        stems = {m["source"].replace(".md", "") for (_, m, _) in hits}

        row = {"q": t["q"]}

        # --- retrieval score (skip for out-of-scope) ---
        if not t.get("expect_refusal"):
            retr_total += 1
            exp = t["expect_source"]
            expected = exp if isinstance(exp, list) else [exp]
            hit = any(e in stems for e in expected)
            retr_hits += 1 if hit else 0
            row["retrieval"] = "HIT " if hit else "MISS"
        else:
            row["retrieval"] = "n/a "

        # --- generate the answer and score it ---
        prompt = query.build_prompt(t["q"], hits)
        resp = ollama.chat(model=query.CHAT_MODEL, messages=[{"role": "user", "content": prompt}])
        ans = resp["message"]["content"].lower()

        ans_total += 1
        if t.get("expect_refusal"):
            ok = any(m in ans for m in REFUSAL_MARKERS)
        else:
            ok = all(k.lower() in ans for k in t["expect_keywords"])
        ans_ok += 1 if ok else 0
        row["answer"] = "OK  " if ok else "WEAK"
        rows.append(row)

        print(f"[{row['retrieval']} | {row['answer']}]  {t['q']}")

    # --- summary ---
    retr_pct = (retr_hits / retr_total * 100) if retr_total else 0
    ans_pct = (ans_ok / ans_total * 100) if ans_total else 0
    print("\n" + "=" * 60)
    print(f"Retrieval hit-rate : {retr_hits}/{retr_total}  ({retr_pct:.0f}%)")
    print(f"Answer correctness : {ans_ok}/{ans_total}  ({ans_pct:.0f}%)")
    print("=" * 60)

    with open("eval_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "retrieval_hit_rate": f"{retr_hits}/{retr_total} ({retr_pct:.0f}%)",
            "answer_correctness": f"{ans_ok}/{ans_total} ({ans_pct:.0f}%)",
            "rows": rows,
        }, f, indent=2)
    print("Saved eval_results.json")


if __name__ == "__main__":
    main()
