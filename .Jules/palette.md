## 2025-05-15 - Async AI Client in Discord Bots
**Learning:** Using a synchronous AI client (like `openai.OpenAI`) in an asynchronous framework like `discord.py` blocks the entire event loop. This prevents the bot from processing other events and makes UX features like `message.channel.typing()` lag or fail to appear correctly.
**Action:** Always use `AsyncOpenAI` for AI completions in Discord bots to ensure the event loop remains responsive and visual indicators work smoothly.
