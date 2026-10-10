# proj-anthropic-python-sdk-part2

Jupyter notebooks working through the Anthropic Python SDK: prompt evaluation and engineering, and tool use.

Notebooks are numbered in teaching order and are mostly self-contained — each one re-declares its own client and helper functions, so you can open any single notebook and run it top to bottom.

## Why this session (read this first)

The fair objection: *"we came for AI-powered SDLC, we're not building AI apps."* Correct — and that is what this session is about. Your AI coding tool **is** a prompt, a tool loop, and a context window. Every lever you have over it is one of four things, and each notebook here is one lever with the covers off:

| What you do in the IDE | What it actually is | Notebook |
| --- | --- | --- |
| Write `CLAUDE.md`, slash commands, specs for an agent | Prompt engineering, measured | `11` |
| Judge whether that change actually helped | Evals — a test suite for a non-deterministic component | `10` |
| Install an MCP server, write a hook | A tool schema plus a `tool_result` round-trip | `20` |
| Debug "why did it loop / pick the wrong tool / stop halfway?" | The agent loop and its failure modes | `21`, `22` |

You will not write a tool loop by hand at work. You will debug one, or be asked to add a "summarize this" feature, and this is the session that makes that an afternoon instead of a fortnight. The cheapest route to a working mental model of the tool you already use all day is to build a small one by hand, once.

Each notebook opens with a **"Why this is in an AI-powered SDLC class"** cell tying it back to this table.

## Setup

1. Install dependencies:
   ```bash
   pip install anthropic python-dotenv jupyter
   ```
2. Add your API key to `.env`:
   ```
   ANTHROPIC_API_KEY=your-key-here
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

## Supporting files

| Path | Used by |
| --- | --- |
| `dataset-aws.json` | `10` — generated eval dataset of AWS Python/JSON/regex tasks |
| `dataset-athlete.json` | `11` — generated eval dataset of athlete meal-planning scenarios |
| `prompt-eval-results-v1.md`, `prompt-eval-results-v2.md` | Written by `10` — one report per prompt version |

Notebook `11` also writes `output-<version>.json` / `output-<version>.html` reports; those are
generated artifacts and are not checked in.

## Notes

- All notebooks use `claude-haiku-4-5`.
- The eval notebooks pin `temperature=0` (`10`) and use assistant prefill with `stop_sequences`, so score changes come from the prompt rather than sampling noise. Both features are Haiku 4.5-era; on `claude-sonnet-5` / `claude-opus-5` they return a 400, and the portable replacement is structured outputs (`client.messages.parse`).
- Don't regenerate a dataset mid-demo — the versions would no longer be compared on the same test cases. The dataset-generation cells in `10` and `11` are marked accordingly.
