# Palette's Journal - ESP-32-AI

## 2025-05-14 - Initial UX Observations
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, leading to poor responsiveness and potential timeouts. Providing visual feedback (e.g. "typing...") is essential for long-running AI completions to reassure the user.
**Action:** Always use `AsyncOpenAI` and `message.channel.typing()` in Discord bots to ensure a smooth, non-blocking user experience.
