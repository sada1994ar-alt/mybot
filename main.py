import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# حافظه برای ذخیره زبان کاربران
user_languages = {}

@bot.command()
async def setlang(ctx, lang_code: str):
    # ذخیره زبان کاربر
    user_languages[ctx.author.id] = lang_code.lower()
    await ctx.send(f"✅ زبان شما به {lang_code} تغییر کرد.")

@bot.event
async def on_message(message):
    # اگر پیام از طرف خود ربات بود، نادیده بگیر
    if message.author == bot.user:
        return
    
    # اگر پیام یک دستور (مثل !setlang) بود، آن را پردازش کن
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    # اگر کاربر قبلاً زبانی انتخاب کرده بود، پیامش را ترجمه کن
    if message.author.id in user_languages:
        target_lang = user_languages[message.author.id]
        try:
            # ترجمه خودکار
            translated = GoogleTranslator(source='auto', target=target_lang).translate(message.content)
            # ارسال ترجمه به صورت ریپلای
            await message.reply(f"({target_lang.upper()}): {translated}")
        except Exception as e:
            print(f"خطا در ترجمه: {e}")

keep_alive()
bot.run(os.environ['TOKEN'])
