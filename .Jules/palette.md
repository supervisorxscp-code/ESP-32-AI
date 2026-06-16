## 2025-05-14 - Discord AI Feedback
**Learning:** Users can feel uncertain if a bot is actually processing their long-form AI requests. Providing immediate visual feedback via `message.channel.typing()` significantly improves the perceived responsiveness.
**Action:** Always wrap async AI generation calls in a typing context manager in Discord bots.
