from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    user.__str__.return_value = "TestBot#0001"
    return user


@pytest.fixture
def mock_message(mock_bot_user):
    msg = MagicMock()
    msg.author = MagicMock()
    msg.author.id = 987654321
    msg.channel = MagicMock()
    msg.channel.id = bot.CHANNEL_ID
    msg.content = "Xin chào"
    msg.reply = AsyncMock()

    typing_cm = MagicMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    msg.channel.typing = MagicMock(return_value=typing_cm)

    return msg


@pytest.mark.asyncio
async def test_on_message_ignores_bot_itself(mock_bot_user, mock_message):
    mock_message.author = mock_bot_user
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)
    mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_other_channel_without_mention(mock_bot_user, mock_message):
    mock_message.channel.id = 999999
    mock_bot_user.mentioned_in.return_value = False
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)
    mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_after_mention(mock_bot_user, mock_message):
    mock_message.content = f"<@{mock_bot_user.id}>"
    mock_bot_user.mentioned_in.return_value = True
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)
    mock_message.reply.assert_called_once_with("Bạn cần trợ giúp gì? Hãy đặt câu hỏi nhé!")


@pytest.mark.asyncio
async def test_on_message_empty_prompt_after_nickname_mention(mock_bot_user, mock_message):
    mock_message.content = f"<@!{mock_bot_user.id}>"
    mock_bot_user.mentioned_in.return_value = True
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        await bot.on_message(mock_message)
    mock_message.reply.assert_called_once_with("Bạn cần trợ giúp gì? Hãy đặt câu hỏi nhé!")


@pytest.mark.asyncio
async def test_on_message_success_with_typing_and_truncation(mock_bot_user, mock_message):
    mock_message.content = "Giúp tôi với"
    mock_bot_user.mentioned_in.return_value = False

    fake_reply = "A" * 2000
    mock_choice = MagicMock()
    mock_choice.message.content = fake_reply
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create,
    ):
        mock_create.return_value = mock_response
        await bot.on_message(mock_message)

    mock_message.channel.typing.assert_called_once()
    mock_message.reply.assert_called_once()
    reply_arg = mock_message.reply.call_args[0][0]
    assert len(reply_arg) == 1900
    assert reply_arg.endswith("...")


@pytest.mark.asyncio
async def test_on_message_handles_exception(mock_bot_user, mock_message):
    mock_message.content = "Gây lỗi"
    mock_bot_user.mentioned_in.return_value = False

    with (
        patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user),
        patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create,
    ):
        mock_create.side_effect = RuntimeError("API connection timeout")
        await bot.on_message(mock_message)

    mock_message.reply.assert_called_once_with("❌ Lỗi: API connection timeout")
