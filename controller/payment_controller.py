from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.send_fcm import FCM
from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel


def post_payment(session, request, g):
    response = DefaultModel()

    ticket = session.query(Ticket).filter(Ticket.id == request.ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    _format = '%Y-%m-%d %H:%M:%S'
    today = datetime.now().date()
    expired_date = datetime.strptime((today + timedelta(days=30)).strftime(_format), _format)

    exists = session.query(UserTicket).filter(UserTicket.user_id == g.id,
                                              UserTicket.ticket_id == request.ticket_id,
                                              UserTicket.expired_date >= today).first()
    if exists:
        raise HTTPException(status_code=ERROR_DIC[ERROR_BAD_REQUEST][0],
                            detail=ERROR_BAD_REQUEST)

    user_ticket = UserTicket()
    session.add(user_ticket)

    user_ticket.user_id = g.id
    user_ticket.ticket_id = request.ticket_id
    user_ticket.count = ticket.count
    user_ticket.remain_count = ticket.count
    user_ticket.expired_date = expired_date

    payment = Payment()
    session.add(payment)
    session.flush()

    payment.user_id = g.id
    payment.user_ticket_id = user_ticket.id
    payment.price = ticket.price

    push_data = {
        'title': '티켓 결제가 완료되었습니다.',
        'body': ''
    }
    fcm = FCM()
    fcm.send(g.fcm_token, push_data)

    response.result_data = {
        'payment': payment_detail_schema.dump(payment)
    }
    return response


def get_payment_detail(session, payment_id):
    response = DefaultModel()

    payment = session.query(Payment
                    ).outerjoin(User, Payment.user_id == User.id,
                    ).outerjoin(UserTicket, UserTicket.id == Payment.user_ticket_id,
                    ).options(contains_eager(Payment.user),
                              contains_eager(Payment.user_ticket),
                    ).filter(Payment.id == payment_id
                    ).all()

    response.result_data = {
        'payment': payment_detail_schema.dump(payment[0]),
    }
    return response
