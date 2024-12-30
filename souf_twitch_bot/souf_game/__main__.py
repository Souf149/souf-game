from souf_game.config import settings
from souf_game.game import Game


def main():
    print(f"Running with: {settings.model_dump_json()}")

    g = Game()
    g.run()


if __name__ == "__main__":
    main()
