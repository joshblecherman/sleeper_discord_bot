from db_handler import db_handler
import requests
import os

TABLES = db_handler.Tables

ALL_PLAYERS_EP = "https://api.sleeper.app/v1/players/nfl"

ROSTER_NAME_MAP = {
    1: "Jeremy",
    2: "Garret",
    3: "Brill",
    4: "Evan Klein",
    5: "Seth",
    6: "Jared",
    7: "Tyler",
    8: "Danny",
    9: "Jacob",
    10: "Josh",
    11: "Charlie",
    12: "Evan Keiser"
}

def get_all_players():
    resp = requests.get(ALL_PLAYERS_EP)
    players = resp.json()
    columns = db_handler.Tables.PLAYERS.value["columns"]
    payload = {col: [] for col in columns}
    for player in players:
        data = players[player]
        for col in columns:
            if col in data:
                payload[col].append(data[col])
            else:
                payload[col].append(None)
    return payload


def get_fantasy_rosters(league_id):
    rosters_ep = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    resp = requests.get(rosters_ep)
    rosters = resp.json()
    columns = db_handler.Tables.ROSTERS.value["columns"]
    payload = {col: [] for col in columns}
    for roster in rosters:
        for player in roster["players"]:
            payload["players"].append(player)
            for col in columns:
                if not col == "players":
                    payload[col].append(roster[col])
    return payload
