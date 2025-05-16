from dateutil.utils import today
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_course_detail(course_detail_id, session):
    response = DefaultModel()

    course = session.query(CourseDetail
                    ).outerjoin(Course,
                                and_(CourseDetail.course_id == Course.id,
                                     Course.status >= constant.STATUS_INACTIVE)
                    ).filter(CourseDetail.status >= constant.STATUS_INACTIVE,
                             CourseDetail.id == course_detail_id,
                    ).options(contains_eager(CourseDetail.course),
                    ).first()

    response.result_data = {
        'course_detail': course_detail_schema.dump(course),
    }
    return response


