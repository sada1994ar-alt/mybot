import discord
from discord.ext import commands
import os
from deep_translator import GoogleTranslator

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # ترجمه پیام به فارسی
    translated_text = GoogleTranslator(source='auto', target='fa').translate(message.content)
    await message.channel.send(f"ترجمه: {translated_text}")
    
    await bot.process_commands(message)

bot.run(os.environ['TOKEN'])
