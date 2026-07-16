## 2025-05-14 - Improve responsiveness and visual feedback
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. Always use `AsyncOpenAI` for non-blocking responses. Additionally, `async with message.channel.typing()` provides essential visual feedback for longer AI generations.
**Action:** Use `AsyncOpenAI` and `message.channel.typing()` for all future AI integrations.
