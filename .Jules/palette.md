## 2024-08-11 - Event Loop Block Prevention with AsyncOpenAI
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire single-threaded event loop, leading to lag, unresponsive UI/interactions, and poor UX. Always use `AsyncOpenAI` for non-blocking responses.
**Action:** Always wrap API and integration calls with async clients/libraries (e.g., `AsyncOpenAI`, `aiohttp`) when operating inside discord bots or async runtimes to ensure UI actions/typing indicators remain responsive.
