from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.mark.asyncio
async def test_on_message_ignores_self():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 123456

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        mock_message = AsyncMock()
        mock_message.author = mock_bot_user

        await bot.on_message(mock_message)

        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_mention():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 123456

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        mock_message = AsyncMock()
        mock_message.author = MagicMock()
        mock_message.channel.id = 99999  # Not CHANNEL_ID
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        mock_message.content = "<@123456>"

        await bot.on_message(mock_message)

        mock_message.reply.assert_called_once_with("Xin chào! Bạn cần mình giúp gì nào? 😊")


@pytest.mark.asyncio
async def test_on_message_success_flow():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 123456

    with patch.object(type(bot.bot), 'user', new_callable=PropertyMock, return_value=mock_bot_user):
        mock_message = AsyncMock()
        mock_message.author = MagicMock()
        mock_message.channel.id = bot.CHANNEL_ID
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        mock_message.content = "Chào bot"

        # Mock typing context manager
        typing_mock = AsyncMock()
        typing_mock.__aenter__ = AsyncMock(return_value=None)
        typing_mock.__aexit__ = AsyncMock(return_value=None)
        mock_message.channel.typing = MagicMock(return_value=typing_mock)

        # Mock AsyncOpenAI response
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content="Chào bạn!"))]

        with patch.object(bot.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_completion

            await bot.on_message(mock_message)

            mock_create.assert_called_once()
            mock_message.channel.typing.assert_called_once()
            mock_message.reply.assert_called_once_with("Chào bạn!")
