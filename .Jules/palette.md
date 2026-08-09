# Palette's UX Journal

## 2025-02-15 - Async AI Generation in Discord
**Learning:** In asynchronous frameworks like discord.py, calling a synchronous OpenAI client blocks the main execution flow and causes the bot to become unresponsive to other events or heartbeats. Always use AsyncOpenAI and show visual indicators like typing state so users know the bot is actively responding.
**Action:** Use `AsyncOpenAI` for AI operations and wrap long-running generation tasks in `async with channel.typing():`.
