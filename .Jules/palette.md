# Palette's Journal

## 2025-02-02 - Async AI client and typing indicators in Discord
**Learning:** Using a synchronous AI client blocks the Discord bot's event loop, creating a poor user experience. Proper Discord UX requires `AsyncOpenAI`, visual typing indicators (`async with message.channel.typing()`), and elegant truncation with ellipsis.
**Action:** Always implement AsyncOpenAI, channel typing context managers, and handle truncation gracefully with `...` when responses exceed Discord's size limits.
