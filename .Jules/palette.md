# Palette's Journal

## 2024-05-23 - Initializing Journal
**Learning:** Always check for `.Jules/palette.md` to ensure consistency with UX patterns.
**Action:** Created this file to track future UX improvements.

## 2024-05-23 - Async AI Client for Discord UX
**Learning:** In asynchronous frameworks like `discord.py`, using a synchronous AI client (e.g., `openai.OpenAI`) blocks the entire event loop. This prevents the bot from responding to other events and makes micro-UX indicators like `message.channel.typing()` lag or fail to appear promptly.
**Action:** Always prefer `AsyncOpenAI` for AI completions in Discord bots to maintain a responsive interface.
