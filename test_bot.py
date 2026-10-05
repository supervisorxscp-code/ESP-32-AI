import os
import pytest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

os.environ["CHANNEL_ID"] = "123456789"
os.environ["DISCORD_TOKEN"] = "dummy_token"
os.environ["OPENAI_API_KEY"] = "dummy_api_key"

import bot

@pytest.mark.asyncio
async def test_on_message_empty_prompt_after_mention():
    mock_message = MagicMock()
    mock_message.channel = MagicMock()
    mock_message.channel.id = 123456789
    mock_message.content = "<@99999>"
    mock_message.reply = AsyncMock()

    mock_bot_user = MagicMock()
    mock_bot_user.id = 99999

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in = MagicMock(return_value=True)
        mock_message.author = "another_user"
        await bot.on_message(mock_message)

    mock_message.reply.assert_called_once_with("💡 Bạn cần nhập câu hỏi hoặc yêu cầu!")

@pytest.mark.asyncio
async def test_on_message_ignores_bot_own_message():
    mock_message = MagicMock()
    mock_bot_user = MagicMock()
    mock_message.author = mock_bot_user
    mock_message.reply = AsyncMock()

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)

    mock_message.reply.assert_not_called()
