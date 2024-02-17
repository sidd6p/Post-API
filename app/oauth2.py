import os
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from . import schemas
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

load_dotenv()


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_at = datetime.utcnow() + timedelta(
        minutes=int(os.getenv("EXPIRATION_TIME_IN_MINUTE"))
    )
    to_encode["expires_at"] = str(expires_at)
    encoded_jwt = jwt.encode(
        claims=to_encode, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


def verify_access_toke(token: str):
    try:
        payload = jwt.decode(
            token=token,
            key=os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
        )
        id: str = payload.get("id")

        if id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot validate the access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            token_data = schemas.TokenDataBase(id=id)
            return token_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot validate the access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_schema)):
    return verify_access_toke(token)
