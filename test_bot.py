from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_message():
    message = AsyncMock()
    message.author = MagicMock()
    message.author.id = 12345
    message.channel = AsyncMock()

    typing_cm = AsyncMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_cm)

    message.content = "Xin chào"
    message.channel.id = 100
    return message


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 9999
    user.__str__ = MagicMock(return_value="TestBot#0000")
    return user


@pytest.mark.asyncio
async def test_on_message_ignores_self(mock_message, mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        mock_message.author = mock_bot_user
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_other_channel(mock_message, mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        mock_message.channel.id = 999
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_input_after_mention(mock_message, mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        mock_message.channel.id = 999
        mock_message.content = "<@9999>"

        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with(
            "Bạn cần trợ giúp gì? Hãy đặt câu hỏi cho tôi nhé!"
        )


@pytest.mark.asyncio
async def test_on_message_success(mock_message, mock_bot_user):
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì cho bạn?"
    mock_completion.choices = [mock_choice]

    with (
        patch.object(
            type(bot.bot),
            "user",
            new_callable=PropertyMock,
            return_value=mock_bot_user,
        ),
        patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ) as mock_create,
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        mock_message.channel.id = bot.CHANNEL_ID

        await bot.on_message(mock_message)

        mock_message.channel.typing.assert_called_once()
        mock_create.assert_called_once()
        mock_message.reply.assert_called_once_with(
            "Chào bạn! Tôi có thể giúp gì cho bạn?"
        )


@pytest.mark.asyncio
async def test_on_message_truncation(mock_message, mock_bot_user):
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "A" * 2000
    mock_completion.choices = [mock_choice]

    with (
        patch.object(
            type(bot.bot),
            "user",
            new_callable=PropertyMock,
            return_value=mock_bot_user,
        ),
        patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ),
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        mock_message.channel.id = bot.CHANNEL_ID

        await bot.on_message(mock_message)

        reply_args = mock_message.reply.call_args[0][0]
        assert len(reply_args) == 1900
        assert reply_args.endswith("...")


@pytest.mark.asyncio
async def test_on_message_error_handling(mock_message, mock_bot_user):
    with (
        patch.object(
            type(bot.bot),
            "user",
            new_callable=PropertyMock,
            return_value=mock_bot_user,
        ),
        patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=Exception("API error"),
        ),
    ):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        mock_message.channel.id = bot.CHANNEL_ID

        await bot.on_message(mock_message)

        mock_message.reply.assert_called_once_with("❌ Lỗi: API error")
