import asyncio
import discord
from discord.ext import commands
from api import init_session, close_session
from config import BOT_TOKEN
import logging
from database import init_database
from pathlib import Path
from services import PlayerNotFoundError


discord.utils.setup_logging(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов!')

async def setup_hook():
    cogs_path = Path("cogs")

    for file in cogs_path.glob("*.py"):
        if file.name == "__init__.py":
            continue

        extension = f"cogs.{file.stem}"
        await bot.load_extension(extension)

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

    original = getattr(error, "original", error)

    if isinstance(original, PlayerNotFoundError):
        message = "❌ Игрок не найден. Проверь правильность ника."

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(
                message,
                ephemeral=True,
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