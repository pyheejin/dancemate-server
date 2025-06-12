from sqlalchemy import and_, or_
from sqlalchemy.orm import contains_eager

from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_search_pre(session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(_format), _format)

    keyword_query = session.query(SearchKeyword)

    latest_keyword = keyword_query.filter(SearchKeyword.user_id == g.id,
                                          SearchKeyword.type == 1,
                                          SearchKeyword.keyword != '',
                                          SearchKeyword.status == constant.STATUS_ACTIVE,
                                    ).order_by(SearchKeyword.created_at.desc()).all()
    recommend_keyword = keyword_query.filter(SearchKeyword.type == 99,
                                             SearchKeyword.keyword != '',
                                             SearchKeyword.status == constant.STATUS_ACTIVE,
                                    ).order_by(SearchKeyword.created_at.desc()).all()

    recommend_courses = session.query(Lesson
                            ).outerjoin(Course,
                                        and_(Course.lesson_id == Lesson.id,
                                             # Course.course_date >= today,
                                             Course.status == constant.STATUS_ACTIVE)
                            # ).outerjoin(RecommendUser,
                            #             and_(RecommendUser.user_id == Lesson.user_id,
                            #                  RecommendUser.status == constant.STATUS_ACTIVE)
                            ).filter(Lesson.status == constant.STATUS_ACTIVE,
                                     Lesson.last_course_date >= today,
                            ).options(contains_eager(Lesson.course),
                            ).all()[:3]

    response.result_data = {
        'latest_keyword': search_keyword_schema.dump(latest_keyword),
        'recommend_keyword': search_keyword_schema.dump(recommend_keyword),
        'recommend_courses': lessons_schema.dump(recommend_courses),
    }
    return response


def get_search(session, keyword, g):
    response = DefaultModel()

    date_format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(date_format), date_format)

    courses = session.query(Lesson
                    ).outerjoin(Course,
                                and_(Course.lesson_id == Lesson.id,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).outerjoin(User,
                                and_(User.id == Lesson.user_id,
                                     User.status == constant.STATUS_ACTIVE)
                    ).outerjoin(UserCourseLike,
                                and_(UserCourseLike.course_id == Course.id,
                                     UserCourseLike.user_id == g.id,
                                     UserCourseLike.status == constant.STATUS_ACTIVE)
                    ).filter(Course.status == constant.STATUS_ACTIVE,
                             Course.course_date >= today,
                             or_(Lesson.title.like(f'%{keyword}%'),
                                 Lesson.description.like(f'%{keyword}%'),
                                 and_(User.type == constant.USER_TYPE_DANCER,
                                      User.nickname.like(f'%{keyword}%'))),
                    ).options(contains_eager(Lesson.course),
                              contains_eager(Lesson.dancer),
                              contains_eager(Lesson.course).contains_eager(Course.like_user),
                    ).all()

    # 최근 검색어에 추가
    if keyword != '':
        search_keyword = SearchKeyword()
        session.add(search_keyword)

        search_keyword.type = 1
        search_keyword.user_id = g.id,
        search_keyword.keyword = keyword

    response.result_data = {
        'result_count': len(courses),
        'courses': lessons_schema.dump(courses),
    }
    return response