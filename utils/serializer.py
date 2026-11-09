import discord

def serialize_emoji(emoji: discord.PartialEmoji | str) -> str:
    return str(emoji)