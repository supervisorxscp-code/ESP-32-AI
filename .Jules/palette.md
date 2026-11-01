# Palette's Journal - ESP-32-AI

## 2026-05-14 - Real-Time Feedback via Discord Typing Indicator
**Learning:** In chat bots communicating with slow external services or LLM APIs, lack of immediate feedback leaves users uncertain whether their message was received. Using `async with message.channel.typing()` provides instant native visual loading states in Discord while the model generates its response.
**Action:** Always wrap async AI generation calls in `async with message.channel.typing():` and use asynchronous API clients (`AsyncOpenAI`) to avoid freezing the event loop.
