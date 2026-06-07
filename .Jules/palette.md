## 2025-05-15 - [Discord Bot Typing Feedback]
**Learning:** In Discord bots, users often feel the interface is unresponsive during long-running AI generations. Using `async with message.channel.typing():` provides immediate visual feedback, indicating that the bot is processing the request. Switching to asynchronous API clients (like `AsyncOpenAI`) is essential to avoid blocking the bot's event loop while waiting for these responses.
**Action:** Always use `async with message.channel.typing()` for AI-driven responses in Discord and ensure the underlying API calls are non-blocking.
