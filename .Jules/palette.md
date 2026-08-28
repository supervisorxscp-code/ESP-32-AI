## 2025-02-23 - Async Typing Feedback & Empty Mention Guard in Discord Bot
**Learning:** In Discord bots powered by LLMs, long synchronous completions block the asyncio event loop and leave users without visual feedback. Always use `AsyncOpenAI` with `async with message.channel.typing():` and guard against empty mention prompts to provide immediate, clear UX feedback.
**Action:** When updating Discord bot interfaces, combine async clients, channel typing indicators, and empty prompt fallbacks.
