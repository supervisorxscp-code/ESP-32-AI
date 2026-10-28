from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_empty_mention():
    mock_user = MagicMock()
    mock_user.id = 12345

    mock_author = MagicMock()
    mock_author.id = 67890

    mock_channel = MagicMock()
    mock_channel.id = 100

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel = mock_channel
    mock_message.content = "<@12345>"

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_user):
        await bot.on_message(mock_message)

    mock_message.reply.assert_called_once_with("Bạn cần tôi giúp gì ạ? Hãy nhập câu hỏi của bạn nhé! 😊")

@pytest.mark.asyncio
async def test_on_message_valid_ai_response():
    mock_user = MagicMock()
    mock_user.id = 12345

    mock_author = MagicMock()
    mock_author.id = 67890

    typing_cm = AsyncMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)

    mock_channel = MagicMock()
    mock_channel.id = 100
    mock_channel.typing = MagicMock(return_value=typing_cm)

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel = mock_channel
    mock_message.content = "<@12345> Xin chào"

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Chào bạn! Tôi là trợ lý AI."))]

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_user), \
         patch.object(bot.client.chat.completions, 'create', new=AsyncMock(return_value=mock_response)):
        await bot.on_message(mock_message)

    mock_channel.typing.assert_called_once()
    mock_message.reply.assert_called_once_with("Chào bạn! Tôi là trợ lý AI.")
