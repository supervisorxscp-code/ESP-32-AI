from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_triggers_typing_and_replies():
    mock_message = MagicMock()
    mock_message.author = MagicMock()
    mock_message.channel.id = 12345
    mock_message.content = "Xin chào"
    mock_message.reply = AsyncMock()

    # Mock typing context manager
    typing_cm = MagicMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing = MagicMock(return_value=typing_cm)

    # Mock bot.user
    mock_bot_user = MagicMock()
    mock_bot_user.id = 99999

    # Mock client.chat.completions.create
    mock_choice = MagicMock()
    mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì?"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user), \
         patch.object(bot, "CHANNEL_ID", 12345), \
         patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response):

        await bot.on_message(mock_message)

        # Verify typing was activated
        mock_message.channel.typing.assert_called_once()
        typing_cm.__aenter__.assert_awaited_once()
        typing_cm.__aexit__.assert_awaited_once()

        # Verify reply was sent
        mock_message.reply.assert_awaited_once_with("Chào bạn! Tôi có thể giúp gì?")


@pytest.mark.asyncio
async def test_on_message_handles_exception_with_error_reply():
    mock_message = MagicMock()
    mock_message.author = MagicMock()
    mock_message.channel.id = 12345
    mock_message.content = "Test lỗi"
    mock_message.reply = AsyncMock()

    typing_cm = MagicMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing = MagicMock(return_value=typing_cm)

    mock_bot_user = MagicMock()
    mock_bot_user.id = 99999

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user), \
         patch.object(bot, "CHANNEL_ID", 12345), \
         patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, side_effect=Exception("API timeout")):

        await bot.on_message(mock_message)

        mock_message.channel.typing.assert_called_once()
        mock_message.reply.assert_awaited_once_with("❌ Lỗi: API timeout")
