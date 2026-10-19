from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    return user


@pytest.fixture
def mock_message(mock_bot_user):
    message = AsyncMock()
    message.author = MagicMock()
    message.author.id = 987654321

    message.channel = MagicMock()
    message.channel.id = 100

    typing_cm = MagicMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing.return_value = typing_cm

    return message


@pytest.mark.asyncio
async def test_on_message_ignores_bot_own_message(mock_message, mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        mock_message.author = mock_bot_user
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_wrong_channel_unmentioned(
    mock_message, mock_bot_user
):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        mock_message.channel.id = 999
        bot.bot.user.mentioned_in.return_value = False
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_after_mention(mock_message, mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        mock_message.channel.id = 0
        bot.bot.user.mentioned_in.return_value = True
        mock_message.content = f"<@{mock_bot_user.id}>"

        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with(
            "Bạn cần tôi giúp gì? Hãy nhập câu hỏi nhé! 🤖"
        )


@pytest.mark.asyncio
async def test_on_message_success_response(mock_message, mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        mock_message.channel.id = 0
        bot.bot.user.mentioned_in.return_value = False
        mock_message.content = "Xin chào"

        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content="Chào bạn! Tôi có thể giúp gì?"))
        ]

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ):
            await bot.on_message(mock_message)

            mock_message.channel.typing.assert_called_once()
            mock_message.reply.assert_called_once_with("Chào bạn! Tôi có thể giúp gì?")


@pytest.mark.asyncio
async def test_on_message_truncates_long_response(mock_message, mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        mock_message.channel.id = 0
        bot.bot.user.mentioned_in.return_value = False
        mock_message.content = "Viết bài văn dài"

        long_text = "A" * 2000
        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content=long_text))
        ]

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ):
            await bot.on_message(mock_message)

            expected_text = "A" * 1897 + "..."
            mock_message.reply.assert_called_once_with(expected_text)


@pytest.mark.asyncio
async def test_on_message_handles_exception(mock_message, mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        mock_message.channel.id = 0
        bot.bot.user.mentioned_in.return_value = False
        mock_message.content = "Lỗi API"

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=Exception("API Connection Failed"),
        ):
            await bot.on_message(mock_message)

            mock_message.reply.assert_called_once_with("❌ Lỗi: API Connection Failed")
