from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_course(session, date):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.now().date()
    if date is None:
        before_date_filter = datetime.strptime(today.strftime(_format), _format)
        after_date_filter = datetime.strptime((today + timedelta(days=1)).strftime(_format), _format)
    else:
        before_date_filter = datetime.strptime(f'{date} 00:00:00', _format)
        after_date_filter = before_date_filter + timedelta(days=1)

    courses = session.query(CourseDetail
                    ).outerjoin(Course,
                                and_(CourseDetail.course_id == Course.id,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).filter(CourseDetail.status == constant.STATUS_ACTIVE,
                             and_(CourseDetail.course_date >= before_date_filter,
                                  CourseDetail.course_date <= after_date_filter),
                    ).options(contains_eager(CourseDetail.course),
                    ).all()

    response.result_data = {
        'count': len(courses),
        'courses': course_details_schema.dump(courses),
    }
    return response


def get_course_detail(session, course_id):
    response = DefaultModel()

    courses = session.query(Course
                    ).outerjoin(CourseDetail,
                                and_(CourseDetail.course_id == Course.id,
                                     CourseDetail.status == constant.STATUS_ACTIVE)
                    ).filter(Course.status >= constant.STATUS_INACTIVE,
                             Course.id == course_id
                    ).options(contains_eager(Course.course_detail),
                    ).all()

    response.result_data = {
        'course': course_schema.dump(courses[0]),
    }
    return response


def get_course_detail_reserve(session, course_detail_id, g):
    response = DefaultModel()

    date_format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(date_format), date_format)

    courses = session.query(Course
                    ).outerjoin(CourseDetail,
                                and_(CourseDetail.course_id == Course.id,
                                     CourseDetail.status == constant.STATUS_ACTIVE)
                    ).filter(CourseDetail.id == course_detail_id
                    ).options(contains_eager(Course.course_detail),
                    ).all()

    tickets = session.query(UserTicket
                    ).outerjoin(Ticket, UserTicket.ticket_id == Ticket.id,
                    ).outerjoin(User, UserTicket.user_id == User.id,
                    ).options(contains_eager(UserTicket.mate),
                              contains_eager(UserTicket.ticket),
                    ).filter(UserTicket.user_id == g.id,
                             UserTicket.status >= constant.STATUS_INACTIVE,
                             UserTicket.expired_date >= today,
                             Ticket.user_id == courses[0].user_id
                    ).all()

    response.result_data = {
        'course': course_schema.dump(courses[0]),
        'tickets': user_tickets_schema.dump(tickets),
    }
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
                    ).outerjoin(UserCourseLike, UserCourseLike.course_id == Course.id,
                    ).outerjoin(User, User.id == UserCourseLike.user_id,
                    ).filter(Course.status == constant.STATUS_ACTIVE,
                             UserCourseLike.user_id == g.id,
                             UserCourseLike.status == constant.STATUS_ACTIVE,
                    ).options(contains_eager(Course.course_like_user),
                              contains_eager(Course.course_like_user
                            ).contains_eager(UserCourseLike.user),
                    ).order_by(UserCourseLike.order.asc()).all()

    response.result_data = {
        'result_count': len(courses),
        'courses': course_list_schema.dump(courses),
    }
    return response