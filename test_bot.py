import os
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

# Ensure dummy env vars prior to importing bot
os.environ.setdefault("CHANNEL_ID", "123456789")
os.environ.setdefault("NVIDIA_API_KEY", "test_key")

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 9999
    return user


@pytest.fixture
def mock_message(mock_bot_user):
    message = AsyncMock()
    message.author = MagicMock()
    message.author.id = 1111
    message.channel = AsyncMock()
    message.channel.id = 123456789

    # Configure channel.typing() as async context manager
    typing_context = AsyncMock()
    typing_context.__aenter__.return_value = None
    typing_context.__aexit__.return_value = None
    message.channel.typing = MagicMock(return_value=typing_context)

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        mock_bot_user.mentioned_in = MagicMock(return_value=False)
        yield message


@pytest.mark.asyncio
async def test_on_message_ignores_bot_own_message(mock_message, mock_bot_user):
    mock_message.author = mock_bot_user
    await bot.on_message(mock_message)
    mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt(mock_message, mock_bot_user):
    mock_message.content = "<@9999>"
    mock_bot_user.mentioned_in = MagicMock(return_value=True)

    await bot.on_message(mock_message)

    mock_message.reply.assert_called_once_with("❓ Bạn hãy nhập câu hỏi sau khi nhắc tới tôi nhé!")


@pytest.mark.asyncio
async def test_on_message_successful_ai_completion(mock_message):
    mock_message.content = "Xin chào"

    mock_choice = MagicMock()
    mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì cho bạn?"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_response
        await bot.on_message(mock_message)

        mock_message.channel.typing.assert_called_once()
        mock_create.assert_called_once()
        mock_message.reply.assert_called_once_with("Chào bạn! Tôi có thể giúp gì cho bạn?")


@pytest.mark.asyncio
async def test_on_message_truncates_long_response(mock_message):
    mock_message.content = "Viết câu chuyện dài"

    long_content = "A" * 2000
    mock_choice = MagicMock()
    mock_choice.message.content = long_content
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_response
        await bot.on_message(mock_message)

        assert mock_message.reply.call_count == 1
        replied_text = mock_message.reply.call_args[0][0]
        assert len(replied_text) == 1900
        assert replied_text.endswith("...")


@pytest.mark.asyncio
async def test_on_message_error_handling(mock_message):
    mock_message.content = "Lỗi kết nối"

    with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = Exception("API rate limit exceeded")
        await bot.on_message(mock_message)

        mock_message.reply.assert_called_once_with("❌ Lỗi: API rate limit exceeded")
