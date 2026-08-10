# Palette UX Journal

## 2026-08-10 - Async API Calls & Visual State Feedback in Chatbots
**Learning:** In asynchronous applications (such as Discord bots running on `discord.py`), executing blocking synchronous code (such as synchronous API calls using a synchronous OpenAI client) halts the single-threaded event loop and delays message handling for all users. Furthermore, lack of immediate visual feedback during slow API computations can make the application feel unresponsive or broken.
**Action:** Always use non-blocking asynchronous clients (`AsyncOpenAI`) and pair slow backend request cycles with rich visual state feedback (such as Discord's `async with channel.typing():` context manager) to improve UX and responsiveness.
