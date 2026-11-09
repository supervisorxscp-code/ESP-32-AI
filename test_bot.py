from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 12345
    return user


@pytest.fixture
def mock_typing():
    typing_cm = MagicMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    return typing_cm


@pytest.mark.asyncio
async def test_on_message_ignores_self(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = MagicMock()
        message.author = mock_bot_user
        await bot.on_message(message)
        message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_unrelated_channel(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 99999
        bot.CHANNEL_ID = 11111
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        await bot.on_message(message)
        message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 11111
        bot.CHANNEL_ID = 11111
        message.content = "<@12345>   "
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message.reply = AsyncMock()

        await bot.on_message(message)
        message.reply.assert_awaited_once_with(
            "Bạn cần trợ giúp gì? Hãy đặt câu hỏi nhé!"
        )


@pytest.mark.asyncio
async def test_on_message_success_with_typing(mock_bot_user, mock_typing):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 11111
        bot.CHANNEL_ID = 11111
        message.content = "<@!12345> Xin chào"
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message.channel.typing = MagicMock(return_value=mock_typing)
        message.reply = AsyncMock()

        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content="Chào bạn! Tôi có thể giúp gì cho bạn?"))
        ]

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ) as mock_create:
            await bot.on_message(message)

            mock_typing.__aenter__.assert_awaited_once()
            mock_typing.__aexit__.assert_awaited_once()
            mock_create.assert_awaited_once()
            # Check prompt was stripped of mention
            messages_arg = mock_create.call_args[1]["messages"]
            assert messages_arg[1]["content"] == "Xin chào"
            message.reply.assert_awaited_once_with(
                "Chào bạn! Tôi có thể giúp gì cho bạn?"
            )


@pytest.mark.asyncio
async def test_on_message_truncation(mock_bot_user, mock_typing):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 11111
        bot.CHANNEL_ID = 11111
        message.content = "Viết bài dài"
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.channel.typing = MagicMock(return_value=mock_typing)
        message.reply = AsyncMock()

        long_text = "a" * 2000
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content=long_text))]

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ):
            await bot.on_message(message)

            message.reply.assert_awaited_once()
            sent_reply = message.reply.call_args[0][0]
            assert len(sent_reply) == 1900
            assert sent_reply.endswith("...")


@pytest.mark.asyncio
async def test_on_message_handles_api_exception(mock_bot_user, mock_typing):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 11111
        bot.CHANNEL_ID = 11111
        message.content = "Gây lỗi"
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.channel.typing = MagicMock(return_value=mock_typing)
        message.reply = AsyncMock()

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=Exception("API timeout"),
        ):
            await bot.on_message(message)

            message.reply.assert_awaited_once_with("❌ Lỗi: API timeout")
