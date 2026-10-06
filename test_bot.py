import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
import bot

@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    user.__str__.return_value = "TestBot#1234"
    return user

@pytest.mark.asyncio
async def test_on_message_empty_prompt_when_mentioned(mock_bot_user):
    message = AsyncMock()
    message.author = MagicMock()
    message.author.__eq__ = lambda self, other: False  # Not the bot user
    message.channel.id = 999999
    message.content = "<@123456789>"

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        # bot.user.mentioned_in(message) returns True if user is in message.mentions
        message.mentions = [mock_bot_user]

        await bot.on_message(message)

        message.reply.assert_called_once_with("❓ Bạn cần tôi giúp gì? Hãy nhập câu hỏi hoặc yêu cầu của bạn nhé!")

@pytest.mark.asyncio
async def test_on_message_truncates_long_response(mock_bot_user):
    message = AsyncMock()
    message.author = MagicMock()
    message.author.__eq__ = lambda self, other: False
    message.channel.id = 999999
    message.content = "<@123456789> Hello"
    message.mentions = [mock_bot_user]

    long_reply = "A" * 2000

    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content=long_reply))]

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user), \
         patch.object(bot.client.chat.completions, 'create', return_value=mock_completion):

        await bot.on_message(message)

        expected_reply = "A" * 1897 + "..."
        message.reply.assert_called_once_with(expected_reply)
        assert len(expected_reply) == 1900
