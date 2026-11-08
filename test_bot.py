from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    user.name = "TestBot"
    return user


@pytest.fixture
def mock_typing():
    typing_cm = MagicMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    return typing_cm


@pytest.mark.asyncio
async def test_on_message_ignores_self(mock_bot_user):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = mock_bot_user
        await bot.on_message(message)
        message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_after_mention(mock_bot_user):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 999
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message.content = f"<@{mock_bot_user.id}>   "
        message.reply = AsyncMock()

        await bot.on_message(message)

        message.reply.assert_called_once_with("Bạn cần hỏi gì nào?")


@pytest.mark.asyncio
async def test_on_message_successful_ai_response_with_typing(mock_bot_user, mock_typing):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = bot.CHANNEL_ID
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.content = "Xin chào!"
        message.reply = AsyncMock()
        message.channel.typing = MagicMock(return_value=mock_typing)

        mock_choice = MagicMock()
        mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì cho bạn?"
        mock_response = MagicMock(choices=[mock_choice])

        with patch.object(bot.client.chat.completions, "create", new=AsyncMock(return_value=mock_response)) as mock_create:
            await bot.on_message(message)

            message.channel.typing.assert_called_once()
            mock_typing.__aenter__.assert_called_once()
            mock_typing.__aexit__.assert_called_once()
            mock_create.assert_called_once()
            message.reply.assert_called_once_with("Chào bạn! Tôi có thể giúp gì cho bạn?")


@pytest.mark.asyncio
async def test_on_message_truncates_long_response(mock_bot_user, mock_typing):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = bot.CHANNEL_ID
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.content = "Kể chuyện thật dài"
        message.reply = AsyncMock()
        message.channel.typing = MagicMock(return_value=mock_typing)

        long_text = "A" * 2000
        mock_choice = MagicMock()
        mock_choice.message.content = long_text
        mock_response = MagicMock(choices=[mock_choice])

        with patch.object(bot.client.chat.completions, "create", new=AsyncMock(return_value=mock_response)):
            await bot.on_message(message)

            expected_reply = ("A" * 1897) + "..."
            message.reply.assert_called_once_with(expected_reply)


@pytest.mark.asyncio
async def test_on_message_handles_api_exception(mock_bot_user, mock_typing):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = bot.CHANNEL_ID
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.content = "Gây lỗi thử"
        message.reply = AsyncMock()
        message.channel.typing = MagicMock(return_value=mock_typing)

        with patch.object(bot.client.chat.completions, "create", new=AsyncMock(side_effect=RuntimeError("Rate limit"))):
            await bot.on_message(message)

            message.reply.assert_called_once_with("❌ Lỗi: Rate limit")
