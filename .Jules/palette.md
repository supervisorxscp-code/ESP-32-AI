## 2025-05-22 - Non-blocking AI Responses in Discord
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, preventing the bot from responding to other users and making visual indicators like `typing()` lag or fail to show.
**Action:** Always prefer `AsyncOpenAI` for AI completions and wrap network-bound tasks in `await` to maintain bot responsiveness.
