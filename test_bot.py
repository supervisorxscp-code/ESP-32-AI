from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    user.__str__.return_value = "TestBot#0001"
    return user


@pytest.fixture
def mock_typing_cm():
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=None)
    cm.__aexit__ = AsyncMock(return_value=None)
    return cm


@pytest.mark.asyncio
async def test_on_message_ignores_self(mock_bot_user):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = mock_bot_user
        await bot.on_message(message)
        message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_other_channel_without_mention(mock_bot_user):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 999999
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        with patch.object(bot, "CHANNEL_ID", 111111):
            await bot.on_message(message)
            message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_guidance(mock_bot_user):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 111111
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message.content = f"<@{mock_bot_user.id}>"
        message.reply = AsyncMock()
        with patch.object(bot, "CHANNEL_ID", 111111):
            await bot.on_message(message)
            message.reply.assert_awaited_once_with(
                "Xin chào! Bạn cần mình giúp gì không? Hãy đặt câu hỏi cho mình nhé!"
            )


@pytest.mark.asyncio
async def test_on_message_success_with_typing(mock_bot_user, mock_typing_cm):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 111111
        message.channel.typing = MagicMock(return_value=mock_typing_cm)
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message.content = f"<@{mock_bot_user.id}> Thời tiết hôm nay thế nào?"
        message.reply = AsyncMock()

        mock_choice = MagicMock()
        mock_choice.message.content = "Hôm nay trời nắng đẹp."
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        with patch.object(bot, "CHANNEL_ID", 111111), \
             patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response) as mock_create:
            await bot.on_message(message)

            mock_typing_cm.__aenter__.assert_awaited_once()
            mock_typing_cm.__aexit__.assert_awaited_once()
            mock_create.assert_awaited_once()
            message.reply.assert_awaited_once_with("Hôm nay trời nắng đẹp.")


@pytest.mark.asyncio
async def test_on_message_error_handling(mock_bot_user, mock_typing_cm):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        message = MagicMock()
        message.author = MagicMock()
        message.channel.id = 111111
        message.channel.typing = MagicMock(return_value=mock_typing_cm)
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.content = "Thử nghiệm lỗi"
        message.reply = AsyncMock()

        with patch.object(bot, "CHANNEL_ID", 111111), \
             patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, side_effect=Exception("API connection timeout")):
            await bot.on_message(message)

            message.reply.assert_awaited_once_with("❌ Lỗi: API connection timeout")
