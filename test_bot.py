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
    message.author.__eq__ = lambda self, other: self is other
    message.channel = AsyncMock()

    typing_cm = AsyncMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_cm)

    message.channel.id = bot.CHANNEL_ID
    message.content = "Xin chào"
    return message


@pytest.mark.asyncio
async def test_on_ready():
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value="TestBot#1234"):
        await bot.on_ready()


@pytest.mark.asyncio
async def test_on_message_ignores_self_message(mock_message, mock_bot_user):
    mock_message.author = mock_bot_user
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_unmentioned_wrong_channel(mock_message, mock_bot_user):
    mock_message.channel.id = 999999
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in = MagicMock(return_value=False)
        bot.bot.user.mentioned_in = mock_bot_user.mentioned_in
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_guidance(mock_message, mock_bot_user):
    mock_message.content = f"<@{mock_bot_user.id}>"
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in = MagicMock(return_value=True)
        bot.bot.user.mentioned_in = mock_bot_user.mentioned_in
        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with("Bạn cần mình giúp gì nào? 😊")


@pytest.mark.asyncio
async def test_on_message_successful_ai_reply(mock_message, mock_bot_user):
    mock_message.content = "Hôm nay thời tiết thế nào?"
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in = MagicMock(return_value=False)
        bot.bot.user.mentioned_in = mock_bot_user.mentioned_in

        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Thời tiết hôm nay rất đẹp!"))]

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response):
            await bot.on_message(mock_message)
            mock_message.channel.typing.assert_called_once()
            mock_message.reply.assert_called_once_with("Thời tiết hôm nay rất đẹp!")


@pytest.mark.asyncio
async def test_on_message_truncates_long_response(mock_message, mock_bot_user):
    mock_message.content = "Viết bài văn dài"
    long_content = "A" * 2000
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in = MagicMock(return_value=False)
        bot.bot.user.mentioned_in = mock_bot_user.mentioned_in

        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=long_content))]

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response):
            await bot.on_message(mock_message)
            expected_reply = "A" * 1897 + "..."
            mock_message.reply.assert_called_once_with(expected_reply)


@pytest.mark.asyncio
async def test_on_message_handles_exception(mock_message, mock_bot_user):
    mock_message.content = "Lỗi API"
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in = MagicMock(return_value=False)
        bot.bot.user.mentioned_in = mock_bot_user.mentioned_in

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, side_effect=Exception("API Error")):
            await bot.on_message(mock_message)
            mock_message.reply.assert_called_once_with("❌ Lỗi: API Error")
