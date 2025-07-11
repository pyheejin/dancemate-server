from typing import Optional, List

from PIL.ImageChops import constant
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import chat_room_controller


router = APIRouter(
    prefix='/chat-room'
)


class PostChatRoomModel(BaseModel):
    user_id: int


class PostChatModel(BaseModel):
    message: str


@router.get('', tags=['chat_room'], summary='채팅방 목록', dependencies=[Depends(get_current_user)])
def get_chat_room(type: int,
                  session: Session = Depends(db.session),
                  g: User = Depends(get_current_user)):
    result_msg = '채팅방 목록'
    try:
        response = chat_room_controller.get_chat_room(type=type,
                                                      session=session,
                                                      g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.post('', tags=['chat_room'], summary='채팅방 생성', dependencies=[Depends(get_current_user)])
def post_chat_room(request: PostChatRoomModel,
                   session: Session = Depends(db.session),
                   g: User = Depends(get_current_user)):
    result_msg = '채팅방 생성'
    try:
        response = chat_room_controller.post_chat_room(request=request,
                                                       session=session,
                                                       g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.get('/dancer', tags=['chat_room'], summary='댄서 채팅방 목록', dependencies=[Depends(get_current_user)])
def get_chat_room_dancer(session: Session = Depends(db.session),
                         g: User = Depends(get_current_user)):
    result_msg = '댄서 채팅방 목록'
    try:
        response = chat_room_controller.get_chat_room_dancer(session=session,
                                                             g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.put('/{chat_room_id}', tags=['chat_room'], summary='채팅방 수정', dependencies=[Depends(get_current_user)])
def put_chat_room_detail(chat_room_id: int,
                         session: Session = Depends(db.session),
                         g: User = Depends(get_current_user)):
    result_msg = '채팅방 수정'
    try:
        response = chat_room_controller.put_chat_room_detail(chat_room_id=chat_room_id,
                                                             session=session,
                                                             g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.get('/{chat_room_id}', tags=['chat_room'], summary='채팅방 상세', dependencies=[Depends(get_current_user)])
def get_chat_room_detail(chat_room_id: int,
                         session: Session = Depends(db.session),
                         g: User = Depends(get_current_user)):
    result_msg = '채팅방 상세'
    try:
        response = chat_room_controller.get_chat_room_detail(chat_room_id=chat_room_id,
                                                             session=session,
                                                             g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.delete('/{chat_room_id}', tags=['chat_room'], summary='채팅방 삭제', dependencies=[Depends(get_current_user)])
def delete_chat_room_detail(chat_room_id: int,
                            session: Session = Depends(db.session),
                            g: User = Depends(get_current_user)):
    result_msg = '채팅방 삭제'
    try:
        response = chat_room_controller.delete_chat_room_detail(chat_room_id=chat_room_id,
                                                                session=session,
                                                                g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.post('/{chat_room_id}/chat', tags=['chat_room'], summary='채팅', dependencies=[Depends(get_current_user)])
def post_chat_room_detail_chat(chat_room_id: int,
                               request: PostChatModel,
                               session: Session = Depends(db.session),
                               g: User = Depends(get_current_user)):
    result_msg = '채팅'
    try:
        response = chat_room_controller.post_chat_room_detail_chat(chat_room_id=chat_room_id,
                                                                   request=request,
                                                                   session=session,
                                                                   g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response
