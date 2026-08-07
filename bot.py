import asyncio
import discord
from discord.ext import commands
from api import init_session, close_session
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов!')
    init_session()
    await bot.load_extension('cogs.profile')
    await bot.tree.sync()

async def main():
    try:
        await bot.start(BOT_TOKEN)
    finally:
        await close_session()
        print("Сессия закрыта")

if __name__ == "__main__":
    asyncio.run(main())