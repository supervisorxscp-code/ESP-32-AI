import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import bot

@pytest.mark.asyncio
async def test_on_message_empty_mention():
    mock_message = AsyncMock()
    mock_message.author = MagicMock()
    mock_message.channel.id = bot.CHANNEL_ID
    mock_message.content = "<@12345>"

    mock_user = MagicMock()
    mock_user.id = 12345
    mock_user.mentioned_in.return_value = True

    with patch.object(bot.bot, "_connection") as mock_conn:
        mock_conn.user = mock_user
        mock_message.author.__eq__.return_value = False

        await bot.on_message(mock_message)

    mock_message.reply.assert_called_once_with("Bạn cần mình giúp gì thế? 😊")
