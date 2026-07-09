## 2025-05-14 - [Blocking Async Event Loop]
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g., `openai.OpenAI`) blocks the entire event loop. This prevents the bot from responding to other events and makes UX indicators (like typing indicators) lag or fail to appear.
**Action:** Always prefer `AsyncOpenAI` and properly `await` completion calls within Discord bot event handlers.
