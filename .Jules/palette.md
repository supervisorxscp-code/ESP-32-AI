# Palette's Journal

## 2025-02-12 - Non-blocking Async Operations in Discord Bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, causing all concurrent users of the bot to experience massive latency. Always use `AsyncOpenAI` and provide immediate visual feedback via `message.channel.typing()`.
**Action:** Ensure all Discord-facing AI bots use `AsyncOpenAI` with asynchronous `chat.completions.create` and wrap the API calls within a `typing()` context manager.
