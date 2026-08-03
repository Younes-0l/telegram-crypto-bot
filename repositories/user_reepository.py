from database.models.users import User
from database.database import get_session
from sqlalchemy import select


class UserRepository:
     
    def create(self, telegram_id: int, full_name: str, username: str):

        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username
        )

        with get_session() as session:
            session.add(user)
            session.flush()
            return user

    def get_by_telegram_id(self, telegram_id: int):

        with get_session() as session:

                user = select(User).where(User.telegram_id == telegram_id)
                return session.scalar(user)

    def create_or_update(self, telegram_id: int, full_name: str, username: str | None):
        with get_session() as session:
            user = session.scalar(
                select(User).where(User.telegram_id == telegram_id)
            )

            if user is None:
                user = User(
                    telegram_id=telegram_id,
                    full_name=full_name,
                    username=username
                )
                session.add(user)
            else:
                user.full_name = full_name
                user.username = username

            session.commit()
            session.refresh(user)
            return user