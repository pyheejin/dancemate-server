from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

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
