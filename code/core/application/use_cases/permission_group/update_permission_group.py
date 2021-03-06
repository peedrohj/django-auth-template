# Utils
from dataclasses import dataclass

# Entities
from core.domain.entities import User
from core.domain.value_objects.unique_entity_id import UniqueEntityId

# Repositories
from core.domain.repositories import UserRepository

# Exceptions
from core.domain.exceptions import InvalidUUidException


@dataclass(slots=True)
class UpdateUser:
    user_repository: UserRepository

    def execute(self, user_id: str | UniqueEntityId, user: User) -> User:
        if not user_id:
            raise InvalidUUidException()

        return self.user_repository.update(user_id=user_id, user=user)
