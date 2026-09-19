import asyncio
import discord
from discord.ext import commands
from api import init_session, close_session
from config import BOT_TOKEN
import logging
from database import init_database

discord.utils.setup_logging(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов!')

async def setup_hook():
    await bot.load_extension('cogs.profile')
    await bot.load_extension('cogs.emoji_limiter')
    await bot.tree.sync()

bot.setup_hook = setup_hook

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: discord.app_commands.AppCommandError
):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message(
            "У тебя недостаточно прав для использования этой команды.",
            ephemeral=True
        )
        return

    # Все неизвестные ошибки продолжаем выводить в консоль
    print(f"Ошибка в slash-команде: {error}")

    import traceback
    traceback.print_exception(
        type(error),
        error,
        error.__traceback__
    )

async def main():
    await init_session()
    init_database()
    try:
        async with bot:
            await bot.start(BOT_TOKEN)
    finally:
        await close_session()
        print("Сессия закрыта")

if __name__ == "__main__":
    asyncio.run(main(), debug=True)