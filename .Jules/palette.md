## 2025-02-18 - Discord Async AI Response & Visual Typing Indicator UX
**Learning:** Using synchronous OpenAI client in `discord.py` blocks the event loop, causing responsiveness issues. Adding `async with message.channel.typing()` provides visual feedback while waiting for AI generation, and empty prompt checks after mention stripping prevent sending empty queries.
**Action:** Always use `AsyncOpenAI` for AI completions in async chat bots, use channel typing context managers for user feedback during processing, and sanitize mentions with helpful fallback prompts.
