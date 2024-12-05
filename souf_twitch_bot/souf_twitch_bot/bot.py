from twitchio.ext import commands  # type: ignore
from souf_twitch_bot.clients.repos.db_client import DbClient
from souf_twitch_bot.config import settings


class Bot(commands.Bot):
    def __init__(self):
        self.db_connection = DbClient()

        super().__init__(
            token=settings.access_token,
            prefix="souf ",
            initial_channels=["metabyte149", "faccboii", "csc14"],
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
    async def score(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        # await ctx.send(f"Hello {ctx.author.name}!")
        await ctx.send(f"Souf is the better lidia")
