## 2025-02-18 - Non-blocking async Discord events with typing status
**Learning:** Using synchronous clients (such as standard OpenAI Client) inside asynchronous handlers like `on_message` blocks the entire asyncio event loop, causing UX lag or bot unresponsiveness. Using `AsyncOpenAI` coupled with the typing feedback context manager (`async with message.channel.typing():`) provides a seamless, non-blocking user experience in Discord.
**Action:** Always use `AsyncOpenAI` with `await` and utilize `message.channel.typing()` for asynchronous event loop safety and real-time response feedback.
