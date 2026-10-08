# Palette's Journal - ESP-32-AI

## 2026-03-31 - Discord Bot Asynchronous Typing & Empty Mention Guidance
**Learning:** In asynchronous Discord bots (`discord.py`), users expect immediate visual feedback when waiting for LLM completions; without `async with message.channel.typing():`, the interface appears unresponsive. Additionally, stripping mentions can leave empty prompts, which should be caught early with helpful prompt guidance rather than sending empty requests to the LLM.
**Action:** Always wrap async AI completions in `async with message.channel.typing():` and provide user guidance for empty prompts after stripping mention tags (`<@id>` and `<@!id>`).
