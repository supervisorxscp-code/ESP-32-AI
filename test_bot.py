from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    return user


@pytest.fixture
def mock_typing_ctx():
    ctx = MagicMock()
    ctx.__aenter__ = AsyncMock(return_value=None)
    ctx.__aexit__ = AsyncMock(return_value=None)
    return ctx


@pytest.mark.asyncio
async def test_on_message_ignores_bot_own_message(mock_bot_user):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        msg = MagicMock()
        msg.author = mock_bot_user
        msg.channel.id = bot.CHANNEL_ID

        await bot.on_message(msg)
        msg.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_other_channel_without_mention(mock_bot_user):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        bot.CHANNEL_ID = 1111
        msg = MagicMock()
        msg.author.id = 9999
        msg.channel.id = 2222
        bot.bot.user.mentioned_in = MagicMock(return_value=False)

        await bot.on_message(msg)
        msg.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_replies_help(mock_bot_user):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        bot.CHANNEL_ID = 1111
        msg = MagicMock()
        msg.author.id = 9999
        msg.channel.id = 1111
        msg.content = f"<@{mock_bot_user.id}>"
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        msg.reply = AsyncMock()

        await bot.on_message(msg)
        msg.reply.assert_awaited_once_with("Bạn cần trợ giúp gì? Hãy đặt câu hỏi nhé!")


@pytest.mark.asyncio
async def test_on_message_success_with_typing(mock_bot_user, mock_typing_ctx):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        bot.CHANNEL_ID = 1111
        msg = MagicMock()
        msg.author.id = 9999
        msg.channel.id = 1111
        msg.content = f"<@{mock_bot_user.id}> Xin chào"
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        msg.channel.typing = MagicMock(return_value=mock_typing_ctx)
        msg.reply = AsyncMock()

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì cho bạn?"
        mock_response.choices = [mock_choice]

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response) as mock_create:
            await bot.on_message(msg)

            msg.channel.typing.assert_called_once()
            mock_typing_ctx.__aenter__.assert_awaited_once()
            mock_typing_ctx.__aexit__.assert_awaited_once()
            mock_create.assert_awaited_once_with(
                model="meta/llama-3.3-70b-instruct",
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý thông minh, trả lời ngắn gọn bằng tiếng Việt."},
                    {"role": "user", "content": "Xin chào"},
                ],
                temperature=0.7,
                max_tokens=800,
            )
            msg.reply.assert_awaited_once_with("Chào bạn! Tôi có thể giúp gì cho bạn?")


@pytest.mark.asyncio
async def test_on_message_error_handling(mock_bot_user, mock_typing_ctx):
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        bot.CHANNEL_ID = 1111
        msg = MagicMock()
        msg.author.id = 9999
        msg.channel.id = 1111
        msg.content = "Câu hỏi lỗi"
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        msg.channel.typing = MagicMock(return_value=mock_typing_ctx)
        msg.reply = AsyncMock()

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock, side_effect=RuntimeError("API error")):
            await bot.on_message(msg)

            msg.reply.assert_awaited_once_with("❌ Lỗi: API error")
