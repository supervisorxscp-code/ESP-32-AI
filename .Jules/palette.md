# Palette UX Journal

## 2025-05-18 - Visual Typing Indicator & Non-Blocking Async AI Feedback in Discord
**Learning:** In Discord conversational bots, generative LLM queries take several seconds to stream or return responses. Without `async with message.channel.typing():`, users receive no visual feedback that their request is being processed, often leading to repeated questions or assuming the bot is frozen. Additionally, using synchronous AI client calls in `discord.py` blocks the event loop, disrupting typing statuses and message receipt across channels.
**Action:** Always combine `AsyncOpenAI` with `async with message.channel.typing():` to provide immediate, non-blocking visual feedback on message processing.
