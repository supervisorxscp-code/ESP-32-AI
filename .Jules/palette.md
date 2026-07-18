# Palette's Journal

## 2026-07-18 - Async OpenAI & Non-blocking Typing Indicator in Discord.py
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (like `openai.OpenAI`) blocks the entire Discord bot's event loop. Always use `AsyncOpenAI` for non-blocking API calls. Additionally, providing the `async with channel.typing():` context manager gives immediate visual feedback to the user while waiting for the API response.
**Action:** Always wrap async API calls in `async with channel.typing():` and use non-blocking `AsyncOpenAI` client in Discord bots.
