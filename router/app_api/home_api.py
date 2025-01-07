from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.common import error_response, get_current_user
from database.database import db
from database.base_model import DefaultModel
from controller import home_controller


router = APIRouter(
    prefix='/home'
)


@router.get('', tags=['home'], summary='홈', dependencies=[Depends(get_current_user)])
def get_home(session: Session = Depends(db.session)):
    result_msg = '홈'
    try:
        response = home_controller.get_home(session=session)
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
