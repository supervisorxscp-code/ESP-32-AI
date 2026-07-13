## 2025-05-15 - Async AI client for responsive Discord bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. This prevents the bot from processing other events (like heartbeats or other messages) and makes visual feedback like `typing()` indicators lag or fail to appear.
**Action:** Always use `AsyncOpenAI` for AI completions in `discord.py` projects to maintain bot responsiveness and ensure smooth UX feedback.
