import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ذخیره زبان کاربران: {user_id: lang_code}
user_languages = {}

@bot.command()
async def setlang(ctx, lang_code: str):
    user_languages[ctx.author.id] = lang_code.lower()
    await ctx.send(f"✅ زبان مقصد شما برای دریافت ترجمه‌ها روی {lang_code.upper()} تنظیم شد.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # پردازش دستورات
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    # ارسال ترجمه به همه افرادی که زبان خود را ست کرده‌اند
    for user_id, target_lang in user_languages.items():
        if user_id != message.author.id: # برای خودِ شخص ترجمه نکند
            try:
                translated = GoogleTranslator(source='auto', target=target_lang).translate(message.content)
                user = await bot.fetch_user(user_id)
                # ارسال به صورت پیام خصوصی یا در کانال (اینجا به صورت ریپلای در کانال است)
                await message.channel.send(f"ترجمه برای <@{user_id}> ({target_lang.upper()}): {translated}")
            except Exception as e:
                print(f"Error: {e}")

keep_alive()
bot.run(os.environ['TOKEN'])
