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
                              contains_eager(CourseDetail.user_course_detail),
                    ).all()

    response.result_data = {
        'count': len(courses),
        'courses': course_detail_schema.dump(courses),
    }
    return response
