
import os
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

# تنظیمات اولیه
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# بخش وب‌سرور برای آنلاین نگه داشتن ربات در رندر
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# اجرای وب‌سرور
keep_alive()

# رویداد آنلاین شدن
@bot.event
async def on_ready():
    print("بات ترجمه عمومی آنلاین شد!")
    print("آماده ترجمه در گروه ها...")

# دستور ترجمه (مثال)
@bot.command()
async def my_lang(ctx, lang):
    await ctx.send(f"زبان تنظیم شد به: {lang}")

# اجرای نهایی ربات با توکن امن
bot.run(os.environ.get('DISCORD_TOKEN'))
def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# اجرای ربات با استفاده از متغیر محیطی
bot.run(os.environ.get('DISCORD_TOKEN'))
