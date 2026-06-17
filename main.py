import discord
from discord.ext import commands
import os
from googletrans import Translator

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.event
async def on_message(message):
    if message.author == bot.user or message.content.startswith('!'):
        await bot.process_commands(message)
        return
    
    # ترجمه ساده برای تست
    translated = translator.translate(message.content, dest='fa')
    await message.channel.send(f"ترجمه: {translated.text}")
    await bot.process_commands(message)

bot.run(os.environ['TOKEN'])
