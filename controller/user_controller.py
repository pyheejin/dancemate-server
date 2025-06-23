import pillow_heif

from sqlalchemy import and_, false
from sqlalchemy.orm import contains_eager
from fastapi import HTTPException, UploadFile
from PIL import Image
from io import BytesIO

from database.models import *
from database.schema import *
from database.base_model import DefaultModel, DefaultLoginModel
from config.jwt_handler import JWT
from config.constant import *


def get_user_profile(session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(_format), _format)

    user = session.query(User).outerjoin(UserCourse,
                                         and_(UserCourse.user_id == User.id,
                                              UserCourse.status >= constant.STATUS_INACTIVE)
                            ).outerjoin(Course,
                                        and_(Course.id == UserCourse.course_id,
                                             Course.status == constant.STATUS_ACTIVE,
                                             Course.course_date >= today)
                            ).outerjoin(Lesson,
                                        and_(Course.lesson_id == Lesson.id,
                                             Lesson.status == constant.STATUS_ACTIVE)
                            ).outerjoin(UserTicket,
                                        and_(UserTicket.user_id == User.id,
                                             UserTicket.status >= constant.STATUS_INACTIVE,
                                             UserTicket.remain_count > 0,
                                             UserTicket.expired_date >= today)
                            ).filter(User.id == g.id,
                            ).options(contains_eager(User.mate_ticket),
                                      contains_eager(User.reserve_course),
                                      contains_eager(User.reserve_course
                                                     ).contains_eager(UserCourse.course),
                                      contains_eager(User.reserve_course
                                                     ).contains_eager(UserCourse.course
                                                    ).contains_eager(Course.lesson),
                            ).order_by(Course.course_date,
                                       UserTicket.expired_date,
                            ).all()

    response.result_data = {
        'user': user_profile_schema.dump(user[0]),
    }
    return response


def post_user_profile(session, request, g):
    response = DefaultModel()

    user = session.query(User).filter(User.id == g.id).first()
    if user is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    user.nickname = request.nickname
    user.introduction = request.introduction

    # 이미지 업로드
    if request.image_url is not None:
        image = request.image_url

        file_data = image.filename.split('.')
        filename = f'user_{g.id}_profile_{file_data[0]}'
        extension = file_data[1]

        if extension.upper() == 'HEIC':
            heif_file = pillow_heif.read_heif(image.file.read())
            img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, 'raw')
        else:
            img = Image.open(BytesIO(image.file.read()))

        # webp_data = BytesIO()
        img.save(f'../dancemate_app/assets/images/{filename}.jpeg', format='jpeg', quality=75)
        user.image_url = f'assets/images/{filename}.jpeg'
        # webp_data.seek(0)

        # webp_upload_file = UploadFile(webp_data, filename=filename)

    response.result_data = {
        'user': user_profile_schema.dump(user),
    }
    return response


def get_user_detail(session, g, user_id):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(_format), _format)

    if g.id == user_id:
        is_mine = True

        user = session.query(User
                    ).outerjoin(UserCourse,
                                and_(UserCourse.user_id == User.id,
                                     UserCourse.status >= constant.STATUS_INACTIVE)
                    ).outerjoin(Course,
                                and_(Course.id == UserCourse.course_id,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).outerjoin(Lesson,
                                and_(Course.lesson_id == Lesson.id,
                                     Lesson.status == constant.STATUS_ACTIVE)
                    ).outerjoin(UserTicket,
                                and_(UserTicket.user_id == User.id,
                                     UserTicket.status >= constant.STATUS_INACTIVE)
                    ).filter(User.id == g.id,
                             UserTicket.expired_date >= today,
                    ).options(contains_eager(User.mate_ticket),
                              contains_eager(User.reserve_course),
                              contains_eager(User.reserve_course
                                        ).contains_eager(UserCourse.course),
                              contains_eager(User.reserve_course
                                        ).contains_eager(UserCourse.course
                                        ).contains_eager(Course.lesson),
                    ).all()

        if len(user) > 0:
            user = user_profile_schema.dump(user[0])
    else:
        is_mine = False

        user = session.query(User
                    ).outerjoin(Ticket,
                                and_(Ticket.user_id == User.id,
                                     Ticket.status >= constant.STATUS_INACTIVE)
                    ).outerjoin(Lesson,
                                and_(Lesson.user_id == User.id,
                                     Lesson.last_course_date >= today,
                                     Lesson.status == constant.STATUS_ACTIVE)
                    ).outerjoin(Course,
                                and_(Course.lesson_id == Lesson.id,
                                     Course.course_date >= today,
                                     Course.status == constant.STATUS_ACTIVE)
                    ).filter(User.id == user_id,
                    ).options(contains_eager(User.dancer_ticket),
                              contains_eager(User.dancer_lesson),
                              contains_eager(User.dancer_lesson
                                ).contains_eager(Lesson.course),
                    ).all()

        if len(user) > 0:
            user = user_detail_schema.dump(user[0])

    response.result_data = {
        'user': user,
        'is_mine': is_mine,
    }
    return response


def post_user_join(session, request):
    response = DefaultModel()

    jwt = JWT()

    exists = session.query(User).filter(User.email == request.email).first()
    if exists:
        raise HTTPException(status_code=ERROR_DIC[ERROR_EMAIL_EXISTS][0],
                            detail=ERROR_EMAIL_EXISTS)

    user = User()
    user.type = request.type
    user.email = request.email
    user.password = jwt.get_password_hash(request.password)
    user.nickname = request.nickname
    user.name = request.name
    user.phone = request.phone
    user.introduction = request.introduction

    if request.type == constant.USER_TYPE_MATE:
        user.expired_day = 0
    else:
        user.expired_day = 30

    session.add(user)
    session.flush()

    user_payload = user_payload_schema.dump(user)
    user.access_token = jwt.create_access_token(user_payload)
    user.refresh_token = jwt.create_refresh_token(user_payload)

    # 알림
    notification = Notification()
    session.add(notification)

    notification.user_id = user.id
    notification.lesson = constant.STATUS_ACTIVE
    notification.ticket = constant.STATUS_ACTIVE
    notification.community = constant.STATUS_ACTIVE

    response.result_data = {
        'user': user_payload,
    }
    return response


def post_user_login(session, request):
    response = DefaultLoginModel()

    user = session.query(User).filter(User.email == request.username).first()
    if user is not None:
        jwt = JWT()
        verify = jwt.verify_password(request.password, user.password)
        if verify:
            access_token = jwt.create_access_token(token_payload_schema.dump(user))
            refresh_token = jwt.create_refresh_token(token_payload_schema.dump(user))

            user.access_token = access_token
            user.refresh_token = refresh_token
            user.last_login_date = datetime.now()

            response.user_id = user.id
            response.type = user.type
            response.access_token = access_token
            response.refresh_token = refresh_token
    return response


def get_user_ticket(dancer_id, session, g):
    response = DefaultModel()

    date_format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(date_format), date_format)

    filter_list = []
    if dancer_id is not None:
        if dancer_id > 0:
            filter_list.append(Ticket.user_id == dancer_id)

    tickets = session.query(UserTicket
                    ).outerjoin(Ticket, UserTicket.ticket_id == Ticket.id,
                    ).outerjoin(User, UserTicket.user_id == User.id,
                    ).options(contains_eager(UserTicket.mate),
                              contains_eager(UserTicket.ticket),
                    ).filter(UserTicket.user_id == g.id,
                             UserTicket.status >= constant.STATUS_INACTIVE,
                             UserTicket.expired_date >= today,
                             *filter_list,
                    ).order_by(UserTicket.created_at.desc()
                    ).all()

    result = []
    for user_ticket in user_tickets_schema.dump(tickets):
        if not next((e for e in result if e['date'] == user_ticket['created_at']), None):
            result.append({
                'date': user_ticket['created_at'],
                'ticket_list': [],
            })

    for user_ticket in user_tickets_schema.dump(tickets):
        if next((e for e in result if e['date'] == user_ticket['created_at']), None):
            ticket = {
                'dancer': {
                    'nickname': user_ticket['ticket']['dancer']['nickname'],
                    'email': user_ticket['ticket']['dancer']['email'],
                    'image_url': user_ticket['ticket']['dancer']['image_url'],
                },
                'count': f"{user_ticket['ticket']['count']}회권",
                'price': format(user_ticket['ticket']['price'], ',d'),
                'remain_count': user_ticket['remain_count'],
                'expired_date': user_ticket['expired_date'],
            }
            next((e for e in result if e['date'] == user_ticket['created_at']))['ticket_list'].append(ticket)

    response.result_data = {
        'result_count': len(tickets),
        'tickets': result,
    }
    return response


def get_user_course(session, g):
    response = DefaultModel()

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.strptime(datetime.now().date().strftime(_format), _format)

    courses = session.query(Course
                    ).outerjoin(Lesson,
                                and_(Course.lesson_id == Lesson.id,
                                     Lesson.status == constant.STATUS_ACTIVE)
                    ).outerjoin(UserCourse,
                                and_(UserCourse.course_id == Course.id,
                                     UserCourse.status == constant.STATUS_ACTIVE)
                    ).outerjoin(Review,
                                and_(Review.user_course_id == UserCourse.id,
                                     Review.status == constant.STATUS_ACTIVE)
                    ).filter(UserCourse.user_id == g.id
                    ).options(contains_eager(Course.lesson),
                              contains_eager(Course.user_course),
                              contains_eager(Course.user_course).contains_eager(UserCourse.review),
                    ).order_by(Course.course_date.desc()
                    ).all()

    response.result_data = {
        'result_count': len(courses),
        'courses': courses_schema.dump(courses),
    }
    return response