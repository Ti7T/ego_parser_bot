import discord
from discord.ext import commands
from discord import app_commands
from services import create_profile, get_player

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profile",
        description="Показать статистику игрока на EGO серверах"
    )
    @app_commands.describe(
        nick="Ник игрока на EGO"
    )
    async def profile(
        self,
        interaction: discord.Interaction,
        nick: str
    ):
        await interaction.response.defer(thinking=True)
        player = await get_player(nick)
        image = await create_profile(player)
        file = discord.File(
            fp=image, 
            filename="profile.png"
        )
        await interaction.followup.send(file=file)

    @app_commands.command(
        name="private_profile",
        description="Показать невидимую для остальных кроме вас статистику игрока на EGO серверах"
    )
    @app_commands.describe(
        nick="Ник игрока на EGO"
    )
    async def private_profile(
        self,
        interaction: discord.Interaction,
        nick: str
    ):
        await interaction.response.defer(ephemeral=True, thinking=True)
        player = await get_player(nick)
        image = await create_profile(player)
        file = discord.File(
            fp=image, 
            filename="profile.png"
        )
        await interaction.followup.send(file=file, ephemeral=True)
    
    # @commands.command()
    # async def profile(self, ctx, name):
    #     data = get_player_json(f"https://eternal-gores.com/api/profiles/by-nick/{name}")
    #     player = JSONConverter.to_player(data)
    #     embed = create_profile_embed(player)
    #     await ctx.send(embed=embed)

    # @profile.error
    # async def profile_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send(
    #             "❌ Вы не указали ник.\n"
    #             "Использование: `!profile <ник>`"
    #         )
    #     else:
    #         raise error

# Функция "setup" обязательна для загрузки Кога
async def setup(bot):
    await bot.add_cog(ProfileCog(bot))