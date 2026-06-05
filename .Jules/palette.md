## 2025-05-14 - [Typing Indicator for Discord Bot]
**Learning:** For LLM-powered Discord bots, the delay between a user message and the bot's response can be several seconds. Without a typing indicator, the user might think the bot is broken or didn't receive the message.
**Action:** Always use `async with channel.typing():` when performing long-running tasks like AI generation in Discord bots.
