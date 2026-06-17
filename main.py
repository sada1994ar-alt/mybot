import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ذخیره زبان کاربران به صورت {user_id: language_code}
user_languages = {}

@bot.command()
async def setlang(ctx, lang_code: str):
    user_languages[ctx.author.id] = lang_code.lower()
    await ctx.send(f"✅ زبان شما برای دریافت ترجمه‌ها روی {lang_code.upper()} تنظیم شد.")

@bot.event
async def on_message(message):
    # ربات به پیام‌های خودش پاسخ نمی‌دهد
    if message.author == bot.user:
        return
    
    # پردازش دستورات (مثل !setlang)
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    # ترجمه پیام برای هر کسی که زبانی تنظیم کرده
    # فقط پیام‌های عادی (بدون !) ترجمه می‌شوند
    for user_id, target_lang in user_languages.items():
        # ربات پیام را برای نویسنده اصلی ترجمه نمی‌کند
        if user_id != message.author.id:
            try:
                translated = GoogleTranslator(source='auto', target=target_lang).translate(message.content)
                # ارسال ترجمه به صورت ریپلای در همان کانال
                await message.channel.send(f"ترجمه برای <@{user_id}> ({target_lang.upper()}): {translated}")
            except Exception as e:
                print(f"Error translating: {e}")

keep_alive()
bot.run(os.environ['TOKEN'])
