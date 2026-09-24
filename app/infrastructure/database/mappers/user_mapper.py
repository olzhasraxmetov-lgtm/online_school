from uuid import UUID

from app.domain.entities.user import User, UserRole
from app.infrastructure.database.models.user_model import UserModel


class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=UUID(model.id),
            email=model.email,
            hashed_password=model.hashed_password,
            role=UserRole(model.role),
            full_name=model.full_name,
            bio=model.bio,
            avatar_url=model.avatar_url,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=str(entity.id),
            email=entity.email,
            hashed_password=entity.hashed_password,
            role=str(entity.role),
            full_name=entity.full_name,
            bio=entity.bio,
            avatar_url=entity.avatar_url,
        )