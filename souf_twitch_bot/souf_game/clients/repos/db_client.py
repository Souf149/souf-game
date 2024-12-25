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
                username TEXT NOT NULL,
                score INTEGER NOT NULL DEFAULT 0,
                last_message DATE NOT NULL
            );""")
        self._connection.commit()

    def get_last_minute_users(self) -> list[str]:
        cursor = self._connection.cursor()
        # Query to select usernames of players with a message in the last 5 minutes, ordered by score
        cursor.execute("""
            SELECT username
            FROM players
            WHERE last_message >= datetime('now', '-5 minutes')
            ORDER BY score DESC
            LIMIT 5;
        """)
        # Fetch the results
        top_usernames = cursor.fetchall()

        # Extract the usernames from the result tuples
        return [row[0] for row in top_usernames]
