## 2025-02-20 - Discord Bot Interactive Feedback & Async UX
**Learning:** In chat interface applications like Discord bots, absent visual indicators during long async AI completion calls make the bot feel unresponsive or broken. Furthermore, sending empty prompts when users tag a bot without query text leads to unnecessary API calls and confusing errors.
**Action:** Always wrap AI completion generation in `async with channel.typing():` for immediate visual feedback, validate user input non-emptiness before making API calls, and use async client instances to prevent event loop blocking.
