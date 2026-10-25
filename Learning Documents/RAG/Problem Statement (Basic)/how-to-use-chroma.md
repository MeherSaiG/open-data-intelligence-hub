# How to Use Chroma (embedded, no server)

Chroma runs inside your Python program and stores data in a local folder, much like SQLite. You still install it once with pip, but there is no server to set up.

## 1. Install

```bash
pip install chromadb
```

Use a recent Python 3. The first time you add or query text, Chroma downloads its default embedding model (about 80 MB, all-MiniLM-L6-v2) and caches it, so you need internet once.

## 2. Core ideas

| Term | Meaning |
|------|---------|
| **Client** | Connection to Chroma. `PersistentClient(path=...)` saves to disk; `EphemeralClient()` keeps data in memory only. |
| **Collection** | A named set of items, like a table. |
| **Item** | An `id`, a `document` (text), optional `metadata` (dict), and an embedding. |
| **Embedding function** | Turns text into a vector. Chroma uses a default one if you give none. |
| **Distance** | Lower means more similar. With `cosine` it is `1 - cosine similarity`. |

## 3. Create a collection

```python
import chromadb

client = chromadb.PersistentClient(path="chroma_db")
col = client.get_or_create_collection(
    name="policies",
    configuration={"hnsw": {"space": "cosine"}},  # default is l2
)
```

Choose the distance (`l2`, `cosine`, `ip`) when you create the collection. It cannot be changed afterwards; delete and rebuild the collection to change it. Older Chroma versions use `metadata={"hnsw:space": "cosine"}` instead.

## 4. Add data

```python
col.upsert(
    ids=["IN-2026", "G-2026"],
    documents=["Chennai payroll staff: up to 10 days...", "Employees may carry over up to 3 days..."],
    metadatas=[{"region": "IN-Chennai", "status": "current"},
               {"region": "global", "status": "current"}],
)
```

`upsert` inserts new IDs and updates existing ones, so you can rerun your script safely. Metadata values must be strings, numbers, or booleans.

## 5. Query

```python
res = col.query(query_texts=["carry over leave Chennai"], n_results=3)
```

The result is a dictionary of lists, one inner list per query text:

```python
res["ids"][0]        # ['IN-2026', 'G-2026', ...]
res["documents"][0]  # the texts
res["metadatas"][0]  # the metadata dicts
res["distances"][0]  # lower is closer
```

## 6. Filter by metadata (`where`)

```python
col.query(
    query_texts=["carry over leave"],
    n_results=3,
    where={"$and": [
        {"status": "current"},
        {"region": {"$in": ["global", "IN-Chennai"]}},
    ]},
)
```

Operators include `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$and`, `$or`. The filter is applied together with the similarity search.

## 7. Filter by text (`where_document`)

```python
col.query(query_texts=["carry over leave"], n_results=3,
          where_document={"$contains": "Chennai"})
```

This is a simple keyword condition on the document text. It is case-sensitive, so "chennai" will not match "Chennai". It is not a ranked keyword search like BM25, only a filter.

## 8. Other useful calls

```python
col.count()                         # number of items
col.get(ids=["IN-2026"])            # fetch by id, no similarity search
col.get(where={"status": "superseded"})
col.delete(ids=["IN-2025"])
client.delete_collection("policies")
```

## 9. Common mistakes

- **Changing the embedding model later.** Vectors from different models are not comparable. Re-embed everything if you switch.
- **Forgetting that distance is lower-is-better.** A score near 0 is a close match.
- **Stale data.** Updating a policy without updating or deleting the old chunk leaves both searchable. Use metadata such as `status` and filter on it.
- **Too-strict filters.** If a filter matches nothing, you get empty results. Handle that case in your code.
- **Trusting similarity alone.** Always check that the chunk you expected is in the retrieved set before blaming the LLM.

## Related files

- [01-problem-statement.md](./problem-statement.md)
- [03-rag_chroma_demo.py](./rag-with-chroma.py)
