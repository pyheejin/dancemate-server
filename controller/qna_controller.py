from dateutil.utils import today
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from datetime import timedelta

from config.constant import *
from database.models import *
from database.schema import *
from database.base_model import DefaultModel
from config.smtp_handler import SMTP


def get_qna(session, g):
    response = DefaultModel()

    qnas = session.query(Qna
                ).filter(Qna.status >= constant.STATUS_INACTIVE,
                         Qna.user_id == g.id,
                ).order_by(Qna.created_at.desc()).all()

    response.result_data = {
        'count': len(qnas),
        'qnas': qnas_schema.dump(qnas),
    }
    return response


def post_qna(request, session, g):
    response = DefaultModel()

    qna = Qna()
    session.add(qna)

    qna.user_id = g.id
    qna.title = request.title
    qna.question = request.question
    qna.email = request.email
    session.flush()

    smtp = SMTP()
    smtp.send_email(to_email=config.EMAIL,
                    title=f'[댄스메이트] {request.title}',
                    msg=request.question)

    response.result_data = {
        'qna': qna_schema.dump(qna),
    }
    return response


def put_qna_detail(qna_id, request, session):
    response = DefaultModel()

    qna = session.query(Qna).filter(Qna.id == qna_id).first()
    if qna is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    if qna.is_reply == constant.STATUS_ACTIVE:
        raise HTTPException(status_code=ERROR_DIC[ERROR_COMPLETED_QNA_CANNOT_BE_MODIFIED][0],
                            detail=ERROR_COMPLETED_QNA_CANNOT_BE_MODIFIED)

    qna.title = request.title
    qna.question = request.question
    qna.email = request.email
    return response


def get_qna_detail(session, qna_id):
    response = DefaultModel()

    qna = session.query(Qna).filter(Qna.id == qna_id).first()
    if qna is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    response.result_data = {
        'qna': qna_schema.dump(qna),
    }
    return response


def delete_qna_detail(qna_id, session, g):
    response = DefaultModel()

    qna = session.query(Qna).filter(Qna.id == qna_id,
                                    Qna.user_id == g.id).first()
    if qna is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    qna.status = constant.STATUS_DELETED
    return response


def post_qna_detail_answer(qna_id, request, session):
    response = DefaultModel()

    qna = session.query(Qna).filter(Qna.id == qna_id).first()
    if qna is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    qna.answer = request.answer
    qna.is_reply = constant.STATUS_ACTIVE
    qna.answered_at = datetime.now()

    if qna.email != '':
        smtp = SMTP()
        smtp.send_email(to_email=qna.email,
                        title='[댄스메이트 RE] 문의하신 내용의 답변 드립니다.',
                        msg=request.answer)
    return response