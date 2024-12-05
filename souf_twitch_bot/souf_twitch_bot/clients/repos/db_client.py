from datetime import datetime, timedelta
from souf_twitch_bot.clients.interfaces.db_client_interface import DbClientInterface
import sqlite3

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class DbClient(DbClientInterface):
    def __init__(self) -> None:
        self._connection = sqlite3.connect("players.db")
        cursor = self._connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                user_id TEXT PRIMARY KEY NOT NULL,
                score INTEGER NOT NULL DEFAULT 0,
                last_message DATE NOT NULL
            );""")
        self._connection.commit()
        print("Database connected")

    def new_message_from_user(self, user_id: str):
        cursor = self._connection.cursor()
        cursor.execute("SELECT last_message FROM players WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        print(f"FOUND USER {result}")
        print((datetime.now().strftime(DATE_FORMAT), user_id))
        if result is None:
            self._create_new_user(user_id)
            return

        if datetime.now() - datetime.strptime(result[0], DATE_FORMAT) >= timedelta(
            minutes=1
        ):
            print("UPDATING")
            cursor.execute(
                "UPDATE players SET score = score + 1, last_message = ? WHERE user_id = ?",
                (datetime.now().strftime(DATE_FORMAT), user_id),
            )
            self._connection.commit()

    def _create_new_user(self, user_id: str):
        print("Creating new user")
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO players (user_id, score, last_message) VALUES (?, ?, ?);",
            (user_id, 1, datetime.now().strftime(DATE_FORMAT)),
        )
        self._connection.commit()
