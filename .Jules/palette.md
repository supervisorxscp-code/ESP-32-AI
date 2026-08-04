## 2025-02-14 - Non-blocking AsyncOpenAI and Typing Indicators
**Learning:** In asynchronous frameworks like discord.py, using a synchronous AI client (e.g. openai.OpenAI) blocks the entire event loop. Always use AsyncOpenAI for non-blocking responses. Also, using async with message.channel.typing() provides an immediate visual feedback/typing indicator to the user.
**Action:** Switch any synchronous OpenAI calls in async contexts to AsyncOpenAI and wrap the API requests with typing state indicators to ensure smooth user feedback.
