## 2025-05-22 - Improved AI Interaction Feedback
**Learning:** In chat-based interfaces like Discord, providing immediate visual feedback during long-running async operations (like AI generation) is crucial for responsiveness. Using `async with channel.typing()` ensures the user knows the bot is working.
**Action:** Always wrap AI generation calls in `async with message.channel.typing()` and use `AsyncOpenAI` to avoid blocking the event loop.

## 2025-05-22 - Graceful Content Truncation
**Learning:** Abruptly cutting off text at Discord's character limit can be confusing. Appending an ellipsis (...) provides a visual cue that the message was shortened.
**Action:** Implement a `MAX_MESSAGE_LENGTH` constant (set to 1900 to leave room for the ellipsis and safety margin) and append "..." if truncation occurs.
