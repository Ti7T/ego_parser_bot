import discord
from discord.ext import commands
from parser import get_player_json
from JSONConverter import JSONConverter
from DiscordFormatter import DiscordFormatter

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, name):
        data = get_player_json(f"https://eternal-gores.com/api/profiles/by-nick/{name}")
        player = JSONConverter.to_player(data)
        embed = DiscordFormatter.player_profile(player)
        await ctx.send(embed=embed)

# Функция "setup" обязательна для загрузки Кога
async def setup(bot):
    await bot.add_cog(ProfileCog(bot))