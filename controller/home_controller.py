from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_home(session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now().date()
    today = datetime.strptime(now.strftime(_format), _format)
    tomorrow = datetime.strptime((now+timedelta(days=1)).strftime(_format), _format)

    recommend_users = session.query(User
                            ).outerjoin(RecommendUser, RecommendUser.user_id == User.id
                            ).filter(User.status == constant.STATUS_ACTIVE,
                                     RecommendUser.status == constant.STATUS_ACTIVE).all()
    today_courses = session.query(Course
                            ).outerjoin(CourseDetail,
                                        and_(CourseDetail.course_id == Course.id,
                                             CourseDetail.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserCourse,
                                        and_(UserCourse.course_detail_id == CourseDetail.id,
                                             UserCourse.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserCourseLike,
                                        and_(UserCourseLike.course_id == Course.id,
                                             UserCourseLike.user_id == g.id,
                                             UserCourseLike.status == constant.STATUS_ACTIVE)
                            ).filter(Course.status == constant.STATUS_ACTIVE,
                                     CourseDetail.course_date.between(today, tomorrow)
                            ).options(contains_eager(Course.course_detail),
                                      contains_eager(Course.course_like_user),
                                      contains_eager(Course.course_detail
                                    ).contains_eager(CourseDetail.user_course_detail),
                            ).all()
    reserve_courses = session.query(CourseDetail
                            ).outerjoin(Course,
                                        and_(CourseDetail.course_id == Course.id,
                                             Course.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserCourse,
                                        and_(UserCourse.course_detail_id == CourseDetail.id,
                                             UserCourse.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserCourseLike,
                                        and_(UserCourseLike.course_id == Course.id,
                                             UserCourseLike.user_id == g.id,
                                             UserCourseLike.status == constant.STATUS_ACTIVE)
                            ).filter(CourseDetail.status == constant.STATUS_ACTIVE,
                                     CourseDetail.course_date >= today,
                                     UserCourse.user_id == g.id,
                            ).options(contains_eager(CourseDetail.course),
                                      contains_eager(CourseDetail.user_course_detail),
                                      contains_eager(CourseDetail.course
                                    ).contains_eager(Course.course_like_user),
                            ).all()

    response.result_data = {
        'recommend_users': user_list_schema.dump(recommend_users),
        'today_courses': course_list_schema.dump(today_courses),
        'reserve_courses': course_details_schema.dump(reserve_courses),
    }
    return response
