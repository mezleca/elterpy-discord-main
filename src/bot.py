import discord
from discord.ext import commands

# set intents
BOT_INTENTS = discord.Intents.default()

# set extra intents
BOT_INTENTS.message_content = True
BOT_INTENTS.guilds = True
BOT_INTENTS.voice_states = True
BOT_INTENTS.members = True

# set prefix, etc...W
Bot = commands.Bot(
    intents=BOT_INTENTS,
    command_prefix=commands.when_mentioned_or("."),
)

async def load_cogs():  
    await Bot.load_extension("src.commands.basic")
    await Bot.load_extension("src.commands.music")
    await Bot.load_extension('src.commands.nsfw')

async def main(TOKEN):
    await load_cogs()
    await Bot.start(TOKEN)
