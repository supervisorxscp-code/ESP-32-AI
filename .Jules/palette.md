## 2025-05-15 - Discord Bot Typing Feedback
**Learning:** For chatbot interfaces, especially those with variable latency like AI generators, providing immediate visual feedback such as a "typing..." status is crucial for reducing perceived wait time and confirming the system has received the request.
**Action:** Always implement `async with message.channel.typing()` in Discord bots before long-running asynchronous operations to improve UX.
