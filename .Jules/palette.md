## 2025-05-22 - Async AI client in Discord Bots
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g. `openai.OpenAI`) blocks the entire event loop, preventing the bot from responding and making indicators lag. Always prefer `AsyncOpenAI` for AI completions.
**Action:** When working with Discord bots or other async frameworks, always verify that external API clients are used asynchronously.

## 2025-05-22 - Visual Feedback for AI Generation
**Learning:** Users can find AI generation times frustrating if there is no feedback. Using a typing indicator (`message.channel.typing()`) provides immediate visual confirmation that the bot is working.
**Action:** Always wrap long-running async operations in a typing indicator or similar loading state.
