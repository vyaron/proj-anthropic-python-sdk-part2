# proj-anthropic-python-sdk-part2

Jupyter notebooks working through the Anthropic Python SDK: tool use, RAG, extended thinking, multimodal inputs, citations, prompt caching, and code execution.

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

### Tool use

- **001_tools.ipynb** — The raw tool-use loop, done by hand. Defines a `get_current_datetime` function, describes it with a `ToolParam` schema, and manually feeds the `tool_result` back to Claude.
- **003_tools_run_conversation.ipynb** — Wraps that loop in a reusable `run_conversation` helper so Claude can chain several tool calls to answer one question.
- **004_tools_completed.ipynb** — Two tools together (`get_current_datetime` + `add_duration_to_datetime`), with `run_tool` dispatching by name. Answers "set a reminder 177 days after Jan 1st, 2050."
- **005_tools_text_editor.ipynb** — Anthropic's built-in text editor tool (`text_editor_20250728`). Implements a `TextEditorTool` class backing `view`/`create`/`str_replace` against the local filesystem, then has Claude write and test a `pie.py`.
- **006_tools_web_search.ipynb** — The server-side `web_search_20250305` tool, scoped with `max_uses` and an `allowed_domains` allowlist. No local execution needed — results come back as `server_tool_use` blocks.

### RAG

These build up a retrieval pipeline in layers, all indexing the sample `report.md`.

- **010_rag_chunking.ipynb** — Three chunking strategies: fixed-size by character (with overlap), by sentence, and by markdown `##` section.
- **015_rag_embeddings.ipynb** — Generating embeddings with VoyageAI (`voyage-3-large`) and the `input_type` query/document distinction.
- **020_rag_vectordb.ipynb** — A from-scratch `VectorIndex` with cosine distance. Chunk → embed → index → search for the nearest chunks to a user question.
- **025_rag_bm25.ipynb** — A from-scratch `BM25Index` for keyword search, which beats embeddings on exact identifiers like `INC-2023-Q4-011`.
- **030_rag_hybrid.ipynb** — A `Retriever` that fans queries out to both the vector and BM25 indexes and merges the rankings, getting semantic and keyword matching in one.

### Model capabilities

- **040_extended_thinking.ipynb** — Enabling `thinking` with a token budget, reading `thinking` blocks off the response, and triggering redacted thinking with the magic test string.
- **050_images.ipynb** — Vision. Base64-encodes a satellite image from `images/` and runs a structured wildfire risk assessment over it.
- **051_pdf.ipynb** — The same pattern for PDFs, sending `pdfs/earth.pdf` as a `document` block.
- **052_citations.ipynb** — Turning on `citations` so Claude grounds claims in the source, plus a pretty-printer that resolves page, character, and block citation locations.
- **060_prompt_caching.ipynb** — `cache_control` breakpoints over a ~6k-token system prompt and ~1.7k tokens of tool schemas, with a `show_cache` helper reporting cache creation vs. read tokens per call.
- **065_code_execution.ipynb** — The Files API plus the `code_execution_20250825` sandbox. Uploads `streaming.csv`, has Claude run a churn analysis in the sandbox, and downloads the generated plot.

## Supporting files

| Path | Used by |
| --- | --- |
| `report.md` | All RAG notebooks — the document being chunked and indexed |
| `streaming.csv` | `065` — churn dataset for the code execution sandbox |
| `images/` | `050` — satellite property images |
| `pdfs/` | `051`, `052` — source PDFs |
| `outputs/` | Files downloaded back from the code execution sandbox |
| `.backups/` | Written by the `005` text editor tool before it edits a file |

## Notes

- Models vary by notebook: the early tool notebooks use `claude-haiku-4-5`, the rest use `claude-sonnet-4-5`.
- `065` needs beta headers (`code-execution-2025-08-25`, `files-api-2025-04-14`), set on the client via `default_headers`.
- The `020` and `030` notebooks embed chunks in a single bulk call rather than one at a time, to stay under VoyageAI's rate limits.
- Code execution requests are a single blocking call that runs the whole server-side loop, so `065` can take several minutes with no output until it finishes.
