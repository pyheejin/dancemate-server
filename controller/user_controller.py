import requests

from sqlalchemy import and_, or_
from sqlalchemy.orm import contains_eager
from fastapi import HTTPException

from database.models import *
from database.schema import *
from database.base_model import DefaultModel, DefaultLoginModel
from config.jwt_handler import JWT
from config.constant import *
from config.s3 import *


def get_user_profile(session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(_format), _format)

    user = session.query(User).outerjoin(UserCourse,
                                         and_(UserCourse.user_id == User.id,
                                              UserCourse.status >= constant.STATUS_INACTIVE)
                            ).outerjoin(Course,
                                        and_(Course.id == UserCourse.course_id,
                                             Course.status == constant.STATUS_ACTIVE,
                                             Course.course_date >= today)
                            ).outerjoin(Lesson,
                                        and_(Course.lesson_id == Lesson.id,
                                             Lesson.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserTicket,
                                        and_(UserTicket.user_id == User.id,
                                             UserTicket.status >= constant.STATUS_INACTIVE,
                                             UserTicket.remain_count > 0,
                                             UserTicket.expired_date >= today)
                            ).filter(User.id == g.id,
                            ).options(contains_eager(User.mate_ticket),
                                      contains_eager(User.reserve_course),
                                      contains_eager(User.reserve_course
                                                     ).contains_eager(UserCourse.course),
                                      contains_eager(User.reserve_course
                                                     ).contains_eager(UserCourse.course
                                                    ).contains_eager(Course.lesson),
                            ).order_by(Course.course_date,
                                       UserTicket.expired_date,
                            ).all()

    response.result_data = {
        'user': user_profile_schema.dump(user[0]),
    }
    return response


def post_user_profile(session, request, g):
    response = DefaultModel()

    user = session.query(User).filter(User.id == g.id).first()
    if user is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    user.nickname = request.nickname
    user.introduction = request.introduction
    return response


def get_user_detail(session, g, user_id):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(_format), _format)

    if g.id == user_id:
        is_mine = True

        user = session.query(User
                    ).outerjoin(UserCourse,
                                and_(UserCourse.user_id == User.id,
                                     UserCourse.status >= constant.STATUS_INACTIVE)
                    ).outerjoin(Course,
                                and_(Course.id == UserCourse.course_id,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).outerjoin(Lesson,
                                and_(Course.lesson_id == Lesson.id,
                                     Lesson.status == constant.STATUS_ACTIVE)
                    ).outerjoin(UserTicket,
                                and_(UserTicket.user_id == User.id,
                                     UserTicket.status >= constant.STATUS_INACTIVE)
                    ).filter(User.id == g.id,
                             UserTicket.expired_date >= today,
                    ).options(contains_eager(User.mate_ticket),
                              contains_eager(User.reserve_course),
                              contains_eager(User.reserve_course
                                        ).contains_eager(UserCourse.course),
                              contains_eager(User.reserve_course
                                        ).contains_eager(UserCourse.course
                                        ).contains_eager(Course.lesson),
                    ).all()

        if len(user) > 0:
            user = user_profile_schema.dump(user[0])
    else:
        is_mine = False

        user = session.query(User
                    ).outerjoin(Ticket,
                                and_(Ticket.user_id == User.id,
                                     Ticket.status >= constant.STATUS_INACTIVE)
                    ).outerjoin(Lesson,
                                and_(Lesson.user_id == User.id,
                                     Lesson.last_course_date >= today,
                                     Lesson.status == constant.STATUS_ACTIVE)
                    ).outerjoin(Course,
                                and_(Course.lesson_id == Lesson.id,
                                     Course.course_date >= today,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).filter(User.id == user_id,
                    ).options(contains_eager(User.dancer_ticket),
                              contains_eager(User.dancer_lesson),
                              contains_eager(User.dancer_lesson
                                ).contains_eager(Lesson.course),
                    ).all()

        if len(user) > 0:
            user = user_detail_schema.dump(user[0])

    response.result_data = {
        'user': user,
        'is_mine': is_mine,
    }
    return response


def put_user_detail(session, request, g):
    response = DefaultModel()

    user = session.query(User).filter(User.id == g.id).first()
    if user is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    user.type = request.type
    if request.type == constant.USER_TYPE_DANCER:
        user.expired_day = 30
    user.name = request.name
    user.nickname = request.nickname
    user.phone = request.phone
    user.introduction = request.introduction
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
    user.method = request.method
    user.email = request.email
    user.password = jwt.get_password_hash(request.password)
    user.nickname = request.nickname
    user.name = request.name
    user.phone = request.phone
    user.introduction = request.introduction
    user.image_url = request.image_url
    user.apple_token = request.apple_token
    user.apple_identifier = request.apple_identifier
    user.fcm_token = request.fcm_token

    if request.type == constant.USER_TYPE_MATE:
        user.expired_day = 0
    else:
        user.expired_day = 30

    session.add(user)
    session.flush()

    user_payload = user_payload_schema.dump(user)
    user.access_token = jwt.create_access_token(user_payload)
    user.refresh_token = jwt.create_refresh_token(user_payload)

    # 알림
    notification = Notification()
    session.add(notification)

    notification.user_id = user.id
    notification.lesson = constant.STATUS_ACTIVE
    notification.ticket = constant.STATUS_ACTIVE
    notification.community = constant.STATUS_ACTIVE

    response.result_data = {
        'user': user_payload,
    }
    return response


def post_user_login(session, request):
    response = DefaultLoginModel()

    user = session.query(User).filter(or_(User.email == request.username,
                                          User.apple_identifier == request.username)).first()
    if user is not None:
        jwt = JWT()
        if user.method == constant.USER_METHOD_DEFAULT:
            verify = jwt.verify_password(request.password, user.password)
            if not verify:
                raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                                    detail=ERROR_DATA_NOT_EXIST)

        access_token = jwt.create_access_token(token_payload_schema.dump(user))
        refresh_token = jwt.create_refresh_token(token_payload_schema.dump(user))

        user.access_token = access_token
        user.refresh_token = refresh_token
        user.fcm_token = request.client_secret
        user.last_login_date = datetime.now()

        response.user_id = user.id
        response.type = user.type
        response.access_token = access_token
        response.refresh_token = refresh_token

    else:
        raise HTTPException(status_code=ERROR_DIC[ERROR_UNAUTHORIZED][0],
                            detail=ERROR_UNAUTHORIZED)
    return response


def get_user_ticket(dancer_id, session, g):
    response = DefaultModel()

    date_format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(date_format), date_format)

    filter_list = []
    if dancer_id is not None:
        if dancer_id > 0:
            filter_list.append(Ticket.user_id == dancer_id)

    tickets = session.query(UserTicket
                    ).outerjoin(Ticket, UserTicket.ticket_id == Ticket.id,
                    ).outerjoin(User, UserTicket.user_id == User.id,
                    ).options(contains_eager(UserTicket.mate),
                              contains_eager(UserTicket.ticket),
                    ).filter(UserTicket.user_id == g.id,
                             UserTicket.status >= constant.STATUS_INACTIVE,
                             UserTicket.expired_date >= today,
                             *filter_list,
                    ).order_by(UserTicket.created_at.desc()
                    ).all()

    result = []
    for user_ticket in user_tickets_schema.dump(tickets):
        if not next((e for e in result if e['date'] == user_ticket['created_at']), None):
            result.append({
                'date': user_ticket['created_at'],
                'ticket_list': [],
            })

    for user_ticket in user_tickets_schema.dump(tickets):
        if next((e for e in result if e['date'] == user_ticket['created_at']), None):
            ticket = {
                'dancer': {
                    'nickname': user_ticket['ticket']['dancer']['nickname'],
                    'email': user_ticket['ticket']['dancer']['email'],
                    'image_url': user_ticket['ticket']['dancer']['image_url'],
                },
                'count': f"{user_ticket['ticket']['count']}회권",
                'price': format(user_ticket['ticket']['price'], ',d'),
                'remain_count': user_ticket['remain_count'],
                'expired_date': user_ticket['expired_date'],
            }
            next((e for e in result if e['date'] == user_ticket['created_at']))['ticket_list'].append(ticket)

    response.result_data = {
        'result_count': len(tickets),
        'tickets': result,
    }
    return response


def get_user_course(session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(_format), _format)

    courses = session.query(Course
                    ).outerjoin(Lesson,
                                and_(Course.lesson_id == Lesson.id,
                                     Lesson.status == constant.STATUS_ACTIVE)
                    ).outerjoin(UserCourse,
                                and_(UserCourse.course_id == Course.id,
                                     UserCourse.status == constant.STATUS_ACTIVE)
                    ).outerjoin(Review,
                                and_(Review.user_course_id == UserCourse.id,
                                     Review.status == constant.STATUS_ACTIVE)
                    ).filter(UserCourse.user_id == g.id
                    ).options(contains_eager(Course.lesson),
                              contains_eager(Course.user_course),
                              contains_eager(Course.user_course).contains_eager(UserCourse.review),
                    ).order_by(Course.course_date.desc()
                    ).all()

    response.result_data = {
        'result_count': len(courses),
        'courses': courses_schema.dump(courses),
    }
    return response


def get_user_notification(session, g, page, pageSize):
    response = DefaultModel()

    notices = session.query(UserNotification
                    ).outerjoin(User,
                                and_(User.id == UserNotification.user_id,
                                     User.status == constant.STATUS_ACTIVE)
                    ).filter(User.id == g.id
                    ).options(contains_eager(UserNotification.user),
                    ).order_by(UserNotification.created_at.desc()
                    ).offset(pageSize * (page - 1)).limit(pageSize).all()

    result = []
    for user_notification in user_notification_schema.dump(notices):
        date = datetime.strptime(user_notification['created_at'], '%Y-%m-%d').date()
        today = datetime.today().date()

        if date == today:
            notice_date = '오늘'
        else:
            notice_date = date

        if not next((e for e in result if e['date'] == notice_date), None):
            result.append({
                'date': notice_date,
                'notification_list': [],
            })

    for user_notification in user_notification_schema.dump(notices):
        date = datetime.strptime(user_notification['created_at'], '%Y-%m-%d').date()
        today = datetime.today().date()

        if date == today:
            notice_date = '오늘'
        else:
            notice_date = date

        if next((e for e in result if e['date'] == notice_date), None):
            notification = {
                'id': user_notification['id'],
                'title': user_notification['title'],
                'description': user_notification['description'],
                'created_at': user_notification['created_at'],
            }
            next((e for e in result if e['date'] == notice_date))['notification_list'].append(notification)

    response.result_data = {
        'count': len(notices),
        'notices': result,
    }
    return response


def put_user_change_password(request, session):
    response = DefaultModel()

    email = request.email
    password = request.password
    password_again = request.password_again

    if password != password_again:
        raise HTTPException(status_code=ERROR_DIC[ERROR_UNAUTHORIZED][0],
                            detail='비밀번호가 일치하지 않습니다.')

    user = session.query(User).filter(User.status == constant.STATUS_ACTIVE,
                                      User.email == email).first()
    if user is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    jwt = JWT()
    user.password = jwt.get_password_hash(password)
    return response