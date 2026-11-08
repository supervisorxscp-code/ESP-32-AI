## 2025-05-14 - Discord Bot Non-Blocking AI & Typing Indicators
**Learning:** In asynchronous chat frameworks like `discord.py`, using synchronous clients blocks the whole event loop and stops the bot from rendering visual feedback like typing indicators. Pairing `AsyncOpenAI` with `async with channel.typing():` provides immediate responsive feedback while preventing the interface from freezing.
**Action:** When working on chat bots or async interfaces with AI backends, always use non-blocking async clients wrapped in typing/loading indicator context managers.
