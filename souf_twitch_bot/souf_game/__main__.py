from souf_game.api import api
from souf_game.config import settings


def main():
    print(f"Running with: {settings.model_dump_json()}")

    api.run()


if __name__ == "__main__":
    main()
