from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from fastapi import HTTPException

from database.models import *
from database.schema import *
from database.base_model import DefaultModel, DefaultLoginModel
from config.jwt_handler import JWT
from config.constant import *


def get_user(session, g):
    response = DefaultModel()

    user = session.query(User).outerjoin(UserCourse,
                                         and_(UserCourse.user_id == User.id,
                                              UserCourse.status >= constant.STATUS_INACTIVE)
                            ).outerjoin(CourseDetail,
                                        and_(CourseDetail.id == UserCourse.course_detail_id,
                                             CourseDetail.status == constant.STATUS_ACTIVE)
                            ).outerjoin(Course,
                                        and_(CourseDetail.course_id == Course.id,
                                             Course.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserTicket,
                                        and_(UserTicket.user_id == User.id,
                                             UserTicket.status >= constant.STATUS_INACTIVE)
                            ).options(contains_eager(User.mate_ticket),
                                      contains_eager(User.reserve_course),
                                      contains_eager(User.reserve_course).contains_eager(UserCourse.course_detail),
                                      contains_eager(User.reserve_course).contains_eager(UserCourse.course_detail),
                            ).filter(User.id == g.id).all()

    response.result_data = {
        'user': user_detail_schema.dump(user[0]),
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

    user_payload = user_payload_schema.dump(user)
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
            user.last_login_date = datetime.now()

            response.access_token = access_token
            response.refresh_token = refresh_token
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
                    ).order_by(UserTicket.created_at
                    ).all()

    result = []
    for user_ticket in user_tickets_schema.dump(tickets):
        if not list(filter(lambda e: user_ticket['created_at'] in e.keys(), result)):
            result.append({user_ticket['created_at']: []})

    for user_ticket in user_tickets_schema.dump(tickets):
        ticket = {
            'dancer_nickname': user_ticket['ticket']['dancer']['nickname'],
            'count': user_ticket['ticket']['count'],
            'print': user_ticket['ticket']['price']
        }
        list(filter(lambda e: user_ticket['created_at'] in e.keys(), result))[0][user_ticket['created_at']].append(ticket)

    response.result_data = {
        'result_count': len(tickets),
        'tickets': result,
    }
    return response
