import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive
import sqlite3

# تنظیمات دیتابیس
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT)')
conn.commit()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def setlang(ctx, lang_code: str):
    c.execute('INSERT OR REPLACE INTO users (user_id, lang) VALUES (?, ?)', (ctx.author.id, lang_code))
    conn.commit()
    await ctx.send(f"✅ زبان شما به {lang_code} ذخیره شد.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    c.execute('SELECT lang FROM users WHERE user_id = ?', (message.author.id,))
    result = c.fetchone()
    
    if result:
        target_lang = result[0]
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(message.content)
            await message.reply(f"({target_lang.upper()}): {translated}")
        except Exception as e:
            print(f"Error: {e}")

    await bot.process_commands(message)

keep_alive()
bot.run(os.environ['TOKEN'])
