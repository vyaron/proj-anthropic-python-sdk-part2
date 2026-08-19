# proj-anthropic-python-sdk-part2

Jupyter notebooks working through the Anthropic Python SDK: prompt evaluation and engineering, tool use, RAG, extended thinking, multimodal inputs, citations, prompt caching, and code execution.

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
- **23_tools_text_editor.ipynb** — Anthropic's built-in text editor tool (`text_editor_20250728`). Implements a `TextEditorTool` class backing `view`/`create`/`str_replace` against the local filesystem, then has Claude write and test a `pie.py`.
- **24_tools_web_search.ipynb** — The server-side `web_search_20250305` tool, scoped with `max_uses` and an `allowed_domains` allowlist. No local execution needed — results come back as `server_tool_use` blocks.

### RAG

These build up a retrieval pipeline in layers, all indexing the sample `report.md`.

- **30_rag_chunking.ipynb** — Three chunking strategies: fixed-size by character (with overlap), by sentence, and by markdown `##` section.
- **31_rag_embeddings.ipynb** — Generating embeddings with VoyageAI (`voyage-3-large`) and the `input_type` query/document distinction.
- **32_rag_vectordb.ipynb** — A from-scratch `VectorIndex` with cosine distance. Chunk → embed → index → search for the nearest chunks to a user question.
- **33_rag_bm25.ipynb** — A from-scratch `BM25Index` for keyword search, which beats embeddings on exact identifiers like `INC-2023-Q4-011`.
- **34_rag_hybrid.ipynb** — A `Retriever` that fans queries out to both the vector and BM25 indexes and merges the rankings, getting semantic and keyword matching in one.

### Model capabilities

- **40_extended_thinking.ipynb** — Enabling `thinking` with a token budget, reading `thinking` blocks off the response, and triggering redacted thinking with the magic test string.
- **50_images.ipynb** — Vision. Base64-encodes a satellite image from `images/` and runs a structured wildfire risk assessment over it.
- **60_pdf.ipynb** — The same pattern for PDFs, sending `pdfs/earth.pdf` as a `document` block.
- **70_citations.ipynb** — Turning on `citations` so Claude grounds claims in the source, plus a pretty-printer that resolves page, character, and block citation locations.
- **80_prompt_caching.ipynb** — `cache_control` breakpoints over a ~6k-token system prompt and ~1.7k tokens of tool schemas, with a `show_cache` helper reporting cache creation vs. read tokens per call.
- **90_code_execution.ipynb** — The Files API plus the `code_execution_20250825` sandbox. Uploads `streaming.csv`, has Claude run a churn analysis in the sandbox, and downloads the generated plot.

## Supporting files

| Path | Used by |
| --- | --- |
| `dataset-aws.json` | `10` — generated eval dataset of AWS Python/JSON/regex tasks |
| `dataset-athlete.json` | `11` — generated eval dataset of athlete meal-planning scenarios |
| `prompt-eval-results-v1.md`, `prompt-eval-results-v2.md` | Written by `10` — one report per prompt version |
| `report.md` | All RAG notebooks — the document being chunked and indexed |
| `streaming.csv` | `90` — churn dataset for the code execution sandbox |
| `images/` | `50` — satellite property images |
| `pdfs/` | `60`, `70` — source PDFs |
| `outputs/` | Files downloaded back from the code execution sandbox |
| `.backups/` | Written by the `23` text editor tool before it edits a file |

Notebook `11` also writes `output-<version>.json` / `output-<version>.html` reports; those are
generated artifacts and are not checked in.

## Notes

- Models vary by notebook: the prompt and early tool notebooks use `claude-haiku-4-5`, the rest use `claude-sonnet-4-5`.
- The eval notebooks pin `temperature=0` (`10`) and use assistant prefill with `stop_sequences`, so score changes come from the prompt rather than sampling noise. Both features are Haiku 4.5-era; on `claude-sonnet-5` / `claude-opus-5` they return a 400, and the portable replacement is structured outputs (`client.messages.parse`).
- Don't regenerate a dataset mid-demo — the versions would no longer be compared on the same test cases. The dataset-generation cells in `10` and `11` are marked accordingly.
- `90` needs beta headers (`code-execution-2025-08-25`, `files-api-2025-04-14`), set on the client via `default_headers`.
- The `32` and `34` notebooks embed chunks in a single bulk call rather than one at a time, to stay under VoyageAI's rate limits.
- Code execution requests are a single blocking call that runs the whole server-side loop, so `90` can take several minutes with no output until it finishes.
