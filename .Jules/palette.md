# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-01-16 - Non-blocking Event Loop & Loading Indicators in Discord Bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. Using `AsyncOpenAI` keeps the bot responsive. Additionally, using `async with message.channel.typing()` provides visual feedback that the bot is actively generating a response. Truncating long responses with `...` prevents message delivery failures.
**Action:** Always use `AsyncOpenAI` for AI completions in Discord bots, wrap generation inside `typing()` context, and properly truncate outputs to 1900 characters with an ellipsis indicator.
