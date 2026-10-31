from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 12345
    return user


@pytest.mark.asyncio
async def test_on_message_ignores_self(mock_bot_user):
    message = MagicMock()
    message.author = mock_bot_user
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(message)
    message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_unrelated_channel_without_mention(mock_bot_user):
    message = MagicMock()
    message.author.id = 99999
    message.channel.id = 88888
    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(bot.bot.user, "mentioned_in", return_value=False),
    ):
        await bot.on_message(message)
    message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_after_mention(mock_bot_user):
    message = MagicMock()
    message.author.id = 99999
    message.channel.id = bot.CHANNEL_ID
    message.content = "<@12345>"
    message.reply = AsyncMock()

    typing_mock = AsyncMock()
    typing_mock.__aenter__.return_value = None
    typing_mock.__aexit__.return_value = None
    message.channel.typing = MagicMock(return_value=typing_mock)

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        await bot.on_message(message)

    message.reply.assert_called_once_with("Bạn cần trợ giúp gì? Hãy đặt câu hỏi cho tôi nhé! 😊")
    message.channel.typing.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_successful_ai_response_with_typing(mock_bot_user):
    message = MagicMock()
    message.author.id = 99999
    message.channel.id = bot.CHANNEL_ID
    message.content = "<@!12345> Xin chào"
    message.reply = AsyncMock()

    typing_mock = AsyncMock()
    typing_mock.__aenter__.return_value = None
    typing_mock.__aexit__.return_value = None
    message.channel.typing = MagicMock(return_value=typing_mock)

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì cho bạn?"
    mock_response.choices = [mock_choice]

    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response),
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        await bot.on_message(message)

    message.channel.typing.assert_called_once()
    typing_mock.__aenter__.assert_called_once()
    typing_mock.__aexit__.assert_called_once()
    message.reply.assert_called_once_with("Chào bạn! Tôi có thể giúp gì cho bạn?")


@pytest.mark.asyncio
async def test_on_message_truncates_long_response(mock_bot_user):
    message = MagicMock()
    message.author.id = 99999
    message.channel.id = bot.CHANNEL_ID
    message.content = "Kể một câu chuyện rất dài"
    message.reply = AsyncMock()

    typing_mock = AsyncMock()
    typing_mock.__aenter__.return_value = None
    typing_mock.__aexit__.return_value = None
    message.channel.typing = MagicMock(return_value=typing_mock)

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "A" * 2000
    mock_response.choices = [mock_choice]

    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response),
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        await bot.on_message(message)

    assert message.reply.call_count == 1
    reply_arg = message.reply.call_args[0][0]
    assert len(reply_arg) == 1900
    assert reply_arg.endswith("...")


@pytest.mark.asyncio
async def test_on_message_handles_api_exception(mock_bot_user):
    message = MagicMock()
    message.author.id = 99999
    message.channel.id = bot.CHANNEL_ID
    message.content = "Xin chào"
    message.reply = AsyncMock()

    typing_mock = AsyncMock()
    typing_mock.__aenter__.return_value = None
    typing_mock.__aexit__.return_value = None
    message.channel.typing = MagicMock(return_value=typing_mock)

    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=RuntimeError("API Connection timeout"),
        ),
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        await bot.on_message(message)

    message.reply.assert_called_once_with("❌ Lỗi: API Connection timeout")
