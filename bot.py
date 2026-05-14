import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("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")
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
        user_input = user_input.replace(f"<@{bot.user.id}>", "").strip()

    try:
        response = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý thông minh, trả lời ngắn gọn bằng tiếng Việt."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=800
        )
        ai_reply = response.choices[0].message.content
        await message.reply(ai_reply[:1900])
    except Exception as e:
        await message.reply(f"❌ Lỗi: {str(e)}")

bot.run(os.getenv("DISCORD_TOKEN"))