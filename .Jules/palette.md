# Palette's UX Journal - ESP-32-AI

This journal documents critical UX and accessibility learnings for the ESP-32-AI project.

## 2025-01-25 - Async OpenAI and Typing Feedback
**Learning:** In asynchronous frameworks like `discord.py`, utilizing a synchronous AI client blocks the entire event loop, causing responsiveness issues. Additionally, providing no typing status indicator creates a perceived lag.
**Action:** Use `AsyncOpenAI` for asynchronous non-blocking API requests, and wrap AI generation inside `async with message.channel.typing()` to give immediate visual feedback.
