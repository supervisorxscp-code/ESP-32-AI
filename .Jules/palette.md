# Palette UX Journal

## 2025-02-12 - Discord Async AI and Typing Visual State
**Learning:** In asynchronous frameworks like `discord.py`, synchronous requests with `OpenAI` client block the entire event loop, causing the bot to freeze and become unresponsive to other commands/users. Showing immediate visual feedback through a typing indicator (`message.channel.typing()`) is essential to let the user know the bot is generating a response.
**Action:** Use `AsyncOpenAI` for AI completions in Discord bots, wrapping completion calls in `async with message.channel.typing():` to show a loading/typing indicator without blocking other concurrent user interactions.
