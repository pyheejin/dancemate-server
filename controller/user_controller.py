from fastapi import HTTPException

from database.models import *
from database.schema import *
from database.base_model import DefaultModel, DefaultLoginModel
from config.jwt_handler import JWT
from config.constant import *


def get_user(session):
    response = DefaultModel()

    users = session.query(User).filter(User.status == 1).all()

    response.result_data = {
        'users': user_list_schema.dump(users),
    }
    return response


def get_user_detail(session, user_id):
    response = DefaultModel()

    user = session.query(User).filter(User.id == user_id).first()

    response.result_data = {
        'user': user_detail_schema.dump(user),
    }
    return response


def post_user_join(session, request):
    response = DefaultModel()

    jwt = JWT()

    exists = session.query(User).filter(User.email == request.email).first()
    if exists:
        raise HTTPException(status_code=ERROR_DIC[ERROR_EMAIL_EXISTS][0],
                            detail=ERROR_EMAIL_EXISTS)

    user = User()
    user.type = request.type
    user.email = request.email
    user.password = jwt.get_password_hash(request.password)
    user.nickname = request.nickname
    user.name = request.name
    user.phone = request.phone
    user.introduction = request.introduction

    session.add(user)
    session.flush()

    user_payload = user_detail_schema.dump(user)
    user.access_token = jwt.create_access_token(user_payload)
    user.refresh_token = jwt.create_refresh_token(user_payload)

    response.result_data = {
        'user': user_payload,
    }
    return response


def post_user_login(session, request):
    response = DefaultLoginModel()

    user = session.query(User).filter(User.email == request.username).first()
    if user is not None:
        jwt = JWT()
        verify = jwt.verify_password(request.password, user.password)
        if verify:
            access_token = jwt.create_access_token(token_payload_schema.dump(user))
            refresh_token = jwt.create_refresh_token(token_payload_schema.dump(user))

            user.access_token = access_token
            user.refresh_token = refresh_token

            response.access_token = access_token
            response.refresh_token = refresh_token
    return response