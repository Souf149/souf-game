class DbClientInterface:
    def new_message_from_user(self, user_id: str) -> None:
        raise NotImplementedError()
