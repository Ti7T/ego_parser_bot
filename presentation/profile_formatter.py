import discord
from models import Player
from localization import TEXTS


def create_profile_embed(player: Player, language: str = "ru") -> discord.Embed:
    text = TEXTS.get(language, TEXTS["ru"])
    embed = discord.Embed(
        title=text["profile_title"].format(nick=player.nick),
        color=discord.Color.blue(),
    )
    embed.add_field(name=text["profile_player"], value=player.nick, inline=True)
    embed.add_field(
        name=text["profile_clan"],
        value=player.clan.name if player.clan else text["profile_none"],
        inline=True,
    )
    embed.add_field(
        name=text["profile_points"],
        value=f"{player.points:,}".replace(",", " "),
        inline=True,
    )
    embed.add_field(
        name=text["profile_maps"],
        value=str(player.total_finished_maps),
        inline=True,
    )

    counts = player.counts
    totals = player.counts_total
    embed.add_field(
        name=text["profile_progress"],
        value=(
            f"🟢 Easy: **{counts.easy}/{totals.easy}**\n"
            f"🔵 Main: **{counts.main}/{totals.main}**\n"
            f"🟠 Hard: **{counts.hard}/{totals.hard}**\n"
            f"🔴 Insane: **{counts.insane}/{totals.insane}**\n"
            f"⚫ Extreme: **{counts.extreme}/{totals.extreme}**\n"
            f"🟣 Solo: **{counts.solo}/{totals.solo}**\n"
            f"🟡 Jet: **{counts.jet}/{totals.jet}**\n"
            f"⚙️ Mods: **{counts.mods}/{totals.mods}**"
        ),
        inline=False,
    )

    if player.best_teammates:
        embed.add_field(
            name=text["profile_teammates"],
            value="\n".join(
                f"• {teammate.nickname} — "
                f"{text['profile_maps_count'].format(count=teammate.count)}"
                for teammate in player.best_teammates
            ),
            inline=False,
        )

    total_maps = sum(
        getattr(totals, field)
        for field in ("easy", "main", "hard", "insane", "extreme", "solo", "jet", "mods")
    )
    completion = player.total_finished_maps / total_maps * 100 if total_maps else 0
    embed.set_footer(text=text["profile_overall"].format(percent=completion))
    return embed
