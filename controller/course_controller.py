from dateutil.utils import today
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
                                     Course.status >= constant.STATUS_INACTIVE)
                    ).filter(CourseDetail.status >= constant.STATUS_INACTIVE,
                             and_(CourseDetail.course_date >= before_date_filter,
                                  CourseDetail.course_date <= after_date_filter),
                    ).options(contains_eager(CourseDetail.course),
                    ).all()

    response.result_data = {
        'count': len(courses),
        'courses': course_details_schema.dump(courses),
    }
    return response


def post_course(request, session, g):
    response = DefaultModel()

    if g.type != constant.USER_TYPE_DANCER:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DANCER_ONLY][0],
                            detail=ERROR_DANCER_ONLY)

    _format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    today = datetime.strptime(now.strftime(_format), _format)

    course = Course()
    session.add(course)

    course.status = request.status
    course.user_id = g.id
    course.title = request.title
    course.description = request.description
    session.flush()

    for detail in request.detail_list:
        if today > datetime.strptime(detail.course_date, _format):
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_CREATED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_CREATED)

        course_detail = CourseDetail()
        session.add(course_detail)

        course_detail.course_id = course.id
        course_detail.title = detail.title
        course_detail.course_date = detail.course_date
        course_detail.start_time = detail.start_time
        course_detail.end_time = detail.end_time
        course_detail.address = detail.address
        course_detail.address_detail = detail.address_detail

    course.count = len(request.detail_list)
    course.last_course_date = request.detail_list[-1].course_date

    response.result_data = {
        'course_id': course.id
    }
    return response


def put_course_detail(course_id, request, session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    today = datetime.strptime(now.strftime(_format), _format)

    course = session.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    course.status = request.status
    course.user_id = g.id
    course.title = request.title
    course.description = request.description

    detail_query = session.query(CourseDetail
                        ).filter(CourseDetail.course_id == course_id,
                                 CourseDetail.status >= constant.STATUS_INACTIVE)
    detail_query.update({'status': constant.STATUS_DELETED}, synchronize_session=False)

    for detail in request.detail_list:
        if today > datetime.strptime(detail.course_date, _format):
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_CREATED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_CREATED)

        course_detail = CourseDetail()
        session.add(course_detail)

        course_detail.course_id = course.id
        course_detail.title = detail.title
        course_detail.course_date = detail.course_date
        course_detail.start_time = detail.start_time
        course_detail.end_time = detail.end_time
        course_detail.address = detail.address
        course_detail.address_detail = detail.address_detail

    course.count = len(request.detail_list)
    course.last_course_date = request.detail_list[-1].course_date

    response.result_data = {
        'course_id': course.id
    }
    return response


def get_course_detail(session, course_id, g):
    response = DefaultModel()

    date_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.strptime(datetime.now().strftime(date_format), date_format)

    filter_list = []
    course = session.query(Course).filter(Course.user_id == g.id).first()
    if course is None:
        if g.type == constant.USER_TYPE_MATE:
            filter_list.append(CourseDetail.course_date >= now)

    courses = session.query(Course
                    ).outerjoin(CourseDetail,
                                and_(CourseDetail.course_id == Course.id,
                                     CourseDetail.status == constant.STATUS_ACTIVE)
                    ).outerjoin(UserCourseLike,
                                and_(UserCourseLike.course_id == Course.id,
                                     UserCourseLike.user_id == g.id,
                                     UserCourseLike.status == constant.STATUS_ACTIVE)
                    ).filter(Course.status >= constant.STATUS_INACTIVE,
                             Course.id == course_id,
                             *filter_list,
                    ).options(contains_eager(Course.course_detail),
                              contains_eager(Course.course_like_user),
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


def post_course_detail_reserve(course_detail_id, request, session, g):
    response = DefaultModel()

    exists = session.query(UserCourse
                    ).filter(UserCourse.user_id == g.id,
                             UserCourse.course_detail_id == course_detail_id
                    ).first()
    if exists is not None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_COURSE_RESERVE_EXISTS][0],
                            detail=ERROR_COURSE_RESERVE_EXISTS)

    date_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.strptime(datetime.now().strftime(date_format), date_format)

    course_detail = session.query(CourseDetail).filter(CourseDetail.id == course_detail_id).first()
    if course_detail is not None:
        if course_detail.course_date < now:
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_RESERVED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_RESERVED)

    user_course = UserCourse()
    session.add(user_course)

    user_course.user_id = g.id
    user_course.user_ticket_id = request.user_ticket_id
    user_course.course_detail_id = course_detail_id

    user_ticket = session.query(UserTicket
                        ).filter(UserTicket.id == request.user_ticket_id
                        ).first()
    user_ticket.remain_count -= 1
    return response


def post_course_detail_cancel(course_detail_id, session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    now = datetime.strptime(datetime.now().strftime(_format), _format)

    user_course = session.query(UserCourse
                    ).filter(UserCourse.user_id == g.id,
                             UserCourse.course_detail_id == course_detail_id
                    ).first()
    if user_course is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    course_detail = session.query(CourseDetail).filter(CourseDetail.id == course_detail_id).first()
    if course_detail is not None:
        if course_detail.course_date < now:
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_CANCELED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_CANCELED)

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