from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.common import error_response, get_current_user
from database.database import db
from database.base_model import DefaultModel
from controller import search_controller


router = APIRouter(
    prefix='/search'
)


@router.get('/pre', tags=['search'], summary='검색 전', dependencies=[Depends(get_current_user)])
def get_search_pre(session: Session = Depends(db.session)):
    result_msg = '검색 전'
    try:
        response = search_controller.get_search_pre(session=session)
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


@router.get('', tags=['search'], summary='검색', dependencies=[Depends(get_current_user)])
def get_search(session: Session = Depends(db.session),
               keyword: Optional[str] = None):
    result_msg = '검색'
    try:
        response = search_controller.get_search(session=session,
                                                keyword=keyword)
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