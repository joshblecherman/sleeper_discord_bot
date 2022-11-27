import sqlite3
from enum import Enum
import os


class Tables(Enum):
    PLAYERS = dict(
        name="players",
        columns=[
            "last_name", "first_name", "player_id", "position", "number", "weight", "team"
        ]
    )
    ROSTERS = dict(
        name="rosters",
        columns=[
            "roster_id", "owner_id", "players"
        ]
    )


class Table:
    def __init__(self, table: Enum):
        self.name = table.value["name"]
        self.columns = table.value["columns"]
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        con = sqlite3.connect("state.db")
        cur = con.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.name} ({', '.join(self.columns)});")
        con.close()

    def is_populated(self) -> bool:
        con = sqlite3.connect("state.db")
        cur = con.cursor()
        populated = cur.execute(f"SELECT * FROM {self.name}").fetchone()
        con.close()
        if populated is None:
            return False
        return True

    def populate(self, data: dict):
        data_cols = [data[col] for col in self.columns]
        con = sqlite3.connect("state.db")
        rows = zip(*data_cols)
        con.executemany(f"""
            INSERT INTO {self.name}({", ".join([col for col in self.columns])}) VALUES
                ({", ".join(["?" for _ in range(len(self.columns))])})
        """, rows)
        con.commit()
        con.close()


def select(query, parameters):
    con = sqlite3.connect("state.db")
    cur = con.cursor()
    result = cur.execute(query, parameters).fetchall()
    con.close()
    return result


def close():
    os.remove("state.db")
