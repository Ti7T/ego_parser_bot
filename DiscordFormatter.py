import discord

import PlayerStats


class DiscordFormatter:

    @staticmethod
    def player_profile(player: PlayerStats) -> discord.Embed:
        embed = discord.Embed(
            title=f"📊 Статистика игрока {player.nick}",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="👤 Игрок",
            value=player.nick,
            inline=True
        )

        embed.add_field(
            name="🏰 Клан",
            value=player.clan.name or "Нет",
            inline=True
        )

        embed.add_field(
            name="⭐ Очки",
            value=f"{player.points:,}".replace(",", " "),
            inline=True
        )

        embed.add_field(
            name="🗺️ Пройдено карт",
            value=str(player.total_finished_maps),
            inline=True
        )

        counts = player.counts
        counts_total = player.counts_total

        embed.add_field(
            name="📈 Прогресс",
            value=(
                f"🟢 Easy: **{counts.easy}/{counts_total.easy}**\n"
                f"🔵 Main: **{counts.main}/{counts_total.main}**\n"
                f"🟠 Hard: **{counts.hard}/{counts_total.hard}**\n"
                f"🔴 Insane: **{counts.insane}/{counts_total.insane}**\n"
                f"⚫ Extreme: **{counts.extreme}/{counts_total.extreme}**\n"
                f"🟣 Solo: **{counts.solo}/{counts_total.solo}**\n"
                f"🟡 Jet: **{counts.jet}/{counts_total.jet}**\n"
                f"⚙️ Mods: **{counts.mods}/{counts_total.mods}**"
            ),
            inline=False
        )

        if player.best_teammates:
            teammates = "\n".join(
                f"• {name}"
                for name in player.best_teammates[:10]
            )

            embed.add_field(
                name="🤝 Лучшие тиммейты",
                value = "\n".join(
                    f"• {t.nickname} — {t.count} карт"
                    for t in player.best_teammates
                ),
                inline=False
            )

        completion = (
            player.total_finished_maps /
            (
                counts_total.easy
                + counts_total.main
                + counts_total.hard
                + counts_total.insane
                + counts_total.extreme
                + counts_total.solo
                + counts_total.jet
                + counts_total.mods
            )
            * 100
        )

        embed.set_footer(
            text=f"Общий прогресс: {completion:.1f}%"
        )

        return embed