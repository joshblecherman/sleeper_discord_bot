# bot.py
import os
import discord
from dotenv import load_dotenv
from discord import app_commands
import requests
from db_handler import db_handler
from sleeper_api_utils import sleeper_api_utils
import tempfile
from thicc_utils import thicc_utils

load_dotenv()

# DISCORD
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('GUILD_ID')
MY_GUILD = discord.Object(id=GUILD_ID)

# SLEEPER
LEAGUE_ID = os.getenv('SLEEPER_LEAGUE_ID')
LEAGUE_SIZE = 12

# STATE
TABLES = db_handler.Tables


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


client = MyClient(intents=discord.Intents.default())


@client.event
async def on_ready():
    guild = discord.guild.Guild
    for g in client.guilds:
        if g.name == GUILD:
            guild = g

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def close():
    db_handler.close()


@client.tree.command()
async def thicc(interaction: discord.Interaction):
    """Who has the thiccest fantasy team?"""
    file = thicc_utils.thicc(LEAGUE_ID, LEAGUE_SIZE)
    await interaction.response.send_message(file=file)


client.run(TOKEN)