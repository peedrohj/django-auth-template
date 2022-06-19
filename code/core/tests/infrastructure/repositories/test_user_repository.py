# Utils
import unittest
import datetime

# Entities
from core.domain.entities import ContentType, User, PermissionGroup, Permission

# Repositories
from core.infrastructure.db.in_memory.repositories import \
    InMemoryUserRepository


class TestUserRepository(unittest.TestCase):
    user_repo: InMemoryUserRepository

    def setUp(self) -> None:
        self.maxDiff = None
        self.user_repo = InMemoryUserRepository()
        self.permission = Permission(name="Test", codename="Test", content_type=ContentType(
            app_label="Test", model="Test"))
        self.group = PermissionGroup(
            name="Test", permissions=[self.permission])
        self.user_props = {
            "email": "teste@teste.com.br",
            "first_name": "Teste",
            "last_name": "1",
            "is_active": True,
            "is_superuser": False,
            "is_staff": False,
            "date_joined": datetime.datetime.now(),
            "permissions": [self.permission],
            "permissions_groups": [self.group],
        }
        self.user = User(**self.user_props)

    def test_insert_user(self):
        self.user_repo.insert(user=self.user)
        self.assertEqual(self.user_repo.db[0], self.user)

    def test_find_by_id(self):
        self.user_repo.insert(user=self.user)
        user = self.user_repo.find_by_id(
            user_id=self.user.id)
        self.assertEqual(user, self.user)

    def test_find_all(self):
        self.user_repo.insert(user=self.user)
        self.assertEqual(self.user_repo.db, [self.user])

    def test_update_user(self):
        user_props = {**self.user_props, "name": "Test 1"}
        expected_data = {**self.user.to_dict(), "name": "Test 1"}

        new_user = User(**user_props)
        self.user_repo.insert(user=self.user)
        self.user_repo.update(
            user_id=self.user.id, user=new_user)
        user = self.user_repo.find_by_id(
            user_id=self.user.id)

        self.assertEqual(
            user.to_dict(), expected_data)

    def test_delete_user(self):
        self.user_repo.insert(user=self.user)
        self.user_repo.delete(user_id=self.user.id)
        self.assertEqual(self.user_repo.db, [])
