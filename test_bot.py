import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
import bot

pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_message():
    message = MagicMock()
    message.author = MagicMock()
    message.channel = MagicMock()
    message.channel.id = 12345
    message.channel.typing = MagicMock()

    typing_cm = AsyncMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing.return_value = typing_cm

    message.reply = AsyncMock()
    return message

async def test_on_message_ignore_own_message(mock_message):
    mock_user = MagicMock()
    mock_message.author = mock_user

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_user):
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()

async def test_on_message_ignore_wrong_channel_unmentioned(mock_message):
    bot_user = MagicMock()
    bot_user.id = 999
    bot_user.mentioned_in.return_value = False
    mock_message.channel.id = 99999
    mock_message.content = "Hello bot"

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=bot_user):
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()

async def test_on_message_empty_prompt_after_mention(mock_message):
    bot_user = MagicMock()
    bot_user.id = 999
    bot_user.mentioned_in.return_value = True
    mock_message.channel.id = 99999
    mock_message.content = "<@999>"

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=bot_user):
        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with("Bạn cần giúp gì? Hãy nhập câu hỏi của bạn nhé!")

async def test_on_message_successful_ai_response(mock_message):
    bot_user = MagicMock()
    bot_user.id = 999
    bot_user.mentioned_in.return_value = False
    mock_message.channel.id = bot.CHANNEL_ID
    mock_message.content = "Xin chào"

    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = "Chào bạn!"

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=bot_user), \
         patch.object(bot.client.chat.completions, 'create', new_callable=AsyncMock, return_value=mock_completion):
        await bot.on_message(mock_message)
        mock_message.channel.typing.assert_called_once()
        mock_message.reply.assert_called_once_with("Chào bạn!")

async def test_on_message_truncates_long_response(mock_message):
    bot_user = MagicMock()
    bot_user.id = 999
    bot_user.mentioned_in.return_value = False
    mock_message.channel.id = bot.CHANNEL_ID
    mock_message.content = "Kể một câu chuyện dài"

    long_text = "A" * 2000
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = long_text

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=bot_user), \
         patch.object(bot.client.chat.completions, 'create', new_callable=AsyncMock, return_value=mock_completion):
        await bot.on_message(mock_message)
        expected_text = "A" * 1897 + "..."
        mock_message.reply.assert_called_once_with(expected_text)

async def test_on_message_handles_exception(mock_message):
    bot_user = MagicMock()
    bot_user.id = 999
    bot_user.mentioned_in.return_value = False
    mock_message.channel.id = bot.CHANNEL_ID
    mock_message.content = "Error test"

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=bot_user), \
         patch.object(bot.client.chat.completions, 'create', side_effect=Exception("API failure")):
        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with("❌ Lỗi: API failure")
