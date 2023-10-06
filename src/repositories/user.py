from repositories.base import BaseRepo
from entities import User


class UserRepo(BaseRepo):
    model = User
