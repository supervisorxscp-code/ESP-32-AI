from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot as bot_module


@pytest.mark.asyncio
async def test_on_message_ignores_self_message():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345

    mock_author = mock_bot_user

    mock_message = AsyncMock()
    mock_message.author = mock_author

    with patch.object(
        type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        await bot_module.on_message(mock_message)

    mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_unrelated_channel():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345
    mock_bot_user.mentioned_in = MagicMock(return_value=False)

    mock_author = MagicMock()
    mock_author.id = 99999

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel.id = 9999

    with patch.object(
        type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        await bot_module.on_message(mock_message)

    mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345
    mock_bot_user.mentioned_in = MagicMock(return_value=True)

    mock_author = MagicMock()
    mock_author.id = 99999

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel.id = 0
    mock_message.content = f"<@{mock_bot_user.id}>"

    with patch.object(
        type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        await bot_module.on_message(mock_message)

    mock_message.reply.assert_called_once_with("Bạn cần tôi giúp gì? Hãy nhập câu hỏi nhé!")


@pytest.mark.asyncio
async def test_on_message_valid_ai_response():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345
    mock_bot_user.mentioned_in = MagicMock(return_value=True)

    mock_author = MagicMock()
    mock_author.id = 99999

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel.id = 0
    mock_message.content = f"<@{mock_bot_user.id}> Xin chào"
    mock_message.channel.typing = MagicMock(return_value=typing_ctx)

    mock_choice = MagicMock()
    mock_choice.message.content = "Chào bạn! Tôi có thể giúp gì cho bạn?"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(
        type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ), patch.object(
        bot_module.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response
    ) as mock_create:
        await bot_module.on_message(mock_message)

        mock_create.assert_called_once()
        mock_message.reply.assert_called_once_with("Chào bạn! Tôi có thể giúp gì cho bạn?")


@pytest.mark.asyncio
async def test_on_message_truncates_long_response():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345
    mock_bot_user.mentioned_in = MagicMock(return_value=True)

    mock_author = MagicMock()
    mock_author.id = 99999

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel.id = 0
    mock_message.content = "Kể một câu chuyện dài"
    mock_message.channel.typing = MagicMock(return_value=typing_ctx)

    long_text = "A" * 2000
    mock_choice = MagicMock()
    mock_choice.message.content = long_text
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch.object(
        type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ), patch.object(
        bot_module.client.chat.completions, "create", new_callable=AsyncMock, return_value=mock_response
    ):
        await bot_module.on_message(mock_message)

        expected_reply = "A" * 1897 + "..."
        mock_message.reply.assert_called_once_with(expected_reply)


@pytest.mark.asyncio
async def test_on_message_handles_exception():
    mock_bot_user = MagicMock()
    mock_bot_user.id = 12345
    mock_bot_user.mentioned_in = MagicMock(return_value=True)

    mock_author = MagicMock()
    mock_author.id = 99999

    typing_ctx = AsyncMock()
    typing_ctx.__aenter__ = AsyncMock(return_value=None)
    typing_ctx.__aexit__ = AsyncMock(return_value=None)

    mock_message = AsyncMock()
    mock_message.author = mock_author
    mock_message.channel.id = 0
    mock_message.content = "Lỗi test"
    mock_message.channel.typing = MagicMock(return_value=typing_ctx)

    with patch.object(
        type(bot_module.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ), patch.object(
        bot_module.client.chat.completions, "create", new_callable=AsyncMock, side_effect=Exception("API limit")
    ):
        await bot_module.on_message(mock_message)

        mock_message.reply.assert_called_once_with("❌ Lỗi: API limit")
