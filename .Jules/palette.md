## 2025-05-14 - Discord Bot Feedback Pattern
**Learning:** Using `async with message.channel.typing():` provides immediate visual feedback in Discord, which is crucial for perceived performance when waiting for AI-generated responses. Switching to an asynchronous client (`AsyncOpenAI`) prevents blocking the bot's event loop.
**Action:** Always implement a typing/loading state for AI interactions and ensure the main event loop remains non-blocking by using async libraries.
