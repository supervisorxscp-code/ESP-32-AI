# Palette's Journal - ESP-32-AI

This journal documents critical UX and accessibility learnings for the ESP-32-AI Discord bot.

## 2025-05-15 - Async UX in Discord
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client blocks the entire event loop, making the bot unresponsive and causing the typing indicator to lag or not appear.
**Action:** Always use `AsyncOpenAI` for AI completions and wrap the processing in `async with message.channel.typing()`.
