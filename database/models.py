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
    name = Column(String(10), comment='이름')
    phone = Column(String(11), comment='전화번호')
    introduction = Column(Text, comment='자기소개')
    image_url = Column(String(255), comment='이미지 url')
    last_login_date = Column(DateTime, comment='최종 방문일')
    access_token = Column(String(255), comment='')
    refresh_token = Column(String(255), comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
