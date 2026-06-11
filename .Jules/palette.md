## 2025-05-22 - Improved Discord Bot Responsiveness
**Learning:** Users experience anxiety during long AI generation times without visual feedback. In Discord, using the `typing` state provides immediate reassurance that the bot is processing the request. Additionally, synchronous API calls in an asynchronous framework like `discord.py` can block the event loop, causing overall bot sluggishness.
**Action:** Always use `AsyncOpenAI` for AI requests and wrap them in `async with message.channel.typing()` to maintain responsiveness and provide UX feedback.
