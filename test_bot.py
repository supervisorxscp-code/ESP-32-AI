from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch
import pytest
import bot


@pytest.mark.asyncio
async def test_on_message_ignores_self_messages():
    mock_message = AsyncMock()
    # Mock bot.user as property
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock) as mock_user_prop:
        mock_user = MagicMock()
        mock_user_prop.return_value = mock_user
        mock_message.author = mock_user

        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_wrong_channel_when_not_mentioned():
    mock_message = AsyncMock()
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock) as mock_user_prop:
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_user_prop.return_value = mock_user

        mock_message.author = MagicMock()
        mock_message.channel.id = 99999
        bot.bot.user.mentioned_in = MagicMock(return_value=False)

        await bot.on_message(mock_message)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_handling():
    mock_message = AsyncMock()
    with patch.object(type(bot.bot), "user", new_callable=PropertyMock) as mock_user_prop:
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_user_prop.return_value = mock_user

        mock_message.author = MagicMock()
        mock_message.channel.id = 99999
        mock_message.content = "<@12345>"
        bot.bot.user.mentioned_in = MagicMock(return_value=True)

        await bot.on_message(mock_message)
        mock_message.reply.assert_called_once_with(
            "Bạn cần trợ giúp gì? Hãy gửi câu hỏi cho mình nhé! 😊"
        )


@pytest.mark.asyncio
async def test_on_message_success_with_typing_and_truncation():
    mock_message = AsyncMock()
    typing_cm = AsyncMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing = MagicMock(return_value=typing_cm)

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock) as mock_user_prop:
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_user_prop.return_value = mock_user

        mock_message.author = MagicMock()
        mock_message.channel.id = 99999
        mock_message.content = "<@12345> Xin chào"
        bot.bot.user.mentioned_in = MagicMock(return_value=True)

        long_response = "A" * 2000
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message.content = long_response

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ):
            await bot.on_message(mock_message)

            mock_message.channel.typing.assert_called_once()
            mock_message.reply.assert_called_once()
            reply_text = mock_message.reply.call_args[0][0]
            assert len(reply_text) == 1900
            assert reply_text.endswith("...")


@pytest.mark.asyncio
async def test_on_message_error_handling():
    mock_message = AsyncMock()
    typing_cm = AsyncMock()
    typing_cm.__aenter__ = AsyncMock(return_value=None)
    typing_cm.__aexit__ = AsyncMock(return_value=None)
    mock_message.channel.typing = MagicMock(return_value=typing_cm)

    with patch.object(type(bot.bot), "user", new_callable=PropertyMock) as mock_user_prop:
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_user_prop.return_value = mock_user

        mock_message.author = MagicMock()
        mock_message.channel.id = 99999
        mock_message.content = "<@12345> Lỗi rồi"
        bot.bot.user.mentioned_in = MagicMock(return_value=True)

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=Exception("API Error"),
        ):
            await bot.on_message(mock_message)

            mock_message.reply.assert_called_once_with("❌ Lỗi: API Error")
