## 2025-06-14 - [Async Transition for Typing Indicator]
**Learning:** In `discord.py`, implementing a typing indicator (`message.channel.typing()`) during long-running tasks like AI generation requires transitioning to an asynchronous client (e.g., `AsyncOpenAI`) to avoid blocking the event loop and ensure the bot remains responsive.
**Action:** Always verify if external API clients are synchronous and refactor to their asynchronous counterparts when adding visual feedback like typing indicators.
