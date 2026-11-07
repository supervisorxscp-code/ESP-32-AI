# Palette's Journal

## 2026-05-14 - Discord Bot Async Feedback and Typing State
**Learning:** In chat bots like Discord bots, prolonged silence while awaiting AI responses creates uncertainty. Utilizing `async with channel.typing()` provides clear micro-UX loading feedback, and pairing it with non-blocking `AsyncOpenAI` prevents freezing the bot event loop for all users.
**Action:** Always wrap AI API calls with Discord typing indicators and use asynchronous clients for smooth chat UX.
