## 2025-05-10 - Asynchronous Feedback and Prompt Validation in Discord Bots
**Learning:** In chat interfaces like Discord, long API completion calls without feedback make the bot appear unresponsive. Additionally, sending empty prompts after stripping bot mentions causes unnecessary API errors.
**Action:** Always provide instant visual feedback with `async with channel.typing()` during async processing, and validate empty inputs before triggering AI completions.
