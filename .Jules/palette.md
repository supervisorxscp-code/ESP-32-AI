# Palette's Journal - UX & Accessibility Learnings

## 2025-02-22 - Discord Bot Empty Prompt Feedback & Typing Indicator
**Learning:** When interacting with a Discord bot via mention, users often send empty mentions without a query. Providing immediate feedback for empty prompts and showing a visual typing indicator during long AI processing significantly improves user satisfaction and perceived responsiveness.
**Action:** Always validate stripped user input before calling AI endpoints and wrap AI generation calls with `async with message.channel.typing():`.
