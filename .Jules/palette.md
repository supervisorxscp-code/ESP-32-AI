## 2025-06-13 - Enhance Visual Feedback in Discord
**Learning:** Using `message.channel.typing()` provides immediate visual confirmation that the bot is processing a request, which is crucial for perceived performance in chat interfaces. Truncating long responses with an ellipsis instead of a hard cut improves readability.
**Action:** Always include a "typing..." state for long-running async operations in Discord bots and ensure response lengths are gracefully handled.
