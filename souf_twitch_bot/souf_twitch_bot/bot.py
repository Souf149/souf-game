from twitchio.ext import commands  # type: ignore
from souf_twitch_bot.clients.repos.db_client import DbClient
from souf_twitch_bot.clients.repos.game_client import GameClient
from souf_twitch_bot.config import settings


class Bot(commands.Bot):
    def __init__(self):
        self.db_connection = DbClient()
        self.game_connection = GameClient()
        super().__init__(
            token=settings.access_token,
            prefix="souf ",
            initial_channels=["metabyte149"],
        )

    async def event_ready(self):
        print(f"Logged in. {self.user_id} | {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        print(
            f"Message:\t{message.author.id}\t{message.author.display_name}\t{message.content}"
        )
        self.db_connection.new_message_from_user(
            message.author.id, message.author.display_name
        )
        await self.handle_commands(message)

    @commands.command()
    async def top(self, ctx: commands.Context):
        leaderboard_msg = "Leaderboard 🔥 | "
        for player_score in self.db_connection.get_top_5_players():
            leaderboard_msg += f"{player_score[0]}: {player_score[1]} --"

        await ctx.send(leaderboard_msg)

    @commands.command()
    async def score(self, ctx: commands.Context):
        player_score = self.db_connection.get_score_of_player(ctx.author.id)

        await ctx.send(f"{ctx.author.name}'s score is {player_score}")

    @commands.command()
    async def ryan(self, ctx: commands.Context):
        await ctx.send("Ryan is kkr nep")

    @commands.command()
    async def dragon(self, ctx: commands.Context):
        await ctx.send("Aashir is washed")
