from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_empty_mention():
    mock_user = MagicMock()
    mock_user.id = 123456

    mock_author = MagicMock()
    mock_author.id = 999999

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel.id = 0
    mock_message.content = "<@123456>"

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)

        await bot.on_message(mock_message)

        mock_message.reply.assert_called_once_with(
            "Xin chào! Bạn muốn hỏi gì ạ? Hãy nhập câu hỏi của bạn nhé. 😊"
        )


@pytest.mark.asyncio
async def test_on_message_success():
    mock_user = MagicMock()
    mock_user.id = 123456

    mock_author = MagicMock()
    mock_author.id = 999999

    mock_typing_cm = AsyncMock()
    mock_typing_cm.__aenter__ = AsyncMock(return_value=None)
    mock_typing_cm.__aexit__ = AsyncMock(return_value=None)

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel.id = 123
    mock_message.channel.typing = MagicMock(return_value=mock_typing_cm)
    mock_message.content = "Xin chào AI"

    bot.CHANNEL_ID = 123

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Xin chào bạn!"))]

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response

            await bot.on_message(mock_message)

            mock_create.assert_called_once()
            mock_message.reply.assert_called_once_with("Xin chào bạn!")


@pytest.mark.asyncio
async def test_on_message_error_handling():
    mock_user = MagicMock()
    mock_user.id = 123456

    mock_author = MagicMock()
    mock_author.id = 999999

    mock_typing_cm = AsyncMock()
    mock_typing_cm.__aenter__ = AsyncMock(return_value=None)
    mock_typing_cm.__aexit__ = AsyncMock(return_value=None)

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel.id = 123
    mock_message.channel.typing = MagicMock(return_value=mock_typing_cm)
    mock_message.content = "Lỗi rùi"

    bot.CHANNEL_ID = 123

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.side_effect = Exception("API connection error")

            await bot.on_message(mock_message)

            mock_message.reply.assert_called_once_with("❌ Lỗi: API connection error")
