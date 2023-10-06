from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from dto.user import RegisterUserRequest, RegisterUserResponse
from services.user import UserService
from security.jwt import oauth2_scheme


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/sign-up', status_code=status.HTTP_201_CREATED)
async def sign_up(
    user: RegisterUserRequest,
    user_service: Annotated[UserService, Depends()]
) -> RegisterUserResponse:
    user_id = await user_service.add(user)
    return RegisterUserResponse(id=user_id)


@router.post('/sign-in', status_code=status.HTTP_200_OK)
async def sign_in(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends()]
):
    token = await user_service.authenticate_user(user)
    return token


@router.get('/me')
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends()]
):
    user = await user_service.get_current_user(token)
    return {"username": user.username}
