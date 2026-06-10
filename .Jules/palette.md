## 2026-06-10 - [Discord UX: Immediate Feedback]
**Learning:** In chat-based interfaces like Discord, high-latency operations (like AI generation) can make the bot feel unresponsive or broken if no immediate visual feedback is provided.
**Action:** Always use `async with message.channel.typing():` for AI response generation in Discord bots to indicate that the bot is actively processing the request.
