## 2026-08-13 - Non-blocking Discord AI Bot Integrations
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (such as `openai.OpenAI`) blocks the entire event loop, causing visual typing indicator lag and making the bot unresponsive to other channel events or user interactions during long API requests.
**Action:** Always use `AsyncOpenAI` for AI completions in Discord bots. Wrap completions in `async with message.channel.typing()` to provide immediate, non-blocking visual feedback to the users while the response is being generated.
