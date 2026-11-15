from datetime import time
from zoneinfo import ZoneInfo
from discord.ext import commands, tasks
from services import save_linked_players


class PlayerSnapshotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.daily_player_snapshot.start()

    def cog_unload(self):
        self.daily_player_snapshot.cancel()

    @tasks.loop(
        time=time(hour=3, minute=0, tzinfo=ZoneInfo("Europe/Moscow"))
    )
    async def daily_player_snapshot(self):
        await save_linked_players()

    @daily_player_snapshot.before_loop
    async def before_snapshot(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(PlayerSnapshotsCog(bot))