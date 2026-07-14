## 2026-07-14 - Interaction Responsiveness & Feedback
**Learning:** Using synchronous AI clients in `discord.py` blocks the event loop, causing visual feedback like typing indicators to lag or fail. Ellipsis suffixes on truncated messages provide necessary context for incomplete content.
**Action:** Always prefer `AsyncOpenAI` and ensure visual indicators like `message.channel.typing()` are used within an async context to maintain a smooth UX.
