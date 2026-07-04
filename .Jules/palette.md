## 2025-05-22 - Async AI client for Discord bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g., `openai.OpenAI`) blocks the entire event loop. This prevents the bot from responding to other events and makes visual indicators like "typing" lag or not appear at all.
**Action:** Always prefer `AsyncOpenAI` for AI completions in Discord bots to maintain responsiveness and ensure smooth visual feedback.
