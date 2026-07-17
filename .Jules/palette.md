# Palette Journal

## 2025-02-13 - Non-blocking Discord bot interactions with async clients and visual typing states
**Learning:** In asynchronous chat frameworks like `discord.py`, using synchronous HTTP requests blocks the entire client thread/event loop, making the bot unresponsive to other users. Additionally, when generative AI APIs take several seconds to respond, providing a visual loading cue (like a typing status indicator) immediately is crucial for satisfying user experience.
**Action:** Always utilize async client implementations (e.g., `AsyncOpenAI`) and trigger a non-blocking visual state (e.g., `async with message.channel.typing():`) before awaiting long-running API calls.
