# RAG (Retrieval-Augmented Generation): Guide with a Worked Scenario

## 1. What RAG is

RAG puts relevant information from an external source into the prompt **before** the LLM answers. The model answers from that material instead of only from what it memorized in training.

**Pipeline**

1. **Index (offline):** split documents into chunks, embed each chunk, store in a vector DB or search index. Keep metadata (region, version, date).
2. **Retrieve (per query):** embed the question and fetch the most relevant chunks.
3. **Augment:** place those chunks and the question into the prompt.
4. **Generate:** the LLM answers from the chunks, ideally citing them.

**Why use it:** it handles private or fresh data, reduces hallucination, supports citations, and updates by re-indexing rather than retraining.

## 2. Scenario question

> Your company has 15,000 HR/IT policy documents that change weekly. An employee asks:
> **"Can I carry over unused leave to next year if I'm on the Chennai payroll?"**
>
> Your first RAG version (chunk → embed → top-3 → LLM) keeps returning the global policy, sometimes an outdated 2024 version. The Chennai rule is missed.
>
> **What is going wrong, and how do you fix it?**

### Example corpus

| ID | Region | Year | Status | Text (shortened) |
|----|--------|------|--------|------------------|
| G-2024 | global | 2024 | superseded | Carry over up to 5 unused days... |
| G-2026 | global | 2026 | current | Carry over up to 3 unused days... |
| US-2026 | US | 2026 | current | US payroll: carry over up to 5 days... |
| IN-2026 | Chennai | 2026 | current | Chennai staff: 10 days roll forward; rest encashed in March |
| IN-2025 | Chennai | 2025 | superseded | Chennai staff: 5 days roll forward |

### Example answer

| Problem | Cause | Fix |
|---------|-------|-----|
| Outdated policy returned | Old and new versions both indexed | Metadata (`status`, `effective_date`); filter out superseded chunks; re-index on change |
| Wrong region returned | Similarity favors wording like "carry over unused leave", which the global and US chunks match more closely | Detect region in the query, filter by it, boost region-specific chunks |
| Chennai rule ranked low | The chunk uses different wording ("roll forward"), so pure similarity underrates it | Hybrid search (keyword + vector), reranker, section-aware chunks that keep headings |
| One lookup is not enough | Answer may need a regional rule plus a global fallback | Retrieve twice or let an agent decide (agentic RAG) |
| Hard to debug | Retrieval and generation failures look the same | Evaluate retrieval separately: did the correct chunk appear in the context? |

**Expected result after the fix:** `IN-2026` first, `G-2026` as fallback, and the answer: *10 days can be carried over; the remainder is encashed in March.*

## 3. Is RAG outdated in 2026?

Not the idea. The naive version is. Long context windows did not remove the need for retrieval because of cost, latency, accuracy degradation on very long inputs, and corpora that are too big or change too often.

What changed:

- **Agentic RAG:** the model decides when and what to retrieve, possibly several times.
- **Hybrid setups:** retrieval selects the best material, then a large context window holds it.
- **Graph and structured retrieval** for relationship-heavy data.
- **Skip retrieval** when you have one document or a small, stable corpus.

## 4. Practice questions

1. **(Easy)** Why do we store metadata alongside embeddings?
2. **(Medium)** Users report the bot is "hallucinating" but the correct chunk is in the prompt. Where do you look first?
3. **(Hard)** The answer needs data from two documents (a policy and a regional exception). Compare a single-shot retriever to an agentic one, including cost and latency.

## 5. Companion files

Keep all three files together in `RAG/Overview/` so these relative links work:

- [rag-demo.html](./rag-demo.html): interactive comparison of naive vs improved retrieval on this scenario.
- [rag-pipeline.html](./rag-pipeline.html): the pipeline stage by stage with example data.
