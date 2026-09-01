## 2025-05-18 - Non-blocking typing feedback in Discord bots
**Learning:** Synchronous OpenAI calls block the Discord event loop during AI generation, causing the bot to freeze and fail to send typing status indicators.
**Action:** Always use `AsyncOpenAI` alongside `async with message.channel.typing():` to provide real-time visual typing feedback while maintaining responsive event loop execution.
