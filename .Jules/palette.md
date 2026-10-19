## 2025-05-18 - Non-Blocking Feedback and Context Indicators in Discord Bots
**Learning:** In Discord bots using `discord.py`, synchronous I/O blocks the main event loop, causing visual indicators like `message.channel.typing()` to stall or fail. Using `AsyncOpenAI` alongside `async with message.channel.typing()` provides smooth, non-blocking visual feedback to users that their request is actively processing.
**Action:** Always pair `AsyncOpenAI` with `async with message.channel.typing()` when generating AI responses in Discord bots.
