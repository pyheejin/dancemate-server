from dateutil.utils import today
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel
from config.smtp_handler import SMTP


def get_chat_room(session, g):
    response = DefaultModel()

    chat_rooms = session.query(ChatRoom
                        ).outerjoin(Lesson,
                                     and_(ChatRoom.lesson_id == Lesson.id,
                                          ChatRoom.status == constant.STATUS_ACTIVE)
                        ).outerjoin(Chat,
                                     and_(Chat.chat_room_id == ChatRoom.id,
                                          Chat.status == constant.STATUS_ACTIVE)
                        ).outerjoin(ChatRoomUser,
                                     and_(ChatRoomUser.chat_room_id == ChatRoom.id,
                                          ChatRoomUser.status == constant.STATUS_ACTIVE)
                        ).outerjoin(User,
                                     and_(ChatRoomUser.user_id == User.id,
                                          User.status == constant.STATUS_ACTIVE)
                        ).filter(ChatRoom.status == constant.STATUS_ACTIVE,
                                 ChatRoomUser.user_id == g.id,
                        ).options(contains_eager(ChatRoom.lesson),
                                  contains_eager(ChatRoom.chat),
                                  contains_eager(ChatRoom.chat_room_user),
                                  contains_eager(ChatRoom.chat_room_user).contains_eager(ChatRoomUser.user),
                        ).order_by(Chat.created_at.desc()
                        ).all()

    response.result_data = {
        'count': len(chat_rooms),
        'chat_rooms': chat_rooms_schema.dump(chat_rooms),
    }
    return response


def get_chat_room_dancer(session, g):
    response = DefaultModel()

    chat_rooms = session.query(ChatRoom
                        ).outerjoin(Lesson,
                                     and_(ChatRoom.lesson_id == Lesson.id,
                                          ChatRoom.status == constant.STATUS_ACTIVE)
                        ).outerjoin(Chat,
                                     and_(Chat.chat_room_id == ChatRoom.id,
                                          Chat.status == constant.STATUS_ACTIVE)
                        ).outerjoin(ChatRoomUser,
                                     and_(ChatRoomUser.chat_room_id == ChatRoom.id,
                                          ChatRoomUser.status == constant.STATUS_ACTIVE)
                        ).outerjoin(User,
                                     and_(ChatRoomUser.user_id == User.id,
                                          User.status == constant.STATUS_ACTIVE)
                        ).filter(ChatRoom.status == constant.STATUS_ACTIVE,
                                 ChatRoom.user_id == g.id,
                        ).options(contains_eager(ChatRoom.lesson),
                                  contains_eager(ChatRoom.chat),
                                  contains_eager(ChatRoom.chat_room_user),
                                  contains_eager(ChatRoom.chat_room_user).contains_eager(ChatRoomUser.user),
                        ).order_by(Chat.created_at.desc()
                        ).all()

    response.result_data = {
        'count': len(chat_rooms),
        'chat_rooms': chat_rooms_schema.dump(chat_rooms),
    }
    return response


def put_chat_room_detail(chat_room_id, request, session):
    response = DefaultModel()

    chat_room = session.query(ChatRoom).filter(ChatRoom.id == chat_room_id).first()
    if chat_room is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    chat_room.question = request.question
    return response


def get_chat_room_detail(session, chat_room_id, g):
    response = DefaultModel()

    chat_room = session.query(ChatRoom
                        ).outerjoin(Lesson,
                                     and_(ChatRoom.lesson_id == Lesson.id,
                                          ChatRoom.status == constant.STATUS_ACTIVE)
                        ).outerjoin(Chat,
                                     and_(Chat.chat_room_id == ChatRoom.id,
                                          Chat.status == constant.STATUS_ACTIVE)
                        ).outerjoin(ChatRoomUser,
                                     and_(ChatRoomUser.chat_room_id == ChatRoom.id,
                                          ChatRoomUser.status == constant.STATUS_ACTIVE)
                        ).outerjoin(User,
                                     and_(ChatRoomUser.user_id == User.id,
                                          User.status == constant.STATUS_ACTIVE)
                        ).filter(ChatRoom.status == constant.STATUS_ACTIVE,
                                 ChatRoom.id == chat_room_id,
                        ).options(contains_eager(ChatRoom.lesson),
                                  contains_eager(ChatRoom.chat),
                                  contains_eager(ChatRoom.chat_room_user),
                                  contains_eager(ChatRoom.chat_room_user).contains_eager(ChatRoomUser.user),
                        ).order_by(Chat.created_at.desc()
                        ).all()
    if len(chat_room) == 0:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    chat_room = chat_room[0]

    result = []
    for data in chat_room_schema.dump(chat_room)['chat']:
        if not next((e for e in result if e['date'] == data['created_at'].split(' ')[0]), None):
            result.append({
                'date': data['created_at'].split(' ')[0],
                'chat_list': [],
            })

    for data in chat_room_schema.dump(chat_room)['chat']:
        if next((e for e in result if e['date'] == data['created_at'].split(' ')[0]), None):
            user = session.query(User).filter(User.id == data['user_id']).first()
            if user is not None:
                chat = {
                    'created_at': data['created_at'],
                    'id': data['id'],
                    'message': data['message'],
                    'status': data['status'],
                    'login_user_id': g.id,
                    'user': user_schema.dump(user),
                }
                next((e for e in result if e['date'] == data['created_at'].split(' ')[0]))['chat_list'].append(chat)

    response.result_data = {
        'chat_room': result,
        'chat_room_user_count': len(chat_room.chat_room_user),
        'lesson': simple_lesson_schema.dump(chat_room.lesson),
    }
    return response


def delete_chat_room_detail(chat_room_id, session, g):
    response = DefaultModel()

    chat_room = session.query(ChatRoom).filter(ChatRoom.id == chat_room_id,
                                               ChatRoom.user_id == g.id).first()
    if chat_room is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    chat_room.status = constant.STATUS_DELETED
    return response


def post_chat_room_detail_chat(chat_room_id, request, session, g):
    response = DefaultModel()

    chat_room = session.query(ChatRoom
                        ).filter(ChatRoom.id == chat_room_id,
                                 ChatRoom.status == constant.STATUS_ACTIVE).first()
    if chat_room is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    chat = Chat()
    session.add(chat)

    chat.chat_room_id = chat_room_id
    chat.user_id = g.id
    chat.message = request.message
    return response