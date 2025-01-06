from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import datetime, timedelta

from database.models import *
from database.schema import *
from database.base_model import DefaultModel, DefaultLoginModel
from config.jwt_handler import JWT
from config.constant import *


def get_search_pre(session):
    response = DefaultModel()

    format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(format), format)
    tomorrow = datetime.strptime((datetime.now().date()+timedelta(days=1)).strftime(format), format)

    keyword_query = session.query(SearchKeyword)

    latest_keyword = keyword_query.filter(SearchKeyword.user_id == 21,
                                          SearchKeyword.type == 1
                                    ).order_by(SearchKeyword.created_at.desc()).all()
    recommend_keyword = keyword_query.filter(SearchKeyword.type == 99
                                    ).order_by(SearchKeyword.created_at.desc()).all()

    recommend_courses = session.query(Course
                            ).outerjoin(CourseDetail,
                                        and_(CourseDetail.course_id == Course.id,
                                             CourseDetail.status == constant.STATUS_ACTIVE)
                            ).outerjoin(RecommendUser,
                                        and_(RecommendUser.user_id == Course.user_id,
                                             RecommendUser.status == constant.STATUS_ACTIVE)
                            ).filter(Course.status == constant.STATUS_ACTIVE,
                                     CourseDetail.course_date.between(today, tomorrow)
                            ).options(contains_eager(Course.course_detail),
                            ).all()

    response.result_data = {
        'latest_keyword': search_keyword_schema.dump(latest_keyword),
        'recommend_keyword': search_keyword_schema.dump(recommend_keyword),
        'recommend_courses': course_list_schema.dump(recommend_courses),
    }
    return response
