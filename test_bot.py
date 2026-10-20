from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch
import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_empty_prompt():
    mock_author = MagicMock()
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345
    mock_author.__eq__ = lambda self, other: False

    mock_message = MagicMock()
    mock_message.author = mock_author
    mock_message.channel.id = 0
    mock_message.content = "<@12345>"
    mock_message.reply = AsyncMock()

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)

    mock_message.reply.assert_called_once_with(
        "Bạn cần hỏi gì tôi thế? Hãy nhập câu hỏi sau khi nhắc tên tôi nhé!"
    )


@pytest.mark.asyncio
async def test_on_message_typing_and_response():
    mock_author = MagicMock()
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345

    mock_message = MagicMock()
    mock_message.author = mock_author
    mock_message.channel.id = 0
    mock_message.content = "<@12345> Hello"
    mock_message.reply = AsyncMock()

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing.return_value = typing_ctx

    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="Xin chào! Tôi có thể giúp gì?"))]

    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_completion),
    ):
        await bot.on_message(mock_message)

    mock_message.channel.typing.assert_called_once()
    mock_message.reply.assert_called_once_with("Xin chào! Tôi có thể giúp gì?")


@pytest.mark.asyncio
async def test_on_message_truncation():
    mock_author = MagicMock()
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345

    mock_message = MagicMock()
    mock_message.author = mock_author
    mock_message.channel.id = 0
    mock_message.content = "<@12345> Tell me a long story"
    mock_message.reply = AsyncMock()

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing.return_value = typing_ctx

    long_response = "A" * 2000
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content=long_response))]

    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_completion),
    ):
        await bot.on_message(mock_message)

    expected_response = "A" * 1897 + "..."
    mock_message.reply.assert_called_once_with(expected_response)
