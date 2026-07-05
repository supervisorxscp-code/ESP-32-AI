## 2026-07-05 - Asynchronous AI client for Discord UX
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop. This prevents the bot from updating visual indicators like "typing" states, making the UI feel frozen or laggy while waiting for a response.
**Action:** Always prefer `AsyncOpenAI` and `await` completion calls to keep the bot responsive and ensure visual feedback mechanisms (like `channel.typing()`) work as intended.
