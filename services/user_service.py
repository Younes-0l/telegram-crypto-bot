class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def get_or_create_user(self, telegram_id: int, username: str | None):
        user = self.user_repo.get_by_telegram_id(telegram_id)
        if user:
            return user, False
        user = self.user_repo.create(telegram_id=telegram_id, username=username)
        return user, True