## 2025-05-22 - Non-blocking AI responsiveness in Discord
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, preventing the bot from responding and making indicators like typing lag.
**Action:** Always prefer `AsyncOpenAI` for AI completions and use `async with message.channel.typing()` to provide immediate visual feedback.
