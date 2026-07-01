## 2026-07-01 - Bot Responsiveness and Message Limits
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g., `openai.OpenAI`) blocks the entire event loop, preventing the bot from responding and making indicators lag. Always prefer `AsyncOpenAI` for AI completions. Visual feedback like `message.channel.typing()` is essential for perceived performance when waiting for AI generation.
**Action:** Always use `AsyncOpenAI` and `async with message.channel.typing()` in Discord bots to ensure a smooth user experience.
