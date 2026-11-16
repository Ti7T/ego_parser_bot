
import logging
from datetime import time
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks

from api import get_player_fire_json, JSONConverter
from database import get_linked_players_with_ids, get_command_channel


logger = logging.getLogger(__name__)

MOSCOW_TZ = ZoneInfo("Europe/Moscow")

REMINDER_TIMES = {
    time(hour=19, tzinfo=MOSCOW_TZ): 8,
    time(hour=21, tzinfo=MOSCOW_TZ): 6,
    time(hour=22, tzinfo=MOSCOW_TZ): 5,
    time(hour=23, tzinfo=MOSCOW_TZ): 4,
    time(hour=0, tzinfo=MOSCOW_TZ): 3,
}


class FireReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.fire_reminders.start()

    async def cog_unload(self):
        self.fire_reminders.cancel()

    @tasks.loop(
        time=list(REMINDER_TIMES.keys())
    )
    async def fire_reminders(self):
        now = discord.utils.utcnow().astimezone(MOSCOW_TZ)
        hours_left = REMINDER_TIMES.get(
            now.replace(second=0, microsecond=0).timetz()
        )

        if hours_left is None:
            return

        linked_players = get_linked_players_with_ids()

        if not linked_players:
            return

        for guild in self.bot.guilds:
            channel_id = get_command_channel(guild.id)

            if channel_id is None:
                continue

            channel = guild.get_channel(channel_id)

            if channel is None:
                try:
                    channel = await guild.fetch_channel(channel_id)
                except discord.HTTPException:
                    logger.exception(
                        "Не удалось получить канал напоминаний на сервере %s",
                        guild.id,
                    )
                    continue

            for user_id, nick in linked_players:
                member = guild.get_member(user_id)

                if member is None:
                    continue

                try:
                    data = await get_player_fire_json(nick)

                    if data is None:
                        logger.warning(
                            "Не удалось получить огонёк игрока %s",
                            nick,
                        )
                        continue

                    fire = JSONConverter.to_fireStats(data)

                    if fire.done_today:
                        continue

                    await channel.send(
                        f"{member.mention}, не забудь сохранить огонёк! "
                        f"До его сброса осталось **{hours_left} ч.** 🔥",
                        allowed_mentions=discord.AllowedMentions(
                            users=True,
                            roles=False,
                            everyone=False,
                        ),
                    )

                except discord.HTTPException:
                    logger.exception(
                        "Не удалось отправить напоминание игроку %s",
                        nick,
                    )
                except Exception:
                    logger.exception(
                        "Ошибка проверки огонька игрока %s",
                        nick,
                    )

    @fire_reminders.before_loop
    async def before_fire_reminders(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(FireReminderCog(bot))
