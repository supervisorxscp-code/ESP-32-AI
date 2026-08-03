# Palette's Journal - ESP-32-AI

## 2025-02-14 - Non-blocking asynchronous OpenAI calls & Typing Status in Discord
**Learning:** In asynchronous frameworks like `discord.py`, using synchronous HTTP client requests blocks the single-threaded event loop, degrading the response time of other requests and heartbeat events. Utilizing `AsyncOpenAI` coupled with an asynchronous visual cue like `async with message.channel.typing():` creates a fluid, highly responsive visual experience and guarantees non-blocking bot communication.
**Action:** Always replace synchronous clients (e.g. `openai.OpenAI`) with non-blocking async clients (e.g. `openai.AsyncOpenAI`) and pair with appropriate platform-level loading or typing states.
