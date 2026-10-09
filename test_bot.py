from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot as bot_module


@pytest.mark.asyncio
async def test_on_message_empty_prompt_reply():
    mock_author = MagicMock()
    mock_channel = MagicMock()
    mock_channel.id = 123
    mock_bot_user = MagicMock()
    mock_bot_user.id = 999

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel = mock_channel
    mock_message.content = "<@999>   "

    with patch.object(type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
        bot_module.bot.user.mentioned_in = MagicMock(return_value=True)

        await bot_module.on_message(mock_message)

        mock_message.reply.assert_called_once_with(
            "Bạn cần mình giúp gì? Hãy nhập câu hỏi hoặc yêu cầu của bạn nhé! 😊"
        )


@pytest.mark.asyncio
async def test_on_message_ai_success_with_typing():
    mock_author = MagicMock()
    mock_channel = MagicMock()
    mock_channel.id = 123

    typing_cm = AsyncMock()
    mock_channel.typing.return_value = typing_cm

    mock_bot_user = MagicMock()
    mock_bot_user.id = 999

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel = mock_channel
    mock_message.content = "<@999> Xin chào"

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Chào bạn, mình là trợ lý AI."))]

    with patch.object(bot_module.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_response
        with patch.object(type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
            bot_module.bot.user.mentioned_in = MagicMock(return_value=True)

            await bot_module.on_message(mock_message)

            mock_channel.typing.assert_called_once()
            mock_message.reply.assert_called_once_with("Chào bạn, mình là trợ lý AI.")


@pytest.mark.asyncio
async def test_on_message_truncation():
    mock_author = MagicMock()
    mock_channel = MagicMock()
    mock_channel.id = 123

    typing_cm = AsyncMock()
    mock_channel.typing.return_value = typing_cm

    mock_bot_user = MagicMock()
    mock_bot_user.id = 999

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel = mock_channel
    mock_message.content = "Viết bài văn dài"

    long_text = "A" * 2000
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=long_text))]

    with patch.object(bot_module.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_response
        with patch.object(type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user):
            bot_module.bot.user.mentioned_in = MagicMock(return_value=True)

            await bot_module.on_message(mock_message)

            mock_message.reply.assert_called_once()
            replied_content = mock_message.reply.call_args[0][0]
            assert len(replied_content) == 1900
            assert replied_content.endswith("...")
