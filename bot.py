import discord
import os
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
MAX_MESSAGE_LENGTH = 1900

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
        user_input = user_input.replace(f"<@{bot.user.id}>", "").strip()

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

        if len(ai_reply) > MAX_MESSAGE_LENGTH:
            ai_reply = ai_reply[:MAX_MESSAGE_LENGTH] + "..."

        await message.reply(ai_reply)
    except Exception as e:
        await message.reply(f"❌ Lỗi: {str(e)}")

bot.run(os.getenv("DISCORD_TOKEN"))