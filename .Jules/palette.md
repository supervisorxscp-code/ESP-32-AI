## 2025-05-22 - [Asynchronous AI Clients in Discord Bots]
**Learning:** Using synchronous AI clients in `discord.py` blocks the event loop, making visual feedback like `channel.typing()` unreliable and the bot unresponsive.
**Action:** Always use `AsyncOpenAI` for AI completions in asynchronous frameworks to ensure smooth UX and consistent typing indicators.
