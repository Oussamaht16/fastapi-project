# had l file khas fa9at bi jwt token wa authentification
# pip install python-jose[cryptography]
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# SECRET KEY
# ALGORITHM
# EXPIRATION TIME

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)  # تحويل str إلى int
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
) -> models.Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data2 = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token_data2.id).first()

    return user
