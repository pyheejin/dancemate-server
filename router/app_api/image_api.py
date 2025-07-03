from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.common import error_response, get_current_user
from database.database import db
from database.models import User
from database.base_model import DefaultModel
from controller import image_controller


router = APIRouter(
    prefix='/image'
)


class PostImageUploadModel(BaseModel):
    bucket: str
    lesson_id: Optional[int]
    images: List[UploadFile] = File(None)

    @classmethod
    def as_form(cls,
                bucket: str = Form(...),
                lesson_id: int = Form(None),
                images: List[UploadFile] = File(None)):
        return cls(bucket=bucket,
                   lesson_id=lesson_id,
                   images=images)


@router.post('', tags=['image'], summary='이미지 업로드')
def post_user_profile_image(request: PostImageUploadModel = Depends(PostImageUploadModel.as_form),
                            session: Session = Depends(db.session),
                            g: User = Depends(get_current_user),):
    result_msg = '이미지 업로드'
    try:
        response = image_controller.post_image_upload(session=session,
                                                      request=request,
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
