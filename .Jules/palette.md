## 2025-05-18 - Non-blocking Async Completion & Typing Indicator
**Learning:** In asynchronous Discord bots (`discord.py`), synchronous blocking API calls (e.g. standard `OpenAI` client) block the event loop, stopping typing status indicators and freezing bot responsiveness for all users.
**Action:** Always use `AsyncOpenAI` with `await` and wrap long-running generation tasks in `async with message.channel.typing():` to provide immediate visual UX feedback in Discord.
