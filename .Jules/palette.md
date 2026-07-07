## 2025-05-15 - Async AI Client in Discord Bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. This prevents the bot from responding to other events and causes the `typing` indicator to lag or not appear at all, significantly degrading the user experience.
**Action:** Always use `AsyncOpenAI` for AI completions in Discord bots to ensure the interface remains responsive and visual feedback (like typing indicators) is immediate.
