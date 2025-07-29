from dateutil.utils import today
from fastapi import HTTPException
from sqlalchemy import and_, between
from sqlalchemy.orm import contains_eager
from datetime import timedelta, datetime

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
                    ).order_by(Ticket.created_at.desc()).all()

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


def get_ticket_sales(year, month, session, g, page, pageSize):
    response = DefaultModel()

    filter_list = []

    if year > 0 and month > 0:
        start_date = datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d')
        end_date = start_date + timedelta(days=30)
        filter_list.append(between(UserTicket.created_at, start_date, end_date))

    tickets = session.query(UserTicket
                    ).outerjoin(User, UserTicket.user_id == User.id,
                    ).outerjoin(Payment, Payment.user_ticket_id == UserTicket.id,
                    ).outerjoin(Ticket, and_(Ticket.id == UserTicket.ticket_id,
                                             Ticket.status == constant.STATUS_ACTIVE),
                    ).filter(Ticket.user_id == g.id,
                             *filter_list
                    ).options(contains_eager(UserTicket.ticket),
                              contains_eager(UserTicket.mate),
                              contains_eager(UserTicket.payment),
                    ).order_by(UserTicket.created_at.desc()
                    ).offset(pageSize * (page - 1)).limit(pageSize).all()

    result = []

    if year > 0 and month > 0:
        for user_ticket in user_tickets_schema.dump(tickets):
            if not next((e for e in result if e['date'] == user_ticket['created_at']), None):
                result.append({
                    'date': user_ticket['created_at'],
                    'ticket_list': [],
                })

        for user_ticket in user_tickets_schema.dump(tickets):
            if next((e for e in result if e['date'] == user_ticket['created_at']), None):
                ticket = {
                    'mate': {
                        'nickname': user_ticket['mate']['nickname'],
                        'email': user_ticket['mate']['email'],
                        'image_url': user_ticket['mate']['image_url'],
                    },
                    'count': f"{user_ticket['ticket']['count']}회권",
                    'price': format(user_ticket['ticket']['price'], ',d'),
                    'remain_count': user_ticket['remain_count'],
                    'expired_date': user_ticket['expired_date'],
                    'created_at': user_ticket['created_at'],
                    'payment': user_ticket['payment']
                }
                next((e for e in result if e['date'] == user_ticket['created_at']))['ticket_list'].append(ticket)
    else:
        for data in user_tickets_schema.dump(tickets):
            if not next((e for e in result if e['year'] == data['created_at'].split('-')[0]), None):
                result.append({
                    'year': data['created_at'].split('-')[0],
                    'month_list': [],
                })

        for data in user_tickets_schema.dump(tickets):
            year = data['created_at'].split('-')[0]
            month = data['created_at'].split('-')[1]

            if len(result) > 0:
                for i in result:
                    if year == i['year']:
                        if len(i['month_list']) == 0:
                            month_data = {
                                'month': month,
                                'total_price': 0
                            }
                            i['month_list'].append(month_data)
                        else:
                            if not next((e for e in i['month_list'] if e['month'] == month), None):
                                month_data = {
                                    'month': month,
                                    'total_price': 0
                                }
                                i['month_list'].append(month_data)

        for data in user_tickets_schema.dump(tickets):
            year = data['created_at'].split('-')[0]
            month = data['created_at'].split('-')[1]
            if len(result) > 0:
                for i in result:
                    if year == i['year']:
                        for j in i['month_list']:
                            if j['month'] == month:
                                j['total_price'] += data['ticket']['price']

    response.result_data = {
        'count': len(tickets),
        'tickets': result,
    }
    return response
