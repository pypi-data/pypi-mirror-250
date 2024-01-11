# coding:utf-8
"""
Name : __init__.py.py
Author : lvyunze
Time : 2022/5/11 17:23
Desc : fastapi jwt
"""
import jwt
from typing import Any, Dict
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

__all__ = [
    "JwtAuthorizationCredentials",
    "AuthHandler",
]


class JwtAuthorizationCredentials:
    def __init__(self, subject: Dict[str, Any]):
        self.subject = subject

    def __getitem__(self, item: str) -> Any:
        return self.subject[item]


class AuthHandler(object):
    security = HTTPBearer()

    def __int__(self, secret: str = 'SECRET'):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret = secret

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, subject: str, exp_day: int = 0, exp_hours: int = 2) -> dict:
        exp = datetime.now() + timedelta(days=exp_day, hours=exp_hours)
        iat = datetime.now()
        payload = {
            'exp': exp,
            'iat': iat,
            'sub': subject
        }
        return {
            'token': jwt.encode(
                payload,
                self.secret,
                algorithm='HS256'
            ),
            'iat': iat.strftime('%Y-%m-%d %H:%M:%S'),
            'exp': exp.strftime('%Y-%m-%d %H:%M:%S')
        }

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=402, detail='Invalid token')

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return
        except jwt.InvalidTokenError as e:
            return

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
