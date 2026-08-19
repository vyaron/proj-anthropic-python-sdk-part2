# proj-anthropic-python-sdk-part2

Jupyter notebooks working through the Anthropic Python SDK: prompt evaluation and engineering, tool use, and RAG.

Notebooks are numbered in teaching order and are mostly self-contained — each one re-declares its own client and helper functions, so you can open any single notebook and run it top to bottom.

## Setup

1. Install dependencies:
   ```bash
   pip install anthropic python-dotenv voyageai jupyter
   ```
2. Add your API keys to `.env`:
   ```
   ANTHROPIC_API_KEY=your-key-here
   VOYAGE_API_KEY=your-key-here    # only needed for the RAG notebooks
   ```
3. Launch Jupyter, or open a notebook directly in VS Code:
   ```bash
   jupyter lab
   ```

## Notebooks

### Prompt evaluation & engineering

Both notebooks are built as live demos: you pick a prompt version, run the eval, read the
grader's weaknesses, and write the next version from that evidence. Each has a `DEMO FLOW`
cell at the bottom describing the run order.

- **10_prompt_eval.ipynb** — A hand-rolled eval harness over AWS coding tasks. Claude generates the dataset (`dataset-aws.json`), each test case is scored twice — once by a model grader returning strengths/weaknesses/score as JSON, once by a syntax validator (`json.loads` / `ast.parse` / `re.compile`) — and the two halves are averaged. Writes a Markdown report per prompt version and prints a side-by-side comparison of every version run so far.
- **11_prompt-engineering.ipynb** — Five prompt versions of a meal-planning task, each adding exactly one technique on top of the last (baseline → clear and direct → guidance & steps → XML structure → example), so every score delta is attributable. Uses a `PromptEvaluator` class that generates test cases (`dataset-athlete.json`), grades them concurrently against fixed `extra_criteria`, and renders an HTML report.

### Tool use

- **20_tools.ipynb** — The raw tool-use loop, done by hand. Defines a `get_current_datetime` function, describes it with a `ToolParam` schema, and manually feeds the `tool_result` back to Claude.
- **21_tools_run_conversation.ipynb** — Wraps that loop in a reusable `run_conversation` helper so Claude can chain several tool calls to answer one question.
- **22_tools_completed.ipynb** — Two tools together (`get_current_datetime` + `add_duration_to_datetime`), with `run_tool` dispatching by name. Answers "set a reminder 177 days after Jan 1st, 2050."

### RAG

These build up a retrieval pipeline in layers, all indexing the sample `report.md`.

- **30_rag_chunking.ipynb** — Three chunking strategies: fixed-size by character (with overlap), by sentence, and by markdown `##` section.
- **31_rag_embeddings.ipynb** — Generating embeddings with VoyageAI (`voyage-3-large`) and the `input_type` query/document distinction.
- **32_rag_vectordb.ipynb** — A from-scratch `VectorIndex` with cosine distance. Chunk → embed → index → search for the nearest chunks to a user question.
- **33_rag_bm25.ipynb** — A from-scratch `BM25Index` for keyword search, which beats embeddings on exact identifiers like `INC-2023-Q4-011`.
- **34_rag_hybrid.ipynb** — A `Retriever` that fans queries out to both the vector and BM25 indexes and merges the rankings, getting semantic and keyword matching in one.

## Supporting files

| Path | Used by |
| --- | --- |
| `dataset-aws.json` | `10` — generated eval dataset of AWS Python/JSON/regex tasks |
| `dataset-athlete.json` | `11` — generated eval dataset of athlete meal-planning scenarios |
| `prompt-eval-results-v1.md`, `prompt-eval-results-v2.md` | Written by `10` — one report per prompt version |
| `report.md` | All RAG notebooks — the document being chunked and indexed |
| `VoyageAI_API_Key_Directions.pdf` | How to get the `VOYAGE_API_KEY` the RAG notebooks need |

Notebook `11` also writes `output-<version>.json` / `output-<version>.html` reports; those are
generated artifacts and are not checked in.

## Notes

- Models vary by notebook: the prompt and tool notebooks use `claude-haiku-4-5`, the RAG notebooks use `claude-sonnet-4-5`.
- The eval notebooks pin `temperature=0` (`10`) and use assistant prefill with `stop_sequences`, so score changes come from the prompt rather than sampling noise. Both features are Haiku 4.5-era; on `claude-sonnet-5` / `claude-opus-5` they return a 400, and the portable replacement is structured outputs (`client.messages.parse`).
- Don't regenerate a dataset mid-demo — the versions would no longer be compared on the same test cases. The dataset-generation cells in `10` and `11` are marked accordingly.
- The `32` and `34` notebooks embed chunks in a single bulk call rather than one at a time, to stay under VoyageAI's rate limits.
