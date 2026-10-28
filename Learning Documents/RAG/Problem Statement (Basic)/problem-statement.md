# Problem Statement: The Chennai Leave Question

## Scenario

Your company keeps its HR policies in many documents, and they change often. Employees ask a chatbot questions about them. A typical one:

> **"Can I carry over unused leave to next year if I'm on the Chennai payroll?"**

The first version of the bot uses a basic RAG pipeline: embed chunks, fetch the top 3 most similar, give them to an LLM. Users complain that it quotes the global or US policy, and sometimes an outdated one.

## Data

Seven policy chunks, each with metadata:

| ID | Region | Year | Status | Text (shortened) |
|----|--------|------|--------|------------------|
| G-2024 | global | 2024 | superseded | Carry over up to 5 unused days, use by March |
| G-2026 | global | 2026 | current | Carry over up to 3 unused days, rest lapses |
| US-2026 | US | 2026 | current | US payroll: carry over up to 5 days |
| IN-2026 | IN-Chennai | 2026 | current | Chennai staff: 10 days roll forward, remainder encashed in March |
| IN-2025 | IN-Chennai | 2025 | superseded | Chennai staff: 5 days roll forward |
| G-SICK-2026 | global | 2026 | current | Sick leave does not carry over |
| G-PARENT-2026 | global | 2026 | current | Parental leave: 26 weeks paid |

Full text is in `03-rag_chroma_demo.py`.

## Your tasks

1. **Store** the chunks in a Chroma collection, with metadata.
2. **Baseline:** retrieve the top 3 by similarity only. Record which IDs come back.
3. **Check retrieval:** is `IN-2026` in the results? Is any superseded chunk there?
4. **Improve:** add a metadata filter (`status = current`, region is `global` or the region named in the question).
5. **Add a keyword condition:** require the word "Chennai" in the chunk text, using Chroma's `where_document`. Note when this helps and when it would hurt (what if the policy says "India" instead?).
6. **Build the prompt** from the retrieved chunks, as it would be sent to an LLM.

## Questions to answer

- Did the baseline fail on your machine? With real embeddings, results can differ from the toy demo. If it did not fail, what query would make it fail?
- Which improvement made the biggest difference: the metadata filter or the keyword condition?
- What would break if you filtered on `status = current` but forgot to mark old documents as `superseded` when a new version arrives?
- How would you handle a question that names no region?

## Expected outcome

For the Chennai question after the improvements, `IN-2026` ranks first and no superseded chunk appears. The final answer should say: *10 days can be carried over and the remainder is encashed in March.*

## Related files

- [02-chroma-how-to.md](./how-to-use-chroma.md): Chroma concepts and commands.
- [03-rag_chroma_demo.py](./rag-with-chroma.py): the runnable solution.
