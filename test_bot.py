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
    message.channel = AsyncMock()
    message.channel.id = bot.CHANNEL_ID
    message.content = "Xin chào"

    # Async context manager mock for typing()
    typing_context = MagicMock()
    typing_context.__aenter__ = AsyncMock(return_value=None)
    typing_context.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_context)

    return message


@pytest.mark.asyncio
async def test_on_message_ignores_self_message(mock_message, mock_bot_user):
    mock_message.author = mock_bot_user
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_wrong_channel_no_mention(mock_message):
    mock_message.channel.id = 999999
    mock_message.content = "Hello"
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=MagicMock(id=123)):
        type(mock_message.channel).id = PropertyMock(return_value=999999)
        mock_bot_user = bot.bot.user
        mock_bot_user.mentioned_in.return_value = False
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_when_mentioned(mock_message, mock_bot_user):
    mock_message.content = f"<@{mock_bot_user.id}>"
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in.return_value = True
        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with("Bạn cần tôi giúp gì? Hãy đặt câu hỏi cho tôi nhé!")


@pytest.mark.asyncio
async def test_on_message_valid_prompt(mock_message, mock_bot_user):
    mock_message.content = "Thời tiết hôm nay thế nào?"
    mock_choice = MagicMock()
    mock_choice.message.content = "Thời tiết hôm nay rất đẹp!"

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in.return_value = False
        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response
            await bot.on_message(mock_message)

            mock_message.channel.typing.assert_called_once()
            mock_create.assert_called_once()
            mock_message.reply.assert_called_once_with("Thời tiết hôm nay rất đẹp!")


@pytest.mark.asyncio
async def test_on_message_long_response_truncated(mock_message, mock_bot_user):
    mock_message.content = "Viết bài văn dài"
    long_text = "A" * 2000

    mock_choice = MagicMock()
    mock_choice.message.content = long_text

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in.return_value = False
        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response
            await bot.on_message(mock_message)

            expected_reply = "A" * 1897 + "..."
            mock_message.reply.assert_called_once_with(expected_reply)


@pytest.mark.asyncio
async def test_on_message_exception_handling(mock_message, mock_bot_user):
    mock_message.content = "Lỗi xảy ra"
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in.return_value = False
        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.side_effect = Exception("API connection error")
            await bot.on_message(mock_message)

            mock_message.reply.assert_called_once_with("❌ Lỗi: API connection error")
