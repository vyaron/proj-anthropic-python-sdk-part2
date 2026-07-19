# proj-chat-python

Small example scripts for using the Anthropic Python SDK to chat with Claude.

## Setup

1. Install dependencies:
   ```bash
   pip install anthropic python-dotenv
   ```
2. Add your Anthropic API key to `.env`:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

## Scripts

- **01-messages.py** — Basic multi-turn conversation using a `messages` list with helper functions to append user/assistant turns.
- **02-system.py** — Adds a `system` prompt to steer Claude's behavior (a math tutor that guides instead of answering directly).
- **03-temparture.py** — Same as `01-messages.py` but exposes a `temperature` parameter to control response randomness.
- **04-stream.py** — Streams the response token-by-token using `client.messages.stream`.

Run any script directly, e.g.:
```bash
python 01-messages.py
```
