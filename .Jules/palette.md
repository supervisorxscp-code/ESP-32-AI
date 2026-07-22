# Palette's UX & Accessibility Journal

This journal tracks critical UX and accessibility learnings for the ESP-32-AI Discord bot repository.

## 2025-02-12 - Non-blocking Discord AI Interactions
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, causing severe latency and unresponsiveness for all users. Always use `AsyncOpenAI` for non-blocking responses.
**Action:** Replace `OpenAI` with `AsyncOpenAI` and await completions to ensure smooth asynchronous message handling.
