## 2026-05-14 - Discord Bot Typing Indicator and Async Event Loop
**Learning:** In chat bots built with async frameworks (like discord.py), calling a synchronous API client blocks the entire event loop, freezing all bot interactions and status updates across the server. Pairing an asynchronous client (AsyncOpenAI) with `async with channel.typing()` provides instantaneous visual feedback ("Bot is typing...") while preventing UI freezes.
**Action:** Always wrap long-running chat completions inside `async with channel.typing():` and use non-blocking async clients.
