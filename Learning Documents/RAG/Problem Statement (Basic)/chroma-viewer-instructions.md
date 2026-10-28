# Chroma Viewer: Instructions

A small, read-only web viewer for a local Chroma database. It lets you look at collections, items, metadata, and run filtered similarity searches in your browser.

It needs only `chromadb` (already installed for the demo) and Python's standard library. Nothing else to install.

## 1. Before you start

1. Run the demo once so the database folder exists:

   ```bash
   python 03-rag_chroma_demo.py
   ```

   This creates a `chroma_db` folder next to the script.

2. Keep `04-chroma_viewer.py` in the same folder, or give it the full path to your Chroma folder.

## 2. Start the viewer

```bash
python 04-chroma_viewer.py chroma_db
```

Then open **http://127.0.0.1:8000** in your browser.

| Option | Meaning |
|--------|---------|
| `chroma_db` | Path to the Chroma folder (default: `chroma_db`) |
| `--port 8001` | Use another port if 8000 is taken |

Stop it with **Ctrl+C** in the terminal. The viewer only listens on your own computer (127.0.0.1), and it cannot change or delete data.

## 3. Using the page

**Collection dropdown:** pick a collection. The number in brackets is its item count.

**Browse tab:** lists items with ID, document text, and metadata, 25 per page. Use Previous and Next to page.

**Search tab:** type a question and press Enter or **Run**. You get the nearest chunks with a **distance** column. Lower distance means closer. With the cosine setting used in the demo, 0 is identical.

**Metadata filter box:** takes JSON, the same as `where` in Chroma. It works on both tabs.

```json
{"status": "current"}
{"region": {"$in": ["global", "IN-Chennai"]}}
{"$and": [{"status": "current"}, {"region": "IN-Chennai"}]}
```

Leave it empty for no filter.

**Show embedding preview:** adds a column with the first 8 numbers of each vector. Real vectors have hundreds of numbers (the default model uses 384).

## 4. Try this with the Chennai scenario

1. Choose the `policies` collection and open the **Search** tab.
2. Search: `Can I carry over unused leave to next year if I'm on the Chennai payroll?` with an empty filter. Note the order and distances. This is the baseline.
3. Add the filter `{"status": "current"}` and run again. Superseded chunks (`G-2024`, `IN-2025`) disappear.
4. Change the filter to `{"$and": [{"status": "current"}, {"region": {"$in": ["global", "IN-Chennai"]}}]}`. The US chunk disappears.
5. Check where `IN-2026` ranks in each case. This is the same retrieval check the demo script prints.

## 5. Troubleshooting

| Problem | What to do |
|---------|------------|
| "No collections found at this path" | The path is wrong or the demo has not been run. Run `03-rag_chroma_demo.py` first and check the folder name. |
| Page does not load | Check the terminal for errors. Try another port: `--port 8001`. |
| `JSONDecodeError` in red | The filter box is not valid JSON. Use double quotes: `{"status": "current"}`. |
| Error mentioning an unknown field or operator | Check spelling of metadata keys (`region`, `status`, `year`) and operators (`$in`, `$and`). |
| Search fails on the first try | Chroma may be downloading its embedding model (about 80 MB, needs internet once). Wait and retry. |
| Buttons do nothing | Open the page in a normal browser, not an editor's preview pane that blocks scripts. |
| Changes made by the demo script are not shown | Reload the page. The viewer reads live data each time you click Run. |

## 6. Limits

- Read-only: no editing, adding, or deleting.
- Searching embeds your text with the collection's embedding function, so it works for collections created with the default model. Collections that use a custom function may need that function available.
- Made for small local databases. It pages 25 items at a time but has not been tuned for very large collections.
- I tested the viewer against a stand-in for Chroma, not a real database. If something errors on your machine, note the message shown in the page or terminal.

## Related files

- [01-problem-statement.md](./problem-statement.md)
- [02-chroma-how-to.md](./how-to-use-chroma.md)
- [03-rag_chroma_demo.py](./rag-with-chroma.py)
- [04-chroma_viewer.py](./chroma_viewer.py)
