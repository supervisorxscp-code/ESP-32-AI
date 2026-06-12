## 2026-06-12 - [Improved AI Response Feedback]
**Learning:** In Discord bots, users can feel disconnected when waiting for a large language model to generate a response. Providing immediate visual feedback via a typing indicator significantly improves the perceived responsiveness and UX. Additionally, gracefully handling long responses with an ellipsis instead of a hard cut-off maintains information integrity and sets better expectations.
**Action:** Always use `async with channel.typing():` when performing asynchronous operations like AI completion in Discord bots.
