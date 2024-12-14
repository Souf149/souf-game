class GameClientInterface:
    def new_message_from_user(self, message: str, username: str) -> None:
        raise NotImplementedError()
