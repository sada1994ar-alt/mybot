import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

# تنظیمات اصلی بات
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# حافظه برای ذخیره زبان هر کاربر
user_languages = {}

@bot.event
async def on_ready():
    print("بات ترجمه عمومی آنلاین شد!")
    print("آماده ترجمه در گروه‌ها...")

# دستور برای کاربران جهت تنظیم زبان (مثال: !my_lang fa)
@bot.command()
async def my_lang(ctx, lang):
    user_languages[ctx.author.id] = lang
    await ctx.send(f"✅ زبان شما برای ترجمه روی `{lang}` تنظیم شد.")

@bot.event
async def on_message(message):
    # جلوگیری از پاسخ بات به خودش
    if message.author == bot.user:
        return

    # چک کردن تمام کاربرانی که زبانشان را ست کرده‌اند
    for user_id, target_lang in user_languages.items():
        if message.author.id != user_id:
            try:
                # ترجمه خودکار متن
                translated = GoogleTranslator(source='auto', target=target_lang).translate(message.content)
                
                if translated and translated.lower() != message.content.lower():
                    await message.channel.send(f"👤 <@{user_id}> | ترجمه به {target_lang}: {translated}")
            except:
                continue

    # برای اینکه دستورات بات همچنان کار کنند
    await bot.process_commands(message)

# توکن خود را در اینجا قرار دهید
bot.run('MTUxNjUyODM2NjY0MjEzOTM5Nw.GJD-6s.2G5jq8l2yDieo8mFPEXGKdMnVAfAK_FJnKdysg')
