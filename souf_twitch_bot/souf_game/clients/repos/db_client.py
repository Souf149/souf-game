from datetime import datetime, timedelta
from souf_twitch_bot.clients.interfaces.db_client_interface import DbClientInterface
import sqlite3

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class DbClient(DbClientInterface):
    def __init__(self) -> None:
        self._connection = sqlite3.connect("players.db")
        cursor = self._connection.cursor()
        # Modify the table schema to include 'username' column
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                user_id TEXT PRIMARY KEY NOT NULL,
                username TEXT NOT NULL,  -- New 'username' column
                score INTEGER NOT NULL DEFAULT 0,
                last_message DATE NOT NULL
            );""")
        self._connection.commit()
        print("Database connected")

    def new_message_from_user(self, user_id: str, username: str):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT last_message, username FROM players WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        print(f"FOUND USER {result}")
        print((datetime.now().strftime(DATE_FORMAT), user_id))

        if result is None:
            self._create_new_user(user_id, username)
            return

        # Update score and last_message if the last message is older than 1 minute
        if datetime.now() - datetime.strptime(result[0], DATE_FORMAT) >= timedelta(
            seconds=5
        ):
            print("UPDATING")
            cursor.execute(
                "UPDATE players SET score = score + 1, last_message = ?, username = ? WHERE user_id = ?",
                (datetime.now().strftime(DATE_FORMAT), username, user_id),
            )
            self._connection.commit()

    def _create_new_user(self, user_id: str, username: str):
        print("Creating new user")
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO players (user_id, username, score, last_message) VALUES (?, ?, ?, ?);",
            (user_id, username, 1, datetime.now().strftime(DATE_FORMAT)),
        )
        self._connection.commit()

    def get_top_3_players(self):
        cursor = self._connection.cursor()

        cursor.execute("""
            SELECT username, score FROM players
            ORDER BY score DESC
            LIMIT 3;
        """)
        return cursor.fetchall()

    def get_score_of_player(self, id: str):
        cursor = self._connection.cursor()

        cursor.execute(
            """
            SELECT score FROM players
            WHERE user_id = ?     
                       """,
            (id,),
        )

        result = cursor.fetchone()

        print(result) # TODO: FIX THIS
