class DbClientInterface:
    def get_last_minute_users(self) -> list[str]:
        raise NotImplementedError()
