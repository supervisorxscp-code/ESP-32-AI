## 2025-01-24 - Async AI Client in Discord Bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g., `openai.OpenAI`) blocks the entire event loop. This prevents the bot from responding to other events and makes UX indicators (like typing) lag or fail to appear.
**Action:** Always prefer `AsyncOpenAI` for AI completions to ensure the event loop remains responsive and visual feedback is immediate.
