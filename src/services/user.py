from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from dto.user import LoginUserRequest, RegisterUserRequest
from entities.user import User
from repositories.user import UserRepo
from security.hash import hash_password, verify_password
from security.jwt import create_access_token, jwt_decode


class UserService:
    user_repo: UserRepo

    def __init__(self, user_repo: Annotated[UserRepo, Depends()]) -> None:
        self.user_repo = user_repo

    async def add(self, user: RegisterUserRequest):
        try:
            user_data = user.model_dump()
            user_data['hashed_password'] = hash_password(
                user_data.pop('password'))
            return await self.user_repo.add(user_data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username's already taken")

    async def authenticate_user(self, user: LoginUserRequest):
        user_to_auth = await self.get_user_by_username(user.username)
        if not user_to_auth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-authenticate": "bearer"})
        if not verify_password(user.password, user_to_auth.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-authenticate": "bearer"})

        token = create_access_token(user_to_auth.username)
        return {"access_token": token, "token_type": "bearer"}

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repo.get_by_value(username=username)

    async def get_current_user(self, token: str):
        payload = jwt_decode(token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-authenticate": "bearer"})
        user = await self.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-authenticate": "bearer"})
        return user
