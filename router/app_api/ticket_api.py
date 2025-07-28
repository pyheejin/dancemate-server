from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import ticket_controller


router = APIRouter(
    prefix='/ticket'
)


class PostTicketModel(BaseModel):
    status: int
    count: int
    cost: int
    discount_rate: Optional[int]


class PostTicketExpireModel(BaseModel):
    day: int


@router.get('', tags=['ticket'], summary='티켓 목록', dependencies=[Depends(get_current_user)])
def get_ticket(session: Session = Depends(db.session),
               g: User = Depends(get_current_user)):
    result_msg = '티켓'
    try:
        response = ticket_controller.get_ticket(session=session,
                                                g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.post('', tags=['ticket'], summary='티켓 등록', dependencies=[Depends(get_current_user)])
def post_ticket(request: PostTicketModel,
                session: Session = Depends(db.session),
                g: User = Depends(get_current_user)):
    result_msg = '티켓 등록'
    try:
        response = ticket_controller.post_ticket(request=request,
                                                 session=session,
                                                 g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.put('/{ticket_id}', tags=['ticket'], summary='티켓 수정', dependencies=[Depends(get_current_user)])
def put_ticket_detail(ticket_id: int,
                      request: PostTicketModel,
                      session: Session = Depends(db.session),
                      g: User = Depends(get_current_user)):
    result_msg = '티켓 수정'
    try:
        response = ticket_controller.put_ticket_detail(ticket_id=ticket_id,
                                                       request=request,
                                                       session=session,
                                                       g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.get('/sales', tags=['ticket'], summary='티켓 판매 내역', dependencies=[Depends(get_current_user)])
def get_ticket_sales(year: int = 0,
                     month: int = 0,
                     session: Session = Depends(db.session),
                     g: User = Depends(get_current_user)):
    result_msg = '티켓 판매 내역'
    try:
        response = ticket_controller.get_ticket_sales(year=year,
                                                      month=month,
                                                      session=session,
                                                      g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.get('/{ticket_id}', tags=['ticket'], summary='티켓 상세', dependencies=[Depends(get_current_user)])
def get_ticket_detail(ticket_id: int,
                      session: Session = Depends(db.session),
                      g: User = Depends(get_current_user)):
    result_msg = '티켓 상세'
    try:
        response = ticket_controller.get_ticket_detail(ticket_id=ticket_id,
                                                       session=session,
                                                       g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response


@router.post('/expire', tags=['ticket'], summary='티켓 유효기간 변경', dependencies=[Depends(get_current_user)])
def post_ticket_detail_expired(request: PostTicketExpireModel,
                               session: Session = Depends(db.session),
                               g: User = Depends(get_current_user)):
    result_msg = '티켓 유효기간 변경'
    try:
        response = ticket_controller.post_ticket_detail_expired(request=request,
                                                                session=session,
                                                                g=g)
    except HTTPException as e:
        print(f'error: {e.detail}')
        session.rollback()
        response = None
        response = error_response(response, e.detail, e.status_code, result_msg)
    except Exception as e:
        print(e)
        session.rollback()

        response = DefaultModel()
        response.result_msg = f'{result_msg} 실패'
        response.result_code = 210
    else:
        session.commit()
        if response is None:
            response = DefaultModel()
        if response.result_msg is not None:
            response.result_msg = f'{result_msg} 성공'
    finally:
        session.close()
    return response