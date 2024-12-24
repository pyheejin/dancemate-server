import hashlib

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, BigInteger

from config import config, constant
from database.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    type = Column(Integer, default=constant.USER_TYPE_MATE, comment='1:mate, 50:dancer, 99:admin')
    email = Column(String(255), comment='이메일')
    password = Column(String(255), comment='비밀번호')
    nickname = Column(String(45), comment='닉네임')
    name = Column(String(45), comment='이름')
    phone = Column(String(45), comment='전화번호')
    introduction = Column(Text, comment='자기소개')
    image_url = Column(String(255), comment='이미지 url')
    last_login_date = Column(DateTime, comment='최종 방문일')
    access_token = Column(String(255), comment='')
    refresh_token = Column(String(255), comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, comment='')
    title = Column(String(255), comment='타이틀')
    description = Column(Text, comment='내용')
    image_url = Column(String(255), comment='이미지 url')
    count = Column(Integer, comment='총 수업 회차')
    last_course_date = Column(DateTime, comment='마지막 수업일')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    course_detail = relationship('CourseDetail', back_populates='course')


class CourseDetail(Base):
    __tablename__ = 'course_detail'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    course_id = Column(Integer, ForeignKey('course.id'), comment='')
    title = Column(String(255), comment='타이틀')
    course_date = Column(DateTime, comment='수업일')
    address = Column(Text, comment='연습실 주소')
    address_detail = Column(Text, comment='연습실 주소')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    course = relationship('Course', back_populates='course_detail')


class CourseImage(Base):
    __tablename__ = 'course_image'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    order = Column(Integer, comment='순서')
    course_id = Column(Integer, comment='')
    image_url = Column(Text, comment='이미지 url')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, comment='')
    count = Column(Integer, comment='회차')
    cost = Column(Integer, comment='정가')
    price = Column(Integer, comment='판매가')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class UserTicket(Base):
    __tablename__ = 'user_ticket'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, comment='')
    ticket_id = Column(Integer, comment='')
    course_id = Column(Integer, comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, comment='')
    ticket_id = Column(Integer, comment='')
    data = Column(Text, comment='결제 데이터')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Qna(Base):
    __tablename__ = 'qna'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    is_reply = Column(Integer, comment='답변여부')
    user_id = Column(Integer, comment='')
    course_id = Column(Integer, comment='')
    question = Column(Text, comment='질문')
    answer = Column(Text, comment='답변')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    is_best = Column(Integer, comment='1:베스트 리뷰')
    satisfaction = Column(Integer, comment='만족도')
    user_id = Column(Integer, comment='')
    course_id = Column(Integer, comment='')
    title = Column(Text, comment='제목')
    description = Column(Text, comment='내용')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class RecommendUser(Base):
    __tablename__ = 'recommend_user'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, comment='')
    days = Column(Integer, comment='기간')
    last_recommend_date = Column(DateTime, comment='추천 마지막 날짜')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class UserCourse(Base):
    __tablename__ = 'user_course'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, comment='')
    course_id = Column(Integer, comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)