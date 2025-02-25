from sqlalchemy import and_, or_
from sqlalchemy.orm import contains_eager

from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_search_pre(session):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(_format), _format)
    print(today)

    keyword_query = session.query(SearchKeyword)

    latest_keyword = keyword_query.filter(SearchKeyword.user_id == 21,
                                          SearchKeyword.type == 1
                                    ).order_by(SearchKeyword.created_at.desc()).all()
    recommend_keyword = keyword_query.filter(SearchKeyword.type == 99
                                    ).order_by(SearchKeyword.created_at.desc()).all()

    recommend_courses = session.query(Course
                            ).outerjoin(CourseDetail,
                                        and_(CourseDetail.course_id == Course.id,
                                             # CourseDetail.course_date >= today,
                                             CourseDetail.status == constant.STATUS_ACTIVE)
                            # ).outerjoin(RecommendUser,
                            #             and_(RecommendUser.user_id == Course.user_id,
                            #                  RecommendUser.status == constant.STATUS_ACTIVE)
                            ).filter(Course.status == constant.STATUS_ACTIVE,
                                     Course.last_course_date >= today,
                            ).options(contains_eager(Course.course_detail),
                            ).all()[:3]

    response.result_data = {
        'latest_keyword': search_keyword_schema.dump(latest_keyword),
        'recommend_keyword': search_keyword_schema.dump(recommend_keyword),
        'recommend_courses': course_list_schema.dump(recommend_courses),
    }
    return response


def get_search(session, keyword):
    response = DefaultModel()

    date_format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(date_format), date_format)

    courses = session.query(CourseDetail
                    ).outerjoin(Course,
                                and_(CourseDetail.course_id == Course.id,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).outerjoin(User,
                                and_(User.id == Course.user_id,
                                     User.status == constant.STATUS_ACTIVE)
                    ).filter(CourseDetail.status == constant.STATUS_ACTIVE,
                             CourseDetail.course_date >= today,
                             or_(Course.title.like(f'%{keyword}%'),
                                 Course.description.like(f'%{keyword}%')),
                    ).options(contains_eager(CourseDetail.course),
                              contains_eager(CourseDetail.course).contains_eager(Course.dancer),
                    ).all()

    response.result_data = {
        'result_count': len(courses),
        'courses': search_course_detail_schema.dump(courses),
    }
    return response