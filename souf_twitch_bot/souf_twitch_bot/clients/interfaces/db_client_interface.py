class DbClientInterface:
    def new_message_from_user(self, user_id: str, username: str) -> None:
        raise NotImplementedError()
