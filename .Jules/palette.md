## 2025-02-18 - Non-blocking Asynchronous AI Discord bot responses
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. Always use `AsyncOpenAI` for non-blocking responses, and use `async with message.channel.typing()` during AI generation to provide immediate visual feedback.
**Action:** Always refactor synchronous AI clients to `AsyncOpenAI` in Python Discord bots and wrap API requests in typing indicator blocks.
