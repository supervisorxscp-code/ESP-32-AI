from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    return user


@pytest.mark.asyncio
async def test_on_message_empty_prompt_when_mentioned(mock_bot_user):
    message = MagicMock()
    message.author.id = 987654321
    message.channel.id = 999
    message.content = "<@123456789>"
    message.reply = AsyncMock()

    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        await bot.on_message(message)

    message.reply.assert_called_once_with(
        "Bạn cần hỏi gì thế? Hãy nhập nội dung câu hỏi nhé! 😊"
    )


@pytest.mark.asyncio
async def test_on_message_success_with_typing_and_ai_response(mock_bot_user):
    message = MagicMock()
    message.author.id = 987654321
    message.channel.id = bot.CHANNEL_ID
    message.content = "Xin chào"
    message.reply = AsyncMock()

    typing_mock = AsyncMock()
    typing_mock.__aenter__ = AsyncMock(return_value=None)
    typing_mock.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing.return_value = typing_mock

    mock_choice = MagicMock()
    mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì?"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ), patch.object(
        bot.client.chat.completions,
        "create",
        AsyncMock(return_value=mock_response),
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        await bot.on_message(message)

    message.reply.assert_called_once_with("Chào bạn! Tôi có thể giúp gì?")


@pytest.mark.asyncio
async def test_on_message_truncation_long_response(mock_bot_user):
    message = MagicMock()
    message.author.id = 987654321
    message.channel.id = bot.CHANNEL_ID
    message.content = "Viết bài văn dài"
    message.reply = AsyncMock()

    typing_mock = AsyncMock()
    typing_mock.__aenter__ = AsyncMock(return_value=None)
    typing_mock.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing.return_value = typing_mock

    long_text = "A" * 2000
    mock_choice = MagicMock()
    mock_choice.message.content = long_text
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ), patch.object(
        bot.client.chat.completions,
        "create",
        AsyncMock(return_value=mock_response),
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        await bot.on_message(message)

    expected_text = "A" * 1897 + "..."
    message.reply.assert_called_once_with(expected_text)
