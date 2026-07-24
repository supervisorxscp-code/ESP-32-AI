# Palette's Journal

## 2025-01-20 - Non-blocking async Discord interactions
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (like `OpenAI`) blocks the entire event loop, causing the bot to freeze and become unresponsive to other users or events during API calls.
**Action:** Always use `AsyncOpenAI` with `await` for completions, and wrap generation in `async with message.channel.typing()` to show a typing indicator, which provides immediate and non-blocking visual feedback.
