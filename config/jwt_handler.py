import jwt

from fastapi import HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext

from config.constant import *
from database.base_model import DefaultModel
from config.config import JWT_SECRET_KEY, JWT_ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWT:
    def __init__(self):
        self.ALGORITHM = JWT_ALGORITHM
        self.SECRET_KEY = JWT_SECRET_KEY

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def verify_password(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)

    def create_access_token(self, payloads: dict):
        expired_at = datetime.utcnow() + timedelta(days=7)
        payloads.update({'exp': expired_at,
                         'expired_at': (expired_at + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')})
        result = jwt.encode(payloads, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
        return result

    def create_refresh_token(self, payloads: dict):
        expired_at = datetime.utcnow() + timedelta(days=10)
        payloads.update({'exp': expired_at,
                         'expired_at': (expired_at + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')})
        result = jwt.encode(payloads, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
        return result
    
    def verify_token(self, token):
        response = DefaultModel()

        try:
            response.result_data = jwt.decode(token, key=self.SECRET_KEY, algorithms=self.ALGORITHM)
        except jwt.ExpiredSignatureError:
            # 토큰 인증 시간 만료
            raise HTTPException(status_code=ERROR_DIC[ERROR_TOKEN_EXPIRED][0],
                                detail=ERROR_DIC[ERROR_TOKEN_EXPIRED][1])
        except jwt.InvalidTokenError:
            # 토큰 검증 실패
            raise HTTPException(status_code=ERROR_DIC[ERROR_UNAUTHORIZED][0],
                                detail=ERROR_DIC[ERROR_UNAUTHORIZED][1])
        return response

