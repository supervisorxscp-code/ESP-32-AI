from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_message():
    message = AsyncMock()
    message.author = MagicMock()
    message.channel = MagicMock()
    message.channel.id = 12345

    # Mock async context manager for typing()
    typing_cm = AsyncMock()
    typing_cm.__aenter__.return_value = None
    typing_cm.__aexit__.return_value = None
    message.channel.typing = MagicMock(return_value=typing_cm)

    message.content = "Xin chào"
    message.reply = AsyncMock()
    return message


@pytest.mark.asyncio
async def test_on_message_empty_prompt_when_mentioned(mock_message):
    mock_bot_user = MagicMock()
    mock_bot_user.id = 9999
    mock_message.content = "<@9999>"

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_message.channel.id = 0  # not matching default CHANNEL_ID, but mentioned
        bot.bot.user.mentioned_in = MagicMock(return_value=True)

        await bot.on_message(mock_message)

        mock_message.reply.assert_called_once_with(
            "⚠️ Bạn chưa nhập câu hỏi. Hãy nhắn câu hỏi sau câu nhắc bot nhé!"
        )


@pytest.mark.asyncio
async def test_on_message_truncation_long_reply(mock_message):
    mock_bot_user = MagicMock()
    mock_bot_user.id = 9999
    mock_message.content = "Hãy viết một đoạn văn rất dài"

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        mock_message.channel.id = int(bot.CHANNEL_ID)

        long_response = "A" * 2000
        mock_choice = MagicMock()
        mock_choice.message.content = long_response
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_completion
            await bot.on_message(mock_message)

            expected_reply = "A" * 1897 + "..."
            mock_message.reply.assert_called_once_with(expected_reply)
