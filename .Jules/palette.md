# Palette's Journal

## 2025-02-17 - Discord Typing Indicator Feedback
**Learning:** In Discord bots, users experience perceived latency and uncertainty during AI completion without visual feedback. Utilizing Discord's `channel.typing()` context manager gives immediate visual feedback ("Bot is typing...") while waiting for response generation.
**Action:** Always wrap async completion calls in `async with message.channel.typing():`.
