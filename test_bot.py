from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_message():
    message = MagicMock()
    message.author = MagicMock()
    message.author.__eq__ = lambda self, other: False
    message.channel = MagicMock()
    message.channel.id = 123456789

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_ctx)

    message.content = "Hello bot"
    message.reply = AsyncMock()
    return message


@pytest.mark.asyncio
async def test_on_message_ignores_self(mock_message):
    mock_bot_user = MagicMock()
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        mock_message.author = mock_bot_user
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_mention(mock_message):
    mock_bot_user = MagicMock()
    mock_bot_user.id = 9999
    with (
        patch.object(
            type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
        ),
        patch.object(mock_bot_user, "mentioned_in", return_value=True),
    ):
        mock_message.content = "<@9999>"
        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with(
            "Bạn hãy nhập câu hỏi hoặc yêu cầu để mình giúp đỡ nhé!"
        )


@pytest.mark.asyncio
async def test_on_message_success(mock_message):
    mock_bot_user = MagicMock()
    mock_bot_user.id = 9999

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Xin chào! Tôi có thể giúp gì cho bạn?"

    with (
        patch.object(
            type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
        ),
        patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
    ):
        bot.CHANNEL_ID = 123456789
        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with("Xin chào! Tôi có thể giúp gì cho bạn?")


@pytest.mark.asyncio
async def test_on_message_long_response_truncation(mock_message):
    mock_bot_user = MagicMock()
    mock_bot_user.id = 9999

    long_reply = "A" * 2000
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = long_reply

    with (
        patch.object(
            type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
        ),
        patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
    ):
        bot.CHANNEL_ID = 123456789
        await bot.on_message(mock_message)
        expected_reply = "A" * 1897 + "..."
        mock_message.reply.assert_called_once_with(expected_reply)


@pytest.mark.asyncio
async def test_on_message_exception_handling(mock_message):
    mock_bot_user = MagicMock()
    mock_bot_user.id = 9999

    with (
        patch.object(
            type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
        ),
        patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=Exception("API limit exceeded"),
        ),
    ):
        bot.CHANNEL_ID = 123456789
        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with("❌ Lỗi: API limit exceeded")
