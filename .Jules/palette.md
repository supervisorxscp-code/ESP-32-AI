# Palette's UX Journal

## 2025-02-15 - Discord Bot UX responsiveness
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, causing lag and unresponsive behavior. Always use `AsyncOpenAI` for non-blocking responses. Additionally, always use `async with message.channel.typing()` to show immediate visual feedback to the user while the model generates its response.
**Action:** Replace synchronous `OpenAI` client with `AsyncOpenAI` and wrap AI generation in a Discord typing context manager.
