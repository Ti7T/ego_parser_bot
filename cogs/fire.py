
import logging
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from discord.ext import commands, tasks

from api import get_player_fire_json, JSONConverter
from database import get_linked_players, set_fire_history


logger = logging.getLogger(__name__)

MOSCOW_TZ = ZoneInfo("Europe/Moscow")


class FireCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.save_fire_history.start()

    async def cog_unload(self):
        self.save_fire_history.cancel()

    @tasks.loop(
        time=[
            time(hour=2, minute=55, tzinfo=MOSCOW_TZ),
            time(hour=2, minute=58, tzinfo=MOSCOW_TZ),
        ]
    )
    async def save_fire_history(self):
        now = datetime.now(MOSCOW_TZ)
        game_date = (now - timedelta(hours=3)).date().isoformat()

        nicks = get_linked_players()

        if not nicks:
            logger.info("Нет привязанных игроков для сохранения огоньков")
            return

        saved = 0

        for nick in nicks:
            try:
                data = await get_player_fire_json(nick)

                if data is None:
                    logger.warning("Не удалось получить огонёк игрока %s", nick)
                    continue

                fire = JSONConverter.to_fireStats(data)

                set_fire_history(
                    nick=nick,
                    game_date=game_date,
                    current=fire.current,
                    best=fire.best,
                    done_today=fire.done_today,
                    badge=fire.badge,
                )

                saved += 1

            except Exception:
                logger.exception("Ошибка при сохранении огонька игрока %s", nick)

    @save_fire_history.before_loop
    async def before_save_fire_history(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(FireCog(bot))
