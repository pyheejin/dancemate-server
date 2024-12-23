from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config.constant import *
from config.jwt_handler import JWT
from database.database import db
from database.models import User
from database.base_model import DefaultModel


def error_response(response: DefaultModel,
                   error_msg: str,
                   error_code: int,
                   result_msg: str):
    if response is None:
        response = DefaultModel()

    if error_msg is None:
        return
    print(ERROR_DIC[error_msg])

    response.result_data = {}
    if error_msg in ERROR_DIC.keys():
        response.result_code = ERROR_DIC[error_msg][0]
        response.result_msg = f'[{result_msg} 실패] {ERROR_DIC[error_msg][1]}'
    else:
        response.result_code = error_code
        response.result_msg = f'[{result_msg} 실패] {error_msg}'
    return response


oauth = OAuth2PasswordBearer(
    tokenUrl='/api/v1/user/login',
    scheme_name='JWT',
)


async def get_current_user(token: str = Depends(oauth)) -> User:
    jwt = JWT()
    token_data = jwt.verify_token(token)

    with Session(bind=db.engine) as session:
        user = session.query(User).filter(User.id == token_data.result_data.get('id')).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Could not find user',
            )
        session.close()
        return user
    return None