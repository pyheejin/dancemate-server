from dateutil.utils import today
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_course_detail(course_id, session):
    response = DefaultModel()

    course = session.query(Course
                    ).outerjoin(Lesson,
                                and_(Course.lesson_id == Lesson.id,
                                     Lesson.status >= constant.STATUS_INACTIVE)
                    ).filter(Course.status >= constant.STATUS_INACTIVE,
                             Course.id == course_id,
                    ).options(contains_eager(Course.lesson),
                    ).first()

    if course is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    response.result_data = {
        'course': course_schema.dump(course),
    }
    return response


def get_course_detail_reserve(session, course_id, g):
    response = DefaultModel()

    date_format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(date_format), date_format)

    lessons = session.query(Lesson
                    ).outerjoin(Course,
                                and_(Course.lesson_id == Lesson.id,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).filter(Course.id == course_id
                    ).options(contains_eager(Lesson.course),
                    ).all()

    if len(lessons) == 0:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    lesson = lessons[0]

    tickets = session.query(UserTicket
                    ).outerjoin(Ticket, UserTicket.ticket_id == Ticket.id,
                    ).outerjoin(User, UserTicket.user_id == User.id,
                    ).options(contains_eager(UserTicket.mate),
                              contains_eager(UserTicket.ticket),
                    ).filter(UserTicket.user_id == g.id,
                             UserTicket.status >= constant.STATUS_INACTIVE,
                             UserTicket.expired_date >= today,
                             Ticket.user_id == lesson.user_id
                    ).all()

    response.result_data = {
        'lesson': lesson_schema.dump(lesson),
        'tickets': user_tickets_schema.dump(tickets),
    }
    return response


def post_course_detail_reserve(course_id, request, session, g):
    response = DefaultModel()

    exists = session.query(UserCourse
                    ).filter(UserCourse.user_id == g.id,
                             UserCourse.course_id == course_id
                    ).first()
    if exists is not None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_COURSE_RESERVE_EXISTS][0],
                            detail=ERROR_COURSE_RESERVE_EXISTS)

    date_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.strptime(datetime.now().strftime(date_format), date_format)

    course_detail = session.query(Course).filter(Course.id == course_id).first()
    if course_detail is not None:
        if course_detail.lesson.user_id == g.id:
            raise HTTPException(status_code=ERROR_DIC[ERROR_COURSE_RESERVE_EXISTS][0],
                                detail=ERROR_COURSE_RESERVE_EXISTS)

        course_date = f'{course_detail.course_date.date()} {course_detail.start_time}:00'
        if datetime.strptime(course_date, date_format) < now:
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_RESERVED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_RESERVED)

    user_course = UserCourse()
    session.add(user_course)

    user_course.user_id = g.id
    user_course.user_ticket_id = request.user_ticket_id
    user_course.course_id = course_id

    user_ticket = session.query(UserTicket
                        ).filter(UserTicket.id == request.user_ticket_id
                        ).first()
    user_ticket.remain_count -= 1
    return response


def post_course_detail_cancel(course_id, session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    now = datetime.strptime(datetime.now().strftime(_format), _format)

    user_course = session.query(UserCourse
                    ).filter(UserCourse.user_id == g.id,
                             UserCourse.course_id == course_id
                    ).first()
    if user_course is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    course_detail = session.query(Course).filter(Course.id == course_id).first()
    if course_detail is not None:
        course_date = f'{course_detail.course_date.date()} {course_detail.start_time}:00'
        if datetime.strptime(course_date, _format) < now:
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_RESERVED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_RESERVED)

    user_course.status = constant.STATUS_DELETED

    user_ticket = session.query(UserTicket
                        ).filter(UserTicket.id == user_course.user_ticket_id
                        ).first()
    user_ticket.remain_count += 1
    return response


def post_course_detail_like(session, course_id, g):
    response = DefaultModel()

    course = session.query(Course
                    ).filter(Course.id == course_id,
                             Course.status == constant.STATUS_ACTIVE).first()
    if course is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    like_course_query = session.query(UserCourseLike
                                ).filter(UserCourseLike.user_id == g.id,
                                         UserCourseLike.status == constant.STATUS_ACTIVE)
    # 처음 찜한 경우
    exists = like_course_query.filter(UserCourseLike.course_id == course_id).first()
    if exists is None:
        # 순서
        like_course_list = like_course_query.all()

        user_course_like = UserCourseLike()
        user_course_like.order = len(like_course_list) + 1
        user_course_like.user_id = g.id
        user_course_like.course_id = course_id

        session.add(user_course_like)
    else:  # 이미 찜한 경우
        exists.status = constant.STATUS_DELETED

        # 순서 조정
        order_query = like_course_query.filter(UserCourseLike.order > exists.order
                                    ).order_by(UserCourseLike.order.asc()).all()
        for like_course in order_query:
            like_course.order -= 1

    session.flush()
    return response


def get_course_like(session, g):
    response = DefaultModel()

    courses = session.query(Course
                    ).outerjoin(Lesson, Lesson.id == Course.lesson_id,
                    ).outerjoin(UserCourseLike, UserCourseLike.course_id == Course.id,
                    ).outerjoin(User, User.id == UserCourseLike.user_id,
                    ).filter(Course.status == constant.STATUS_ACTIVE,
                             UserCourseLike.user_id == g.id,
                             UserCourseLike.status == constant.STATUS_ACTIVE,
                    ).options(contains_eager(Course.lesson),
                              contains_eager(Course.like_user),
                              contains_eager(Course.like_user
                            ).contains_eager(UserCourseLike.user),
                    ).order_by(UserCourseLike.order.asc()).all()

    response.result_data = {
        'result_count': len(courses),
        'courses': courses_schema.dump(courses),
    }
    return response


def post_course_detail_exists(course_id, session, g):
    response = DefaultModel()

    # 이미 예약한 수업일 경우
    exists = session.query(UserCourse
                    ).filter(UserCourse.user_id == g.id,
                             UserCourse.course_id == course_id
                    ).first()
    if exists is not None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_COURSE_RESERVE_EXISTS][0],
                            detail=ERROR_COURSE_RESERVE_EXISTS)

    # 날짜가 지난 회차일 경우
    _format = '%Y-%m-%d %H:%M:%S'
    now = datetime.strptime(datetime.now().strftime(_format), _format)

    course_detail = session.query(Course).filter(Course.id == course_id).first()
    if course_detail is not None:
        if course_detail.lesson.user_id == g.id:
            raise HTTPException(status_code=ERROR_DIC[ERROR_COURSE_RESERVE_EXISTS][0],
                                detail=ERROR_COURSE_RESERVE_EXISTS)

        course_date = f'{course_detail.course_date.date()} {course_detail.start_time}:00'
        if datetime.strptime(course_date, _format) < now:
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_RESERVED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_RESERVED)

    # 내가 만든 수업일 경우
    my_lesson = session.query(Lesson).filter(Lesson.user_id == g.id,
                                             Lesson.id == course_detail.lesson_id).first()
    if my_lesson is not None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_MY_COURSE_IS_NOT_AVAILABLE_FOR_RESERVATION][0],
                            detail=ERROR_MY_COURSE_IS_NOT_AVAILABLE_FOR_RESERVATION)
    return response
