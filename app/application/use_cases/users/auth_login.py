from dataclasses import dataclass

from app.application.exceptions import InvalidCredentialsError
from app.application.interfaces.services.password_hasher import PasswordHasher
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.user import User

@dataclass
class LoginUserCommand:
    email: str
    password: str

class LoginUserUseCase:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, command: LoginUserCommand) -> User:
        async with self.uow:
            user = await self.uow.users.get_by_email(command.email)
            if not user:
                raise InvalidCredentialsError("Invalid email or password")

            is_valid_password = self.password_hasher.verify(
                command.password,
                user.hashed_password
            )
            if not is_valid_password:
                raise InvalidCredentialsError("Invalid email or password")
            return user