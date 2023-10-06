import datetime
from fastapi import status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from config.config import get_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign-in")


settings = get_settings()


def create_access_token(
    username: str
) -> str:
    jwt_data = {
        "sub": username,
        "exp": datetime.datetime.utcnow()+datetime.timedelta(minutes=settings.jwt_exp)
    }

    return jwt.encode(jwt_data, settings.jwt_secret, algorithm="HS256")


def jwt_decode(token: str):
    try:
        return jwt.decode(token, settings.jwt_secret, ["HS256"])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-authenticate": "bearer"})
