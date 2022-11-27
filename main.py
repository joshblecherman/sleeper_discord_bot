# bot.py
import os
import discord
from dotenv import load_dotenv
from discord import app_commands
import requests
from db_handler import db_handler
from sleeper_api_utils import sleeper_api_utils
import tempfile

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

    players_table = db_handler.Table(TABLES.PLAYERS)
    if not players_table.is_populated():
        payload = sleeper_api_utils.get_all_players()
        players_table.populate(payload)

    rosters_table = db_handler.Table(TABLES.ROSTERS)
    if not rosters_table.is_populated():
        payload = sleeper_api_utils.get_fantasy_rosters(LEAGUE_ID)
        rosters_table.populate(payload)

    all_team_weights = list()
    for roster_id in range(1, LEAGUE_SIZE + 1):
        roster_query = f"SELECT players FROM rosters WHERE roster_id=?"
        res = db_handler.select(roster_query, (roster_id,))
        players = [player[0] for player in res]
        weight_query = f"""
            SELECT weight, first_name, last_name FROM players WHERE player_id in ({', '.join(['?' for _ in range(len(players))])})
        """
        res = db_handler.select(weight_query, players)
        total_weight = 0
        team_weights = list()
        name = sleeper_api_utils.ROSTER_NAME_MAP[roster_id]
        team_weights.append(f"{name}\n")
        for player in res:
            if player[0] is not None:
                player_str = f"{player[1]} {player[2]}: {player[0]}\n"
                total_weight += int(player[0])
                team_weights.append(player_str)
        team_weights.append(f"total weight: {total_weight}\n")
        team_weights_str = "".join(team_weights)
        all_team_weights.append(team_weights_str)

    all_team_weights_str = "\n".join(all_team_weights)

    with tempfile.TemporaryFile(mode="w+") as tmp:
        tmp.write(all_team_weights_str)
        tmp.seek(0)
        file = discord.File(tmp, "thicc.txt")
        await interaction.response.send_message(file=file)

client.run(TOKEN)