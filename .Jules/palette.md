## 2025-05-14 - Discord Bot Feedback Loop
**Learning:** For Discord bots, displaying a "typing" indicator via `message.channel.typing()` provides immediate visual feedback that the bot is processing a request, which is essential when using slower async AI completions.
**Action:** Always wrap long-running async operations in a typing context when building chat-based interfaces.
