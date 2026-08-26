## 2025-05-18 - Discord AI Bot Async Typing Indicator & Empty Prompt Guidance
**Learning:** In Discord bots, using non-blocking async completion calls with `async with message.channel.typing()` provides essential instant visual feedback to users that their prompt is being processed. Checking for empty input after mention stripping allows presenting friendly prompt guidance rather than sending blank requests to the AI model.
**Action:** Always combine async non-blocking execution with visual typing indicators and empty prompt handling in chat interface interactions.
