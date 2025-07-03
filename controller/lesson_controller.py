from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_lesson(session, date):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.now().date()
    if date is None:
        before_date_filter = datetime.strptime(today.strftime(_format), _format)
        after_date_filter = datetime.strptime((today + timedelta(days=1)).strftime(_format), _format)
    else:
        before_date_filter = datetime.strptime(f'{date} 00:00:00', _format)
        after_date_filter = before_date_filter + timedelta(days=1)

    courses = session.query(Course
                    ).outerjoin(Lesson,
                                and_(Course.lesson_id == Lesson.id,
                                     Lesson.status >= constant.STATUS_INACTIVE)
                    ).filter(Course.status >= constant.STATUS_INACTIVE,
                             and_(Course.course_date >= before_date_filter,
                                  Course.course_date <= after_date_filter),
                    ).options(contains_eager(Course.lesson),
                    ).all()

    response.result_data = {
        'count': len(courses),
        'lessons': courses_schema.dump(courses),
    }
    return response


def post_lesson(request, session, g):
    response = DefaultModel()

    if g.type != constant.USER_TYPE_DANCER:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DANCER_ONLY][0],
                            detail=ERROR_DANCER_ONLY)

    _format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    today = datetime.strptime(now.strftime(_format), _format)

    lesson = Lesson()
    session.add(lesson)

    lesson.status = request.status
    lesson.user_id = g.id
    lesson.title = request.title
    lesson.description = request.description
    session.flush()

    for detail in request.detail_list:
        course_date = f'{detail.course_date} {detail.start_time}:00'
        if today > datetime.strptime(course_date, _format):
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_CREATED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_CREATED)

        course = Course()
        session.add(course)

        course.lesson_id = lesson.id
        course.title = detail.title
        course.course_date = course_date
        course.start_time = detail.start_time
        course.end_time = detail.end_time
        course.address = detail.address
        course.address_detail = detail.address_detail

    lesson.count = len(request.detail_list)
    lesson.last_course_date = request.detail_list[-1].course_date

    # 수업 개설시 단톡방 자동 생성
    chat_room = ChatRoom()
    session.add(chat_room)

    chat_room.user_id = g.id
    chat_room.lesson_id = lesson.id
    session.flush()

    chat_room_user = ChatRoomUser()
    session.add(chat_room_user)

    chat_room_user.chat_room_id = chat_room.id
    chat_room_user.user_id = g.id

    response.result_data = {
        'lesson_id': lesson.id
    }
    return response


def put_lesson_detail(lesson_id, request, session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    today = datetime.strptime(now.strftime(_format), _format)

    lesson = session.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    lesson.status = request.status
    lesson.user_id = g.id
    lesson.title = request.title
    lesson.description = request.description

    course_query = session.query(Course
                        ).filter(Course.lesson_id == lesson_id,
                                 Course.status >= constant.STATUS_INACTIVE)
    course_query.update({'status': constant.STATUS_DELETED}, synchronize_session=False)

    for detail in request.detail_list:
        date = datetime.strptime(detail.course_date, _format).date()
        course_date = f'{date} {detail.start_time}:00'
        if today > datetime.strptime(course_date, _format):
            raise HTTPException(status_code=ERROR_DIC[ERROR_PAST_SESSION_CANNOT_BE_CREATED][0],
                                detail=ERROR_PAST_SESSION_CANNOT_BE_CREATED)

        course = Course()
        session.add(course)

        course.lesson_id = lesson.id
        course.title = detail.title
        course.course_date = course_date
        course.start_time = detail.start_time
        course.end_time = detail.end_time
        course.address = detail.address
        course.address_detail = detail.address_detail

    lesson.count = len(request.detail_list)
    lesson.last_course_date = request.detail_list[-1].course_date

    response.result_data = {
        'lesson_id': lesson.id
    }
    return response


def get_lesson_detail(session, lesson_id, g):
    response = DefaultModel()

    date_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.strptime(datetime.now().strftime(date_format), date_format)

    filter_list = []
    lesson = session.query(Lesson).filter(Lesson.user_id == g.id).first()
    # if lesson is None:
    #     if g.type == constant.USER_TYPE_MATE:
    #         filter_list.append(Course.course_date >= now)

    lesson = session.query(Lesson
                    ).outerjoin(Course,
                                and_(Course.lesson_id == Lesson.id,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).outerjoin(UserCourseLike,
                                and_(UserCourseLike.course_id == Course.id,
                                     UserCourseLike.user_id == g.id,
                                     UserCourseLike.status == constant.STATUS_ACTIVE)
                    ).filter(Lesson.status >= constant.STATUS_INACTIVE,
                             Lesson.id == lesson_id,
                             *filter_list,
                    ).options(contains_eager(Lesson.course),
                              contains_eager(Lesson.course
                            ).contains_eager(Course.like_user),
                    ).all()
    if len(lesson) == 0:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    response.result_data = {
        'lesson': lesson_schema.dump(lesson[0]),
    }
    return response


def post_lesson_detail_review(lesson_id, request, session, g):
    response = DefaultModel()

    lesson = session.query(Lesson
                    ).outerjoin(Course,
                                and_(Course.lesson_id == Lesson.id,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).outerjoin(UserCourse,
                                and_(UserCourse.course_id == Course.id,
                                     UserCourse.user_id == g.id,
                                     UserCourse.status == constant.STATUS_ACTIVE)
                    ).filter(Lesson.status >= constant.STATUS_INACTIVE,
                             Lesson.id == lesson_id,
                    ).options(contains_eager(Lesson.course),
                              contains_eager(Lesson.course
                            ).contains_eager(Course.user_course),
                    ).all()
    if len(lesson) == 0:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    review = Review()
    session.add(review)

    review.satisfaction = request.rate
    review.user_id = g.id
    review.lesson_id = lesson[0].id
    review.user_course_id = request.user_course_id
    review.description = request.description
    return response