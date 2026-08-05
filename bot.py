import discord
from discord.ext import commands
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов!')
    await bot.load_extension('cogs.profile')
    await bot.tree.sync()

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(BOT_TOKEN)