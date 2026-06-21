## 2025-05-15 - Discord Bot Feedback and Truncation Patterns
**Learning:** For chat bots like Discord, providing immediate visual feedback using `typing()` indicators prevents users from thinking the bot is frozen during long AI generations. Additionally, truncating long messages with an ellipsis rather than an abrupt cut-off maintains a more natural conversation flow and informs the user of missing content.
**Action:** Always wrap async AI calls in `async with message.channel.typing()` and implement content-aware truncation with an indicator like `...` when hitting message length limits.
