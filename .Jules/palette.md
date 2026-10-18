## 2026-05-14 - Non-blocking UI Feedback and Typing Status
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, preventing typing status context (`async with message.channel.typing()`) and concurrent event processing. Switching to `AsyncOpenAI` paired with `message.channel.typing()` provides smooth visual progress feedback to users in Discord.
**Action:** Always prefer non-blocking async SDKs and leverage framework status/typing indicators when performing long-running API requests.
