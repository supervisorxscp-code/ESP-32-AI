# Palette's Journal

## 2025-02-15 - Discord Bot Async and UX Polish
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. Always use `AsyncOpenAI` for non-blocking responses. Furthermore, Discord users value visual typing indicators to know the bot is actively generating a response.
**Action:** Use `AsyncOpenAI` combined with the `typing()` context manager for visual feedback and asynchronous safety. Use 1900-character truncation with an ellipsis to avoid exceeding Discord's message size limit.
