import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

# تنظیمات اولیه
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# حافظه موقت برای ذخیره زبان‌ها
user_languages = {}

@bot.command()
async def setlang(ctx, lang_code: str):
    user_languages[ctx.author.id] = lang_code
    await ctx.send(f"✅ زبان شما به {lang_code} تغییر کرد.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # ترجمه بر اساس زبان انتخابی (اگر انتخاب نکرده باشند، پیش‌فرض انگلیسی)
    lang = user_languages.get(message.author.id, 'en')
    try:
        translated = GoogleTranslator(source='auto', target=lang).translate(message.content)
        await message.reply(f"({lang.upper()}): {translated}")
    except:
        pass
    
    await bot.process_commands(message)

keep_alive()
bot.run(os.environ['TOKEN'])
