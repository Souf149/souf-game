from souf_twitch_bot.bot import Bot
from souf_twitch_bot.config import settings


def main():
    print(f"Running with: {settings.model_dump_json()}")
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
