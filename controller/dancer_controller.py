from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from fastapi import HTTPException

from database.models import *
from database.schema import *
from database.base_model import DefaultModel, DefaultLoginModel
from config.jwt_handler import JWT
from config.constant import *


def get_dancer_detail_ticket(dancer_id, session):
    response = DefaultModel()

    tickets = session.query(Ticket
                    ).outerjoin(User, Ticket.user_id == User.id,
                    ).filter(Ticket.user_id == dancer_id,
                             Ticket.status >= constant.STATUS_INACTIVE,
                    ).options(contains_eager(Ticket.dancer),
                    ).all()

    response.result_data = {
        'result_count': len(tickets),
        'dancer': user_schema.dump(tickets[0].dancer),
        'tickets': tickets_schema.dump(tickets),
    }
    return response


def get_dancer_lesson(session, g):
    response = DefaultModel()

    lessons = session.query(Lesson
                    ).outerjoin(User, User.id == Lesson.user_id,
                    ).filter(Lesson.status >= constant.STATUS_INACTIVE,
                             Lesson.user_id == g.id,
                    ).options(contains_eager(Lesson.dancer),
                    ).order_by(Lesson.created_at.desc()).all()

    response.result_data = {
        'result_count': len(lessons),
        'courses': lessons_schema.dump(lessons),
    }
    return response