## 2026-07-12 - [Discord AI Bot Responsiveness]
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. This prevents the bot from responding to other events and makes UI indicators like `message.channel.typing()` lag or fail to show up promptly.
**Action:** Always prefer `AsyncOpenAI` for AI completions in Discord bots to ensure the event loop remains free for UI feedback and multi-user responsiveness.
