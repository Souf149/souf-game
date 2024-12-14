import httpx
from pydantic import BaseModel

from souf_twitch_bot.clients.interfaces.game_client_interface import GameClientInterface
from souf_twitch_bot.config import settings


class MessageEvent(BaseModel):
    message: str
    username: str


class GameClient(GameClientInterface):
    def __init__(self) -> None:
        self._session = httpx.Client(base_url=str(settings.game_api))

    def new_message_from_user(self, message: str, username: str) -> None:
        response = self._session.post(
            "/message",
            content=MessageEvent(message=message, username=username).model_dump_json(),
            timeout=3,
        )
        response.raise_for_status()
