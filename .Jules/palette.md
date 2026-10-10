## 2025-05-18 - Visual Typing Indicators in Discord Bots
**Learning:** Asynchronous AI completion calls leave users without visual feedback unless a typing state is displayed, leading to confusion or duplicate requests.
**Action:** Always wrap asynchronous generation calls in `async with message.channel.typing():` and provide user guidance on empty inputs.
