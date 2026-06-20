## 2025-06-20 - Feedback for AI Bot Interactions
**Learning:** AI response latency can make users feel the bot is unresponsive. Providing immediate visual feedback through Discord's typing indicator significantly improves the perceived speed and reliability of the interaction.
**Action:** Always use `async with message.channel.typing()` when performing long-running tasks like AI generation to keep the user informed.
