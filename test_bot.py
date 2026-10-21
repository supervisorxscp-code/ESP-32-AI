from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    user.__str__ = lambda self: "TestBot#0001"
    return user


@pytest.mark.asyncio
async def test_on_message_empty_mention(mock_bot_user):
    message = MagicMock()
    message.author = MagicMock()
    message.author.id = 987654321
    message.channel.id = 1111

    # Mention bot with no prompt text
    message.content = "<@123456789>"
    message.reply = AsyncMock()

    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        await bot.on_message(message)

    message.reply.assert_called_once_with(
        "Xin chào! Bạn cần mình giúp gì? Hãy nhập câu hỏi của bạn nhé."
    )


@pytest.mark.asyncio
async def test_on_message_typing_and_success(mock_bot_user):
    message = MagicMock()
    message.author = MagicMock()
    message.author.id = 987654321
    message.channel.id = bot.CHANNEL_ID if bot.CHANNEL_ID != 0 else 1111

    message.content = "<@123456789> Xin chào bot"
    message.reply = AsyncMock()

    typing_mock = AsyncMock()
    typing_mock.__aenter__ = AsyncMock(return_value=None)
    typing_mock.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_mock)

    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content="Chào bạn, mình có thể giúp gì?"))
    ]

    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ), patch.object(
        bot.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        return_value=mock_completion,
    ) as mock_create:
        await bot.on_message(message)

        mock_create.assert_called_once()
        message.channel.typing.assert_called_once()
        message.reply.assert_called_once_with("Chào bạn, mình có thể giúp gì?")


@pytest.mark.asyncio
async def test_on_message_truncation(mock_bot_user):
    message = MagicMock()
    message.author = MagicMock()
    message.author.id = 987654321
    message.channel.id = bot.CHANNEL_ID

    message.content = "Viết bài văn thật dài"
    message.reply = AsyncMock()

    typing_mock = AsyncMock()
    typing_mock.__aenter__ = AsyncMock(return_value=None)
    typing_mock.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_mock)

    long_response = "A" * 2000
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content=long_response))
    ]

    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ), patch.object(
        bot.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        return_value=mock_completion,
    ):
        await bot.on_message(message)

        message.reply.assert_called_once()
        args, _ = message.reply.call_args
        reply_text = args[0]
        assert len(reply_text) == 1900
        assert reply_text.endswith("...")
