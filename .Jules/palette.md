## 2025-05-15 - [Discord Bot Feedback UX]
**Learning:** Using `async with message.channel.typing()` provides immediate visual feedback to the user, confirming that the bot has received the input and is generating a response. This is especially important for AI completions which can have high latency.
**Action:** Always wrap asynchronous AI completion requests in a typing indicator context manager to improve perceived performance and user trust.
