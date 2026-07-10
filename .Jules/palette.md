## 2026-07-10 - Async vs Sync in Discord Bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. This prevents the bot from responding to other events and makes UX indicators like `message.channel.typing()` lag or fail to show consistently.
**Action:** Always prefer `AsyncOpenAI` and `await` completions to ensure the bot remains responsive and visual feedback is immediate.
