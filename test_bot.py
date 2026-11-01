from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_triggers_typing_and_reply():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 123456

    mock_author = MagicMock()
    mock_author.id = 999999

    mock_channel = MagicMock()
    mock_channel.id = bot.CHANNEL_ID

    typing_cm = AsyncMock()
    typing_cm.__aenter__.return_value = None
    typing_cm.__aexit__.return_value = None
    mock_channel.typing.return_value = typing_cm

    mock_message = MagicMock()
    mock_message.author = mock_author
    mock_message.channel = mock_channel
    mock_message.content = "Xin chào!"
    mock_message.reply = AsyncMock()

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì cho bạn?"
    mock_response.choices = [mock_choice]

    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response),
    ):
        await bot.on_message(mock_message)

    mock_channel.typing.assert_called_once()
    mock_message.reply.assert_awaited_once_with("Chào bạn! Tôi có thể giúp gì cho bạn?")


@pytest.mark.asyncio
async def test_on_message_ignores_bot_own_messages():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 123456

    mock_message = MagicMock()
    mock_message.author = mock_bot_user

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)

    mock_message.reply.assert_not_called()
