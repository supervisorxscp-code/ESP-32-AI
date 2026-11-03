from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

import bot


@pytest.fixture
def mock_bot_user():
    user = MagicMock()
    user.id = 123456789
    user.name = "TestBot"
    return user


@pytest.mark.asyncio
async def test_on_message_ignores_bot_itself(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = AsyncMock()
        message.author = mock_bot_user
        await bot.on_message(message)
        message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_ignores_other_channel_without_mention(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = AsyncMock()
        message.author = MagicMock()
        message.channel.id = 999999999
        bot.CHANNEL_ID = 111111111
        bot.bot.user.mentioned_in = MagicMock(return_value=False)

        await bot.on_message(message)
        message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_empty_prompt_greeting(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = AsyncMock()
        message.author = MagicMock()
        message.channel.id = 111111111
        bot.CHANNEL_ID = 111111111
        bot.bot.user.mentioned_in = MagicMock(return_value=True)
        message.content = f"<@{mock_bot_user.id}>   "

        await bot.on_message(message)
        message.reply.assert_called_once_with(
            "Xin chào! Bạn muốn hỏi gì về ESP-32 hoặc AI hôm nay?"
        )


@pytest.mark.asyncio
async def test_on_message_typing_and_successful_response(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = AsyncMock()
        message.author = MagicMock()
        message.channel.id = 111111111
        bot.CHANNEL_ID = 111111111
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.content = "ESP32 là gì?"

        # Configure typing context manager mock
        typing_mock = AsyncMock()
        typing_mock.__aenter__.return_value = None
        typing_mock.__aexit__.return_value = None
        message.channel.typing = MagicMock(return_value=typing_mock)

        # Mock OpenAI response
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "ESP32 là vi điều khiển mạnh mẽ có WiFi và BLE."
        mock_completion.choices = [mock_choice]

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ) as mock_create:
            await bot.on_message(message)

            message.channel.typing.assert_called_once()
            typing_mock.__aenter__.assert_awaited_once()
            typing_mock.__aexit__.assert_awaited_once()
            mock_create.assert_awaited_once()
            message.reply.assert_called_once_with(
                "ESP32 là vi điều khiển mạnh mẽ có WiFi và BLE."
            )


@pytest.mark.asyncio
async def test_on_message_truncation(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = AsyncMock()
        message.author = MagicMock()
        message.channel.id = 111111111
        bot.CHANNEL_ID = 111111111
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.content = "Kể một câu chuyện rất dài"

        typing_mock = AsyncMock()
        typing_mock.__aenter__.return_value = None
        typing_mock.__aexit__.return_value = None
        message.channel.typing = MagicMock(return_value=typing_mock)

        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "A" * 2000
        mock_completion.choices = [mock_choice]

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_completion,
        ):
            await bot.on_message(message)

            expected_text = ("A" * 1897) + "..."
            message.reply.assert_called_once_with(expected_text)


@pytest.mark.asyncio
async def test_on_message_handles_exception(mock_bot_user):
    with patch.object(
        type(bot.bot), "user", new_callable=PropertyMock, return_value=mock_bot_user
    ):
        message = AsyncMock()
        message.author = MagicMock()
        message.channel.id = 111111111
        bot.CHANNEL_ID = 111111111
        bot.bot.user.mentioned_in = MagicMock(return_value=False)
        message.content = "Lỗi API"

        typing_mock = AsyncMock()
        typing_mock.__aenter__.return_value = None
        typing_mock.__aexit__.return_value = None
        message.channel.typing = MagicMock(return_value=typing_mock)

        with patch.object(
            bot.client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=RuntimeError("NVIDIA API timeout"),
        ):
            await bot.on_message(message)

            message.reply.assert_called_once_with("❌ Lỗi: NVIDIA API timeout")
