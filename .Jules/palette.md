## 2025-05-15 - Importance of Async Clients for Discord UX
**Learning:** In Discord bots (specifically `discord.py`), using synchronous API clients (like `OpenAI`) blocks the event loop. This prevents the `async with message.channel.typing()` context manager from displaying the "typing..." indicator reliably and makes the bot unresponsive to other events during generation.
**Action:** Always use asynchronous clients (e.g., `AsyncOpenAI`) when integrating external APIs to ensure smooth UX and responsive typing indicators.
