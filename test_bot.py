import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
import bot


@pytest.mark.asyncio
async def test_on_message_ignore_own_message():
    mock_user = MagicMock()
    mock_user.id = 12345

    mock_message = MagicMock()
    mock_message.author = mock_user

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_user):
        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt():
    bot_user = MagicMock()
    bot_user.id = 9999

    author = MagicMock()
    author.id = 1111

    mock_message = MagicMock()
    mock_message.author = author
    mock_message.content = "<@9999>"
    mock_message.channel.id = 123

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=bot_user):
        bot_user.mentioned_in = MagicMock(return_value=True)
        mock_message.reply = AsyncMock()

        await bot.on_message(mock_message)

        mock_message.reply.assert_called_once_with(
            "Bạn cần tôi giúp gì? Hãy nhập câu hỏi nhé!"
        )


@pytest.mark.asyncio
async def test_on_message_successful_ai_response():
    bot_user = MagicMock()
    bot_user.id = 9999

    author = MagicMock()
    author.id = 1111

    mock_message = MagicMock()
    mock_message.author = author
    mock_message.content = "Chào bot"
    mock_message.channel.id = 123

    typing_cm = AsyncMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing = MagicMock(return_value=typing_cm)

    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content="Xin chào! Tôi có thể giúp gì cho bạn?"))
    ]

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=bot_user):
        bot_user.mentioned_in = MagicMock(return_value=True)
        mock_message.reply = AsyncMock()

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_completion

            await bot.on_message(mock_message)

            mock_message.reply.assert_called_once_with("Xin chào! Tôi có thể giúp gì cho bạn?")


@pytest.mark.asyncio
async def test_on_message_truncation_with_ellipsis():
    bot_user = MagicMock()
    bot_user.id = 9999

    author = MagicMock()
    author.id = 1111

    mock_message = MagicMock()
    mock_message.author = author
    mock_message.content = "Viết một bài văn dài"
    mock_message.channel.id = 123

    typing_cm = AsyncMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing = MagicMock(return_value=typing_cm)

    long_response = "A" * 2000
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content=long_response))
    ]

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=bot_user):
        bot_user.mentioned_in = MagicMock(return_value=True)
        mock_message.reply = AsyncMock()

        with patch.object(bot.client.chat.completions, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_completion

            await bot.on_message(mock_message)

            expected_reply = "A" * 1897 + "..."
            mock_message.reply.assert_called_once_with(expected_reply)
