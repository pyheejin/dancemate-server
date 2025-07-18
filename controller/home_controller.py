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
    today_lessons = session.query(Lesson
                            ).outerjoin(Course,
                                        and_(Course.lesson_id == Lesson.id,
                                             Course.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserCourse,
                                        and_(UserCourse.course_id == Course.id,
                                             UserCourse.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserCourseLike,
                                        and_(UserCourseLike.course_id == Course.id,
                                             UserCourseLike.user_id == g.id,
                                             UserCourseLike.status == constant.STATUS_ACTIVE)
                            ).filter(Lesson.status == constant.STATUS_ACTIVE,
                                     Course.course_date.between(today, tomorrow)
                            ).options(contains_eager(Lesson.course),
                                      contains_eager(Lesson.course).contains_eager(Course.user_course),
                                      contains_eager(Lesson.course).contains_eager(Course.like_user),
                            ).all()
    reserve_lessons = session.query(Course
                            ).outerjoin(Lesson,
                                        and_(Course.lesson_id == Lesson.id,
                                             Lesson.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserCourse,
                                        and_(UserCourse.course_id == Course.id,
                                             UserCourse.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserCourseLike,
                                        and_(UserCourseLike.course_id == Course.id,
                                             UserCourseLike.user_id == g.id,
                                             UserCourseLike.status == constant.STATUS_ACTIVE)
                            ).filter(Course.status == constant.STATUS_ACTIVE,
                                     Course.course_date >= today,
                                     UserCourse.user_id == g.id,
                            ).options(contains_eager(Course.lesson),
                                      contains_eager(Course.user_course),
                                      contains_eager(Course.like_user),
                            ).all()

    response.result_data = {
        'recommend_users': user_list_schema.dump(recommend_users),
        'today_lessons': lessons_schema.dump(today_lessons),
        'reserve_lessons': courses_schema.dump(reserve_lessons),
        'login_user_id': g.id,
    }
    return response
