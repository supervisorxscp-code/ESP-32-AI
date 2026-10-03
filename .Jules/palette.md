# Palette's Journal

## 2024-05-18 - Bot Prompt Initialization & UX
**Learning:** For Discord AI bots, when user input is empty after mention stripping (e.g., `@Bot`), making an API call wastes resources and yields confusing responses.
**Action:** Prompt the user directly with a helpful message in Vietnamese when user input is empty.
