"""
RAG with Chroma: the Chennai leave question.

Run:
    pip install chromadb
    python 03-rag_chroma_demo.py
    python 03-rag_chroma_demo.py "How many weeks of parental leave do I get?"

The first run downloads Chroma's default embedding model (about 80 MB).
No LLM is called; the script prints the prompt that would be sent to one.
"""
import sys
import chromadb

# ---------------------------------------------------------------- data
CHUNKS = [
    ("G-2024", "global", 2024, "superseded",
     "Employees may carry over unused leave to the next year, up to 5 days, and must use it by March."),
    ("G-2026", "global", 2026, "current",
     "Employees may carry over up to 3 days of unused leave into the next year; the rest lapses."),
    ("US-2026", "US", 2026, "current",
     "US payroll: employees may carry over up to 5 unused leave days to next year under state rules."),
    ("IN-2026", "IN-Chennai", 2026, "current",
     "Chennai payroll staff: up to 10 days of earned leave roll forward to the following year; "
     "the remainder is encashed in March."),
    ("IN-2025", "IN-Chennai", 2025, "superseded",
     "Chennai payroll staff: up to 5 days of earned leave roll forward to the following year."),
    ("G-SICK-2026", "global", 2026, "current",
     "Sick leave does not carry over; unused sick days lapse on 31 December."),
    ("G-PARENT-2026", "global", 2026, "current",
     "Parental leave: 26 weeks paid, must start within a year of birth."),
]

# words in a question -> (region value in metadata, keyword to require in text)
REGION_WORDS = {
    "chennai": ("IN-Chennai", "Chennai"),
    "india": ("IN-Chennai", "Chennai"),
    "us": ("US", "US"),
    "usa": ("US", "US"),
}
TARGET_ID = "IN-2026"  # the chunk that should be retrieved for the default question


# ---------------------------------------------------------------- setup
def build_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    try:
        col = client.get_or_create_collection(
            name="policies", configuration={"hnsw": {"space": "cosine"}}
        )
    except TypeError:  # older Chroma versions
        col = client.get_or_create_collection(
            name="policies", metadata={"hnsw:space": "cosine"}
        )
    col.upsert(  # safe to rerun: existing ids are updated, not duplicated
        ids=[c[0] for c in CHUNKS],
        documents=[c[4] for c in CHUNKS],
        metadatas=[{"region": c[1], "year": c[2], "status": c[3]} for c in CHUNKS],
    )
    return col


# ---------------------------------------------------------------- retrieval
def show(title, res, target=TARGET_ID):
    ids = res["ids"][0]
    print(f"\n=== {title} ===")
    if not ids:
        print("(no results: the filters matched nothing)")
        return ids
    for i, (cid, dist, meta) in enumerate(zip(ids, res["distances"][0], res["metadatas"][0]), 1):
        print(f"{i}. {cid:14} distance={dist:.3f}  region={meta['region']:10} "
              f"year={meta['year']} {meta['status']}")
    stale = [i for i, m in zip(ids, res["metadatas"][0]) if m["status"] == "superseded"]
    print(f"Contains {target}: {target in ids} | superseded chunks returned: {stale or 'none'}")
    return ids


def detect_region(question):
    for word in question.lower().replace("'", " ").replace("?", " ").split():
        if word in REGION_WORDS:
            return REGION_WORDS[word]
    return None


def naive(col, question):
    return col.query(query_texts=[question], n_results=3)


def improved(col, question):
    found = detect_region(question)
    regions = ["global"] + ([found[0]] if found else [])
    where = {"$and": [{"status": "current"}, {"region": {"$in": regions}}]}
    kwargs = dict(query_texts=[question], n_results=3, where=where)
    if found:  # keyword condition: the chunk text must mention the region
        kwargs["where_document"] = {"$contains": found[1]}
    res = col.query(**kwargs)
    if not res["ids"][0] and found:  # fallback: drop the keyword, keep metadata filters
        kwargs.pop("where_document")
        res = col.query(**kwargs)
    return res


def build_prompt(question, res):
    context = "\n".join(f"[{i}] {d}" for i, d in zip(res["ids"][0], res["documents"][0]))
    return ("Answer using ONLY the context below. Cite chunk IDs. "
            "If the context does not answer the question, say so.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}")


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Can I carry over unused leave to next year if I'm on the Chennai payroll?"
    collection = build_collection()
    print(f"Question: {q}\nItems in collection: {collection.count()}")

    show("1. Baseline: top 3 by similarity only", naive(collection, q))
    better = improved(collection, q)
    show("2. Improved: metadata filter + keyword condition", better)

    print("\n=== 3. Prompt for the LLM ===")
    print(build_prompt(q, better))

    print("\nNext steps: send that prompt to an LLM, and log which chunk IDs were retrieved "
          "so you can debug retrieval separately from generation.")
