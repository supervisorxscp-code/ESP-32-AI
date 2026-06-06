## 2025-05-15 - [Discord Bot Responsiveness]
**Learning:** In Discord bots, using synchronous API calls blocks the entire event loop, causing the bot to become unresponsive to other events. Combining `AsyncOpenAI` with `async with message.channel.typing()` provides both technical responsiveness and visual feedback to the user.
**Action:** Always use asynchronous clients for external APIs in Discord bots and wrap long-running generation tasks in a typing indicator context.
