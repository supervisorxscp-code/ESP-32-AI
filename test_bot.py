from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_ignores_bot_self():
    message = AsyncMock()
    mock_bot_user = MagicMock()
    message.author = mock_bot_user

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(message)

    message.reply.assert_not_called()

@pytest.mark.asyncio
async def test_on_message_empty_prompt_after_mention():
    message = AsyncMock()
    author_user = MagicMock()
    message.author = author_user

    bot_user = MagicMock()
    bot_user.id = 123456789
    bot_user.mentioned_in = MagicMock(return_value=True)

    message.content = "<@123456789>"
    message.channel.id = 9999  # different channel but mentioned

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=bot_user):
        await bot.on_message(message)

    message.reply.assert_called_once_with("Bạn cần mình giúp gì nào? 😊")

@pytest.mark.asyncio
async def test_on_message_success_with_typing_and_truncation():
    message = AsyncMock()
    author_user = MagicMock()
    message.author = author_user

    bot_user = MagicMock()
    bot_user.id = 123456789
    bot_user.mentioned_in = MagicMock(return_value=True)

    message.content = "<@123456789> Chào bạn"
    message.channel.id = bot.CHANNEL_ID

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_ctx)

    long_response = "A" * 2000
    mock_choice = MagicMock()
    mock_choice.message.content = long_response
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=bot_user), \
         patch.object(bot.client.chat.completions, 'create', new_callable=AsyncMock, return_value=mock_completion):
        await bot.on_message(message)

    message.channel.typing.assert_called_once()
    assert message.reply.call_count == 1
    reply_arg = message.reply.call_args[0][0]
    assert len(reply_arg) == 1900
    assert reply_arg.endswith("...")

@pytest.mark.asyncio
async def test_on_message_error_handling():
    message = AsyncMock()
    author_user = MagicMock()
    message.author = author_user

    bot_user = MagicMock()
    bot_user.id = 123456789
    bot_user.mentioned_in = MagicMock(return_value=True)

    message.content = "<@123456789> Hello"
    message.channel.id = bot.CHANNEL_ID

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_ctx)

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=bot_user), \
         patch.object(bot.client.chat.completions, 'create', new_callable=AsyncMock, side_effect=Exception("API connection error")):
        await bot.on_message(message)

    message.reply.assert_called_once_with("❌ Lỗi: API connection error")
