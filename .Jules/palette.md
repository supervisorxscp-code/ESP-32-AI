# Palette's Journal - Critical UX & Accessibility Learnings

## 2025-05-15 - Discord Bot Asynchronous Feedback & Input Validation
**Learning:** In Discord bots using `discord.py`, synchronous API calls (e.g., standard `OpenAI`) block the event loop and prevent proper UI feedback like typing indicators (`async with message.channel.typing()`).
**Action:** Always use `AsyncOpenAI` alongside `async with message.channel.typing()` for non-blocking responses and immediate visual feedback in Discord.
