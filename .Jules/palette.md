# Palette's Journal

## 2025-02-17 - Discord Async UX
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. Always use `AsyncOpenAI` for non-blocking responses. Also, using visual typing status like `async with message.channel.typing()` provides immediate visual feedback.
**Action:** Always migrate synchronous clients to `AsyncOpenAI` and wrap long-running operations in channel typing context when working with bots.
