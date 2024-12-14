from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import Config, Server
from souf_game.config import settings
from souf_game.game import Game


class Api:
    def __init__(self):
        if settings.game_api.port is None:
            raise Exception("PORT IS NOT SET")
        self.app = FastAPI()
        self.server = Server(
            config=Config(
                self.app, host=settings.game_api.host, port=settings.game_api.port
            )
        )

    def run(self):
        self.server.run()


api = Api()
game = Game()


class MessageEvent(BaseModel):
    message: str
    user_name: str


@api.app.post("/message", status_code=200)
def new_message(messageEvent: MessageEvent) -> None:
    game.new_message(messageEvent.message, messageEvent.user_name)
