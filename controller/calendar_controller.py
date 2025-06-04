from dateutil.utils import today
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_calendar_lesson(session, month):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.now().date()
    if month is None:
        if today.month < 10:
            month = f'0{today.month}'
        else:
            month = today.month
    else:
        if month < 10:
            month = f'0{month}'
        else:
            month = month

    date_filter = datetime.strptime(f'{today.year}-{month}-01 00:00:00', _format)
    before_date_filter = date_filter - timedelta(weeks=90)
    after_date_filter = date_filter + timedelta(weeks=90)

    courses = session.query(Course
                    ).outerjoin(Lesson,
                                and_(Course.lesson_id == Lesson.id,
                                     Lesson.status >= constant.STATUS_INACTIVE)
                    ).filter(Course.status >= constant.STATUS_INACTIVE,
                             and_(Course.course_date >= before_date_filter,
                                  Course.course_date <= after_date_filter),
                    ).options(contains_eager(Course.lesson),
                    ).order_by(Course.course_date).all()

    result = []
    for course in simple_courses_schema.dump(courses):
        if not next((e for e in result if e['date'] == course['course_date']), None):
            result.append({
                'date': course['course_date'],
                'course_list': [],
            })

    for course in simple_courses_schema.dump(courses):
        if next((e for e in result if e['date'] == course['course_date']), None):
            course_detail = {
                'lesson': simple_lesson_schema.dump(course['lesson']),
                'course': {
                    'id': course['id'],
                    'title': course['title'],
                    'course_date': course['course_date'],
                },
            }
            next((e for e in result if e['date'] == course['course_date']))['course_list'].append(course_detail)

    response.result_data = {
        'count': len(courses),
        'courses': result,
    }
    return response
