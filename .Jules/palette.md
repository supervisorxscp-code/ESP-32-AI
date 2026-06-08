# Palette's Journal - UX & Accessibility Learnings

This journal tracks critical UX and accessibility learnings discovered during the development process.

## 2025-05-22 - [Immediate feedback in chat interfaces]
**Learning:** In chat-based interfaces like Discord, providing immediate visual feedback (e.g., "typing..." indicator) is essential during long-running async operations like AI generation to reduce perceived latency.
**Action:** Always wrap AI generation calls in `async with channel.typing()` when using `discord.py`, and ensure non-blocking async clients (like `AsyncOpenAI`) are used to keep the event loop responsive.
