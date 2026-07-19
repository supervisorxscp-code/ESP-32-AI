# Palette's Journal

## 2025-02-27 - Discord Bot Event Loop Blocking
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. Always use `AsyncOpenAI` for non-blocking responses to keep the bot responsive.
**Action:** Avoid synchronous API clients in async handlers; wrap network requests with asynchronous equivalents and show visual progress feedback (e.g. `async with message.channel.typing()`).
