## 2025-05-15 - Async AI client in Discord
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, preventing the bot from responding to other events and making "typing" indicators lag.
**Action:** Always prefer `AsyncOpenAI` for AI completions in asynchronous contexts to maintain responsiveness.
