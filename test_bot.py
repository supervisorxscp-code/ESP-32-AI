from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import discord
import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_ignores_bot_self():
    mock_message = MagicMock(spec=discord.Message)
    mock_bot_user = MagicMock(spec=discord.ClientUser)

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_message.author = mock_bot_user
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_unrelated_channel_unmentioned():
    mock_message = MagicMock(spec=discord.Message)
    mock_bot_user = MagicMock(spec=discord.ClientUser)

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        mock_message.author = MagicMock()
        mock_message.channel.id = 99999
        bot.bot.user.mentioned_in.return_value = False

        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_after_mention():
    mock_message = MagicMock(spec=discord.Message)
    mock_bot_user = MagicMock(spec=discord.ClientUser)
    mock_bot_user.id = 12345

    mock_message.author = MagicMock()
    mock_message.channel.id = 99999
    mock_message.content = "<@12345> "
    mock_message.reply = AsyncMock()

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)

        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with("Bạn hãy nhập câu hỏi nhé!")


@pytest.mark.asyncio
async def test_on_message_success():
    mock_message = MagicMock(spec=discord.Message)
    mock_bot_user = MagicMock(spec=discord.ClientUser)
    mock_bot_user.id = 12345

    mock_message.author = MagicMock()
    mock_message.channel.id = bot.CHANNEL_ID
    mock_message.content = "Xin chào"
    mock_message.reply = AsyncMock()

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing = MagicMock(return_value=typing_ctx)

    mock_chat_completion = AsyncMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì?"
    mock_response.choices = [mock_choice]
    mock_chat_completion.create = AsyncMock(return_value=mock_response)

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user), \
         patch.object(bot.client.chat, "completions", mock_chat_completion):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)

        await bot.on_message(mock_message)

        mock_message.channel.typing.assert_called_once()
        mock_message.reply.assert_called_once_with("Chào bạn! Tôi có thể giúp gì?")


@pytest.mark.asyncio
async def test_on_message_truncation():
    mock_message = MagicMock(spec=discord.Message)
    mock_bot_user = MagicMock(spec=discord.ClientUser)

    mock_message.author = MagicMock()
    mock_message.channel.id = bot.CHANNEL_ID
    mock_message.content = "Trả lời dài"
    mock_message.reply = AsyncMock()

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing = MagicMock(return_value=typing_ctx)

    long_text = "a" * 2000
    mock_chat_completion = AsyncMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = long_text
    mock_response.choices = [mock_choice]
    mock_chat_completion.create = AsyncMock(return_value=mock_response)

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user), \
         patch.object(bot.client.chat, "completions", mock_chat_completion):
        bot.bot.user.mentioned_in = MagicMock(return_value=False)

        await bot.on_message(mock_message)

        expected_reply = "a" * 1897 + "..."
        mock_message.reply.assert_called_once_with(expected_reply)
