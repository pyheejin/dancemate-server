from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import payment_controller


router = APIRouter(
    prefix='/payment'
)


class PostPaymentModel(BaseModel):
    ticket_id: int


@router.post('', tags=['payment'], summary='결제', dependencies=[Depends(get_current_user)])
def post_payment(request: PostPaymentModel,
                 session: Session = Depends(db.session),
                 g: User = Depends(get_current_user)):
    result_msg = '결제'
    try:
        response = payment_controller.post_payment(request=request,
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


@router.get('/{payment_id}', tags=['payment'], summary='결제 상세', dependencies=[Depends(get_current_user)])
def get_payment_detail(payment_id: int,
                       session: Session = Depends(db.session)):
    result_msg = '결제 상세'
    try:
        response = payment_controller.get_payment_detail(payment_id=payment_id,
                                                         session=session)
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