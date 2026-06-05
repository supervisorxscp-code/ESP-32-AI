import discord
import os
import re
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

@bot.event
async def on_ready():
    print(f'✅ Bot đã online: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id != CHANNEL_ID and not bot.user.mentioned_in(message):
        return

    user_input = message.content
    if bot.user.mentioned_in(message):
        # Remove bot mention from message content
        user_input = re.sub(rf"<@!?{bot.user.id}>", "", user_input).strip()

    if not user_input and bot.user.mentioned_in(message):
        await message.reply("Xin chào! Bạn cần tôi giúp gì không? Hãy đặt câu hỏi cho tôi nhé! 😊")
        return

    try:
        async with message.channel.typing():
            response = await client.chat.completions.create(
                model="meta/llama-3.3-70b-instruct",
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý thông minh, trả lời ngắn gọn bằng tiếng Việt."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=800
            )
            ai_reply = response.choices[0].message.content
            if len(ai_reply) > 1900:
                ai_reply = ai_reply[:1897] + "..."
            await message.reply(ai_reply)
    except Exception:
        await message.reply("Rất tiếc, tôi gặp lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau! ❌")

bot.run(os.getenv("DISCORD_TOKEN"))