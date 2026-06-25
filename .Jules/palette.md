## 2024-05-23 - Async and UX in Discord Bots
**Learning:** In asynchronous frameworks like discord.py, using a synchronous AI client blocks the entire event loop, preventing the bot from responding to other users and making the "typing" indicator appear laggy or non-existent.
**Action:** Always use `AsyncOpenAI` and wrap AI completions in `async with message.channel.typing()` to ensure responsiveness and provide immediate visual feedback.
