from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    username: str
    password: str


class LoginUserRequest(RegisterUserRequest):
    ...


class RegisterUserResponse(BaseModel):
    id: int
