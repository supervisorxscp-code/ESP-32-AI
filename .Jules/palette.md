# Palette UX Journal

## 2025-02-15 - Async Non-blocking API Calls and Typing Cues in Chatbots
**Learning:** In asynchronous environments like Discord (`discord.py`), executing synchronous operations blocks the event loop, causing visual lag and preventing the bot from handling other actions. Wrapping API calls in `async with message.channel.typing()` provides immediate visual feedback, significantly improving perceived performance, while `AsyncOpenAI` guarantees responsive and scalable non-blocking execution.
**Action:** Always use `AsyncOpenAI` instead of `OpenAI` in async applications, and use immediate visual feedback (like typing indicators) for long-running operations.
