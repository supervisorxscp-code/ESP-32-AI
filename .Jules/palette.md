## 2025-05-15 - Async UX in Discord Bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, preventing the bot from responding and making indicators like `.typing()` lag. Always prefer `AsyncOpenAI` for AI completions to ensure a smooth, responsive UI.
**Action:** Always transition synchronous AI clients to asynchronous ones when working with Discord bots or similar event-driven frameworks.
