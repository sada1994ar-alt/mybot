import discord
from discord.ext import commands
import aiosqlite
from googletrans import Translator
import os
from flask import Flask
from threading import Thread

# تنظیمات ربات
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
translator = Translator()

# دیتابیس برای ذخیره زبان کاربرها
async def init_db():
    async with aiosqlite.connect("user_languages.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT)")
        await db.commit()

@bot.event
async def on_ready():
    await init_db()
    print(f'Bot is ready: {bot.user}')

# دستور تنظیم زبان
@bot.command()
async def set_lang(ctx, lang: str):
    async with aiosqlite.connect("user_languages.db") as db:
        await db.execute("INSERT OR REPLACE INTO users (user_id, lang) VALUES (?, ?)", (ctx.author.id, lang))
        await db.commit()
    await ctx.send(f"زبان شما با موفقیت به {lang} تغییر یافت.")

# ترجمه خودکار پیام‌ها
@bot.event
async def on_message(message):
    if message.author == bot.user or message.content.startswith('!'):
        await bot.process_commands(message)
        return
    
    async with aiosqlite.connect("user_languages.db") as db:
        async with db.execute("SELECT lang FROM users WHERE user_id = ?", (message.author.id,)) as cursor:
            row = await cursor.fetchone()
    
    if row:
        target_lang = row[0]
        try:
            translated = translator.translate(message.content, dest=target_lang)
            await message.channel.send(f"{message.author.name}: {translated.text}")
        except:
            pass # اگر زبان اشتباه بود، ربات خطا نمی‌دهد
    
    await bot.process_commands(message)

# بخش وب‌سرور برای آنلاین ماندن
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is alive!"
def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run).start()
    # در اینجا ربات از محیط هاست توکن را می‌خواند
    bot.run(os.environ['TOKEN'])
