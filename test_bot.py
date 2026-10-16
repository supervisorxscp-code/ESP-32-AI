from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_empty_prompt():
    mock_message = MagicMock()
    mock_message.author = MagicMock()

    mock_bot_user = MagicMock()
    mock_bot_user.id = 123456789

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        mock_message.author = MagicMock()
        mock_message.channel.id = 9999
        mock_message.content = "<@123456789>"
        mock_message.reply = AsyncMock()

        bot.CHANNEL_ID = 1111

        await bot.on_message(mock_message)

        mock_message.reply.assert_called_once_with("Bạn cần hỏi gì tôi thế? Hãy nhập câu hỏi của bạn nhé! 👋")

@pytest.mark.asyncio
async def test_on_message_typing_and_response():
    mock_message = MagicMock()
    mock_bot_user = MagicMock()
    mock_bot_user.id = 123456789

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        mock_message.author = MagicMock()
        mock_message.channel.id = 1111
        mock_message.content = "Xin chào"
        mock_message.reply = AsyncMock()

        typing_cm = AsyncMock()
        typing_cm.__aenter__ = AsyncMock(return_value=None)
        typing_cm.__aexit__ = AsyncMock(return_value=None)
        mock_message.channel.typing = MagicMock(return_value=typing_cm)

        bot.CHANNEL_ID = 1111

        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì cho bạn?"
        mock_completion.choices = [mock_choice]

        with patch.object(bot.client.chat.completions, 'create', new_callable=AsyncMock, return_value=mock_completion) as mock_create:
            await bot.on_message(mock_message)

            mock_message.channel.typing.assert_called_once()
            typing_cm.__aenter__.assert_called_once()
            typing_cm.__aexit__.assert_called_once()

            mock_create.assert_called_once_with(
                model="meta/llama-3.3-70b-instruct",
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý thông minh, trả lời ngắn gọn bằng tiếng Việt."},
                    {"role": "user", "content": "Xin chào"}
                ],
                temperature=0.7,
                max_tokens=800
            )
            mock_message.reply.assert_called_once_with("Chào bạn! Tôi có thể giúp gì cho bạn?")
