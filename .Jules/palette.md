# Palette Journal - ESP-32-AI Discord Bot

## 2025-02-18 - Prevent Discord Bot Event Loop Block with AsyncOpenAI & Typing Feedback
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client blocks the entire event loop, preventing the bot from responding to other users or events concurrently. Utilizing `AsyncOpenAI` ensures non-blocking I/O. Additionally, integrating the `message.channel.typing()` context manager provides a crucial visual feedback (typing indicator) to the user while waiting for the AI response.
**Action:** Always refactor synchronous AI completion calls in Discord bots to use asynchronous alternatives (`AsyncOpenAI` and `await`), and wrap long-running operations in `async with message.channel.typing()` to elevate user experience.
