import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=new_intents)

# زبان پیش‌فرض همه فارسی است
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # ترجمه خودکار به فارسی
    try:
        translated = GoogleTranslator(source='auto', target='fa').translate(message.content)
        await message.reply(f"ترجمه: {translated}")
    except:
        pass
    await bot.process_commands(message)

keep_alive()
bot.run(os.environ['TOKEN'])
