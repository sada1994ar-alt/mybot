import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

# تنظیمات اصلی ربات
intents = discord.Intents.default()
intents.message_content = True # این خط برای خواندن متن پیام‌ها ضروری است
bot = commands.Bot(command_prefix='!', intents=intents)

# حافظه موقت برای ذخیره زبان انتخابی هر کاربر
user_languages = {}

@bot.command()
async def setlang(ctx, lang_code: str):
    # ذخیره زبان کاربر با ID او
    user_languages[ctx.author.id] = lang_code.lower()
    await ctx.send(f"✅ زبان شما با موفقیت به {lang_code.upper()} تغییر کرد.")

@bot.event
async def on_message(message):
    # نادیده گرفتن پیام‌های خودِ ربات برای جلوگیری از حلقه تکرار
    if message.author == bot.user:
        return
    
    # اجازه دادن به ربات برای پردازش دستورات (مثل setlang)
    await bot.process_commands(message)

    # اگر کاربر قبلاً زبانی را انتخاب کرده باشد، پیامش را ترجمه کن
    if message.author.id in user_languages and not message.content.startswith('!'):
        target_lang = user_languages[message.author.id]
        try:
            # ترجمه خودکار متن پیام
            translated = GoogleTranslator(source='auto', target=target_lang).translate(message.content)
            # ارسال ترجمه به صورت پاسخ (Reply) به پیام اصلی
            await message.reply(f"({target_lang.upper()}): {translated}")
        except Exception as e:
            print(f"Error translating message: {e}")

keep_alive()
bot.run(os.environ['TOKEN'])
