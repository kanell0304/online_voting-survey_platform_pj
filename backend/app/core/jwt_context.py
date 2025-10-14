from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from backend.app.core.settings import settings
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

#bcrypt ???댁떆 ?뚭퀬由ъ쬁 以??덉젙?깆씠 ?믪??? ?⑥뒪?뚮뱶 ??μ뿉 留롮씠 ?대떎
pwd_context=CryptContext(schemes=["bcrypt"])

#?댁떆媛????
async def get_pwd_hash(password:str):
    return pwd_context.hash(password)

#鍮꾨쾲 寃利??낅젰??鍮꾨쾲怨? db????λ맂 ?댁떆媛?鍮꾨쾲 媛숈쑝硫?true)
async def verify_pwd(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def create_token(uid: int, expires_delta: timedelta, **kwargs) -> str:
    to_encode = kwargs.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "uid": uid})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_algo
    )
    return encoded_jwt


def create_access_token(uid: int) -> str:
    return create_token(uid=uid, expires_delta=settings.access_token_expire)


def create_refresh_token(uid: int) -> str:
    return create_token(
        uid=uid, jti=str(uuid.uuid4()), expires_delta=settings.refresh_token_expire
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.jwt_algo],
    )


def verify_token(token: str) -> int:
    payload = decode_token(token)
    return payload.get("uid")

