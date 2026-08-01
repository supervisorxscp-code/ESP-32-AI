# Palette Journal

## 2025-02-18 - Discord Bot Asynchronous Generation Feedback
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client blocks the entire event loop, causing the bot to freeze for other users. Using `AsyncOpenAI` coupled with `async with message.channel.typing()` provides a visual "is typing" indicator, resolving UI latency anxiety and keeping the event loop unblocked.
**Action:** Always utilize non-blocking async APIs for LLM generations in chat apps and wrap the call in a visual typing context managers to provide immediate, delightful visual feedback.
