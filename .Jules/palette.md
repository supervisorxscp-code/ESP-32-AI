## 2025-02-18 - Discord Async Typing Indicator & Non-blocking Completions
**Learning:** In asynchronous chat apps like `discord.py`, blocking calls freeze the bot for all users. Wrapping API requests in `async with message.channel.typing():` paired with `AsyncOpenAI` provides immediate feedback without blocking the event loop.
**Action:** Always use non-blocking async clients and native visual indicators (`message.channel.typing()`) when performing background or API operations in bot applications.
