import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive  # اضافه شد

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    translated = GoogleTranslator(source='auto', target='fa').translate(message.content)
    await message.channel.send(f"ترجمه: {translated}")
    await bot.process_commands(message)

keep_alive()  # اضافه شد
bot.run(os.environ['TOKEN'])
