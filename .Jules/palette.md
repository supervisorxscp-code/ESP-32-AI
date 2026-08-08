# Palette's Journal - ESP-32-AI

## 2025-02-18 - Non-blocking Async Discord Interaction & Typing Indicator
**Learning:** Using synchronous HTTP calls (like synchronous `OpenAI` client) in `discord.py` blocks the main single-threaded event loop, freezing all bot activities and resulting in a terrible user experience. Also, without a visual indicator (like typing status), users are left wondering if the bot is actually processing their request.
**Action:** Always use `AsyncOpenAI` for AI completions in Discord bots, and wrap the asynchronous call inside `async with message.channel.typing():` to provide immediate, friendly visual feedback.
