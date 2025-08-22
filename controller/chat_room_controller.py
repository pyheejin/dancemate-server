from dateutil.utils import today
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_chat_room(type, session, g):
    response = DefaultModel()

    chat_room_ids = []
    chat_room_id_query = session.query(ChatRoom
                                ).outerjoin(ChatRoomUser,
                                            and_(ChatRoomUser.chat_room_id == ChatRoom.id,
                                                 ChatRoomUser.status == constant.STATUS_ACTIVE)
                                ).outerjoin(User,
                                            and_(ChatRoomUser.user_id == User.id,
                                                 User.status == constant.STATUS_ACTIVE)
                                ).filter(ChatRoom.status == constant.STATUS_ACTIVE,
                                         ChatRoom.type == type,
                                         ChatRoom.user_id == g.id,
                                ).options(contains_eager(ChatRoom.chat_room_user),
                                          contains_eager(ChatRoom.chat_room_user
                                                         ).contains_eager(ChatRoomUser.user),
                                ).all()

    for room in chat_room_id_query:
        chat_room_ids.append(room.id)

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
                        ).outerjoin(ChatRoomNotification,
                                    and_(ChatRoomNotification.chat_room_id == ChatRoom.id,
                                         ChatRoomNotification.user_id == g.id,
                                         ChatRoomUser.status == constant.STATUS_ACTIVE)
                        ).outerjoin(User,
                                    and_(ChatRoomUser.user_id == User.id,
                                         User.status == constant.STATUS_ACTIVE)
                        ).filter(ChatRoom.id.in_(chat_room_ids),
                        ).options(contains_eager(ChatRoom.lesson),
                                  contains_eager(ChatRoom.chat),
                                  contains_eager(ChatRoom.chat_room_user),
                                  contains_eager(ChatRoom.chat_room_user
                                                 ).contains_eager(ChatRoomUser.user),
                                  contains_eager(ChatRoom.room_notification),
                        ).order_by(Chat.type.asc(),
                                   Chat.id.desc(),
                        ).all()

    response.result_data = {
        'count': len(chat_rooms),
        'chat_rooms': chat_rooms_schema.dump(chat_rooms),
        'login_user_id': g.id,
    }
    return response


def post_chat_room(request, session, g):
    response = DefaultModel()

    room_exists = session.query(ChatRoomUser
                            ).filter(ChatRoomUser.user_id == request.user_id,
                                     ChatRoomUser.user_id == g.id).first()
    if room_exists is None:
        # 초대 받은 유저
        invited_user = session.query(User).filter(User.id == request.user_id).first()
        if invited_user is None:
            raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                                detail=ERROR_DATA_NOT_EXIST)

        chat_room = ChatRoom()
        session.add(chat_room)

        chat_room.type = 1
        chat_room.user_id = g.id
        chat_room.friend_id = request.user_id
        session.flush()

        # 방장
        room_user = ChatRoomUser()
        session.add(room_user)

        room_user.is_notice = 1
        room_user.chat_room_id = chat_room.id
        room_user.user_id = g.id

        # 초대 메시지
        chat = Chat()
        session.add(chat)

        chat.type = 99
        chat.chat_room_id = chat_room.id
        chat.user_id = g.id
        chat.message = f'{g.nickname}님이 {invited_user.nickname}님을 초대했습니다.'

        # 초대 받은 유저
        room_user = ChatRoomUser()
        session.add(room_user)

        room_user.is_notice = 1
        room_user.chat_room_id = chat_room.id
        room_user.user_id = invited_user.id

        response.result_data = {
            'chat_room': chat_room_schema.dump(chat_room),
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


def put_chat_room_detail(chat_room_id, session, g):
    response = DefaultModel()

    chat_room = session.query(ChatRoom).filter(ChatRoom.id == chat_room_id).first()
    if chat_room is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    room_user = session.query(ChatRoomUser).filter(ChatRoomUser.chat_room_id == chat_room_id,
                                                   ChatRoomUser.user_id == g.id).first()
    if room_user is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    if room_user.is_notice == 1:
        is_notice = 0
    else:
        is_notice = 1

    room_user.is_notice = is_notice
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
                        ).order_by(Chat.created_at.desc(),
                                   Chat.type.asc(),
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
                    'type': data['type'],
                }
                next((e for e in result if e['date'] == data['created_at'].split(' ')[0]))['chat_list'].append(chat)

    # 채팅방 확인
    room_notification = session.query(ChatRoomNotification
                            ).filter(ChatRoomNotification.chat_room_id == chat_room_id,
                                     ChatRoomNotification.user_id == g.id).first()
    if room_notification is not None:
        room_notification.status = constant.STATUS_ACTIVE
    else:
        room_notification = ChatRoomNotification()
        session.add(room_notification)

        room_notification.chat_room_id = chat_room_id
        room_notification.user_id = g.id
        room_notification.status = constant.STATUS_ACTIVE

    is_notice = 0
    for user in chat_room.chat_room_user:
        if user.user_id == g.id:
            is_notice = user.is_notice

    if chat_room.type == 50:
        course_users = session.query(UserCourse
                            ).outerjoin(User,
                                        and_(UserCourse.user_id == User.id,
                                             User.status == constant.STATUS_ACTIVE)
                            ).outerjoin(Course,
                                        and_(UserCourse.course_id == Course.id,
                                             Course.status == constant.STATUS_ACTIVE)
                            ).outerjoin(Lesson,
                                        and_(Course.lesson_id == Lesson.id,
                                             Course.status == constant.STATUS_ACTIVE)
                            ).filter(Lesson.id == chat_room.lesson_id
                            ).options(contains_eager(UserCourse.user),
                                      contains_eager(UserCourse.course),
                                      contains_eager(UserCourse.course
                                            ).contains_eager(Course.lesson),
                            ).group_by(UserCourse.user_id,
                            ).all()
        users = lesson_reserve_users_schema.dump(course_users)
        dancer = user_schema.dump(chat_room.lesson.dancer)
    else:
        users = None
        dancer = None

    response.result_data = {
        'chat_room': chat_room_schema.dump(chat_room),
        'chats': result,
        'chat_room_user_count': len(chat_room.chat_room_user),
        'lesson': simple_lesson_schema.dump(chat_room.lesson),
        'is_notice': is_notice,
        'login_user_id': g.id,
        'dancer': dancer,
        'reserve_users': users,
    }
    return response


def delete_chat_room_detail(chat_room_id, session, g):
    response = DefaultModel()

    chat_room = session.query(ChatRoom
                        ).filter(ChatRoom.id == chat_room_id).first()
    if chat_room is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    room_user_query = session.query(ChatRoomUser
                            ).filter(ChatRoomUser.chat_room_id == chat_room_id,
                                     ChatRoomUser.status >= constant.STATUS_INACTIVE)

    # 1:DM, 50:수업톡
    if chat_room.type == 1:
        if len(room_user_query.all()) <= 1:  # 유저가 전부 나가면 채팅방 삭제
            chat_room.status = constant.STATUS_DELETED

        room_user = room_user_query.filter(ChatRoomUser.user_id == g.id).first()
        if room_user is None:
            raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                                detail=ERROR_DATA_NOT_EXIST)

        room_user.status = constant.STATUS_DELETED

        # 퇴장 메시지
        chat = Chat()
        session.add(chat)

        chat.type = 99
        chat.chat_room_id = chat_room.id
        chat.user_id = g.id
        chat.message = f'{g.nickname}님이 퇴장했습니다.'
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

    # 채팅방 알림
    room_notification_query = session.query(ChatRoomNotification
                                    ).filter(ChatRoomNotification.chat_room_id == chat_room_id,
                                             ChatRoomNotification.user_id != g.id)
    room_notification_query.update({'status': constant.STATUS_INACTIVE}, synchronize_session=False)
    return response


def post_chat_room_detail_check(chat_room_id, session, g):
    response = DefaultModel()

    chat_room = session.query(ChatRoom
                        ).filter(ChatRoom.id == chat_room_id,
                                 ChatRoom.status == constant.STATUS_ACTIVE).first()
    if chat_room is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)


    return response