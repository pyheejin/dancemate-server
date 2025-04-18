from dateutil.utils import today
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def get_ticket(session, g):
    response = DefaultModel()

    tickets = session.query(Ticket
                    ).outerjoin(User, Ticket.user_id == User.id,
                    ).filter(Ticket.user_id == g.id,
                             Ticket.status >= constant.STATUS_INACTIVE,
                    ).options(contains_eager(Ticket.dancer),
                    ).all()

    response.result_data = {
        'count': len(tickets),
        'expired_day': g.expired_day,
        'tickets': tickets_schema.dump(tickets),
    }
    return response


def post_ticket(request, session, g):
    response = DefaultModel()

    if g.type != constant.USER_TYPE_DANCER:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DANCER_ONLY][0],
                            detail=ERROR_DANCER_ONLY)

    ticket = Ticket()
    session.add(ticket)

    ticket.status = request.status
    ticket.user_id = g.id
    ticket.count = request.count
    ticket.cost = request.cost
    ticket.discount_rate = request.discount_rate
    ticket.price = request.cost * (1 - (request.discount_rate / 100))

    session.flush()

    response.result_data = {
        'ticket_id': ticket.id
    }
    return response


def put_ticket_detail(ticket_id, request, session, g):
    response = DefaultModel()

    ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    ticket.status = request.status
    ticket.count = request.count
    ticket.cost = request.cost
    ticket.discount_rate = request.discount_rate
    ticket.price = request.cost * (1 - (request.discount_rate / 100))
    return response


def get_ticket_detail(session, ticket_id, g):
    response = DefaultModel()

    ticket = session.query(Ticket
                    ).filter(Ticket.user_id == g.id,
                             Ticket.id == ticket_id,
                             Ticket.status >= constant.STATUS_INACTIVE,
                    ).first()

    if ticket is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    response.result_data = {
        'ticket': ticket_schema.dump(ticket),
    }
    return response


def post_ticket_detail_expired(request, session, g):
    response = DefaultModel()

    user = session.query(User).filter(User.id == g.id).first()
    if user is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    user.expired_day = request.day
    return response