from sqlalchemy.orm import contains_eager
from fastapi import HTTPException
from urllib3 import request

from database.models import *
from database.schema import *
from database.base_model import DefaultModel
from config.constant import *


def get_review_detail(review_id, session):
    response = DefaultModel()

    review = session.query(Review
                    ).outerjoin(UserCourse, UserCourse.id == Review.user_course_id,
                    ).outerjoin(Course, Course.id == UserCourse.course_id,
                    ).outerjoin(Lesson, Review.lesson_id == Lesson.id,
                    ).filter(Review.id == review_id,
                             Review.status >= constant.STATUS_INACTIVE,
                    ).options(contains_eager(Review.user_course),
                              contains_eager(Review.user_course
                                ).contains_eager(UserCourse.course),
                              contains_eager(Review.lesson),
                    ).first()

    if review is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    response.result_data = {
        'review': review_schema.dump(review),
    }
    return response


def put_review_detail(review_id, request, session):
    response = DefaultModel()

    review = session.query(Review
                    ).outerjoin(UserCourse, UserCourse.id == Review.user_course_id,
                    ).outerjoin(Course, Course.id == UserCourse.course_id,
                    ).outerjoin(Lesson, Review.lesson_id == Lesson.id,
                    ).filter(Review.id == review_id,
                             Review.status >= constant.STATUS_INACTIVE,
                    ).options(contains_eager(Review.user_course),
                              contains_eager(Review.user_course
                                ).contains_eager(UserCourse.course),
                              contains_eager(Review.lesson),
                    ).first()

    if review is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    review.satisfaction = request.rate
    review.description = request.description
    return response
