## 2026-05-14 - Real-Time Typing Indicators and Prompt Fallbacks for Discord Bots
**Learning:** Conversational bots that run asynchronous AI completions without a Discord typing indicator leave users uncertain if their message was received or dropped. Additionally, mentioning the bot without prompt text causes empty payload submissions or silent failures instead of helpful onboarding guidance.
**Action:** Always wrap async model completion calls in `async with message.channel.typing():` and provide friendly guidance when user prompt content is empty after mention stripping.
