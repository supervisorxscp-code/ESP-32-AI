from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    return user


def create_mock_message(content, author_is_bot=False, channel_id=0, mentioned_in_bot=True):
    message = MagicMock()
    message.content = content
    message.channel.id = channel_id

    # Mock message.channel.typing() as an async context manager
    typing_cm = MagicMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    message.channel.typing = MagicMock(return_value=typing_cm)

    message.reply = AsyncMock()
    return message


@pytest.mark.asyncio
async def test_on_message_ignores_bot_itself(mock_bot_user):
    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        message = create_mock_message("hello", channel_id=123)
        message.author = mock_bot_user

        await bot.on_message(message)
        message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_input_prompt(mock_bot_user):
    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message = create_mock_message(f"<@{mock_bot_user.id}>   ")
        message.author = MagicMock()

        await bot.on_message(message)
        message.reply.assert_called_once_with("Bạn hãy nhập câu hỏi nhé!")
        message.channel.typing.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_nickname_mention_empty_input(mock_bot_user):
    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message = create_mock_message(f"<@!{mock_bot_user.id}>")
        message.author = MagicMock()

        await bot.on_message(message)
        message.reply.assert_called_once_with("Bạn hãy nhập câu hỏi nhé!")


@pytest.mark.asyncio
async def test_on_message_success_with_typing_and_truncation(mock_bot_user):
    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message = create_mock_message(f"<@{mock_bot_user.id}> Xin chào")
        message.author = MagicMock()

        long_reply = "A" * 2000
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = long_reply

        with patch.object(bot.client.chat.completions, 'create', new_callable=AsyncMock, return_value=mock_response):
            await bot.on_message(message)

        message.channel.typing.assert_called_once()
        message.reply.assert_called_once()
        reply_arg = message.reply.call_args[0][0]
        assert len(reply_arg) == 1900
        assert reply_arg.endswith("...")
        assert reply_arg == "A" * 1897 + "..."


@pytest.mark.asyncio
async def test_on_message_api_error_handling(mock_bot_user):
    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message = create_mock_message(f"<@{mock_bot_user.id}> Lỗi đi")
        message.author = MagicMock()

        with patch.object(bot.client.chat.completions, 'create', new_callable=AsyncMock, side_effect=RuntimeError("API Connection Failed")):
            await bot.on_message(message)

        message.channel.typing.assert_called_once()
        message.reply.assert_called_once_with("❌ Lỗi: API Connection Failed")
