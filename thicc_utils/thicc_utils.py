from db_handler import db_handler
from sleeper_api_utils import sleeper_api_utils
import discord
import tempfile

TABLES = db_handler.Tables

def _is_players_table_populated()

def thicc(league_id: str, league_size: int):
    players_table = db_handler.Table(TABLES.PLAYERS)
    if not players_table.is_populated():
        payload = sleeper_api_utils.get_all_players()
        players_table.populate(payload)

    rosters_table = db_handler.Table(TABLES.ROSTERS)
    if not rosters_table.is_populated():
        payload = sleeper_api_utils.get_fantasy_rosters(league_id)
        rosters_table.populate(payload)

    all_team_weights = list()
    for roster_id in range(1, league_size + 1):
        res = db_handler.select("SELECT players FROM rosters WHERE roster_id=?", (roster_id,))
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
        file = discord.File(tmp, "thicc_utils.txt")
        return file