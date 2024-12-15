import multiprocessing
from multiprocessing.context import Process
from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import Config, Server
from souf_game.config import settings
from souf_game.game import Game


class Api(Process):
    def __init__(self, app):
        if settings.game_api.port is None:
            raise Exception("PORT IS NOT SET")

        super().__init__()
        self.app = app
        self.server = Server(
            config=Config(
                self.app, host=settings.game_api.host, port=settings.game_api.port
            )
        )

    def stop(self) -> None:
        self.terminate()

    def run(self):
        self.server.run()


app = FastAPI()
api = Api(app)
game = Game()
api.run()
game.run()


class MessageEvent(BaseModel):
    message: str
    username: str


@app.post("/message", status_code=200)
def new_message(messageEvent: MessageEvent) -> None:
    game.new_message(messageEvent.message, messageEvent.username)
