import hashlib

from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Double

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
    expired_day = Column(Integer, default=30, comment='티켓 유효기간')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    dancer_lesson = relationship('Lesson', back_populates='dancer')
    search_keyword = relationship('SearchKeyword', back_populates='user')
    reserve_course = relationship('UserCourse', back_populates='reserve')
    mate_ticket = relationship('UserTicket', back_populates='mate')
    dancer_ticket = relationship('Ticket', back_populates='dancer')
    user_course_like = relationship('UserCourseLike', back_populates='user')
    payment = relationship('Payment', back_populates='user')
    review = relationship('Review', back_populates='user')
    notification = relationship('Notification', back_populates='user')
    chat_room = relationship('ChatRoom', back_populates='user')
    chat = relationship('Chat', back_populates='user')
    chat_room_user = relationship('ChatRoomUser', back_populates='user')
    room_notification = relationship('ChatRoomNotification', back_populates='user')


class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    title = Column(String(255), comment='타이틀')
    description = Column(Text, comment='내용')
    image_url = Column(String(255), comment='이미지 url')
    count = Column(Integer, comment='총 수업 회차')
    last_course_date = Column(DateTime, comment='마지막 수업일')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    dancer = relationship('User', back_populates='dancer_lesson')
    course = relationship('Course', back_populates='lesson')
    review = relationship('Review', back_populates='lesson')
    chat_room = relationship('ChatRoom', back_populates='lesson')


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    lesson_id = Column(Integer, ForeignKey('lesson.id'), comment='')
    title = Column(String(255), comment='타이틀')
    course_date = Column(DateTime, comment='수업일')
    start_time = Column(String(10), comment='수업 시작시간')
    end_time = Column(String(10), comment='수업 종료시간')
    address = Column(Text, comment='연습실 주소')
    address_detail = Column(Text, comment='연습실 주소')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    lesson = relationship('Lesson', back_populates='course')
    user_course = relationship('UserCourse', back_populates='course')
    like_user = relationship('UserCourseLike', back_populates='course')


class LessonImage(Base):
    __tablename__ = 'lesson_image'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    order = Column(Integer, comment='순서')
    lesson_id = Column(Integer, comment='')
    image_url = Column(Text, comment='이미지 url')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    count = Column(Integer, comment='회차')
    cost = Column(Integer, comment='정가')
    discount_rate = Column(Integer, comment='할인율')
    price = Column(Integer, comment='판매가')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    dancer = relationship('User', back_populates='dancer_ticket')
    mate_ticket = relationship('UserTicket', back_populates='ticket')


class UserTicket(Base):
    __tablename__ = 'user_ticket'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    ticket_id = Column(Integer, ForeignKey('ticket.id'), comment='')
    count = Column(Integer, comment='사용 횟수')
    remain_count = Column(Integer, comment='남은 횟수')
    expired_date = Column(DateTime, default=datetime.now() + timedelta(days=30))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    mate = relationship('User', back_populates='mate_ticket')
    ticket = relationship('Ticket', back_populates='mate_ticket')
    payment = relationship('Payment', back_populates='user_ticket')


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    user_ticket_id = Column(Integer, ForeignKey('user_ticket.id'), comment='')
    price = Column(Integer, comment='결제 금액')
    method = Column(Integer, comment='결제 방법(1:카드, 2:무통장, 3:간편결제)')
    data = Column(Text, comment='결제 데이터')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='payment')
    user_ticket = relationship('UserTicket', back_populates='payment')


class Qna(Base):
    __tablename__ = 'qna'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    is_reply = Column(Integer, default=0, comment='답변여부')
    user_id = Column(Integer, comment='작성자')
    title = Column(String(255), comment='질문 제목')
    question = Column(Text, comment='질문 내용')
    answer = Column(Text, comment='답변')
    email = Column(String(255), comment='답변 받을 이메일')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    is_best = Column(Integer, default=0, comment='1:베스트 리뷰')
    satisfaction = Column(Double, comment='만족도')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    lesson_id = Column(Integer, ForeignKey('lesson.id'), comment='')
    user_course_id = Column(Integer, ForeignKey('user_course.id'), comment='')
    title = Column(Text, comment='제목')
    description = Column(Text, comment='내용')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='review')
    lesson = relationship('Lesson', back_populates='review')
    user_course = relationship('UserCourse', back_populates='review')


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
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    user_ticket_id = Column(Integer, comment='')
    course_id = Column(Integer, ForeignKey('course.id'), comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    reserve = relationship('User', back_populates='reserve_course')
    course = relationship('Course', back_populates='user_course')
    review = relationship('Review', back_populates='user_course')


class UserCourseLike(Base):
    __tablename__ = 'user_course_like'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    order = Column(Integer, default=1, comment='순서')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    course_id = Column(Integer, ForeignKey('course.id'), comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='user_course_like')
    course = relationship('Course', back_populates='like_user')


class SearchKeyword(Base):
    __tablename__ = 'search_keyword'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    type = Column(Integer, default=1, comment='1:유저가 검색한 키워드, 99:관리자가 등록하는 추천 키워드')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    keyword = Column(String(255), comment='검색어')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='search_keyword')


class Notification(Base):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    lesson = Column(Integer, default=1, comment='수업 관련 알림(1:활성화, 0:비활성화)')
    ticket = Column(Integer, default=1, comment='티켓 관련 알림(1:활성화, 0:비활성화)')
    community = Column(Integer, default=1, comment='커뮤니티 관련 알림(1:활성화, 0:비활성화)')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='notification')


class ChatRoom(Base):
    __tablename__ = 'chat_room'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    lesson_id = Column(Integer, ForeignKey('lesson.id'), comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='chat_room')
    lesson = relationship('Lesson', back_populates='chat_room')
    chat = relationship('Chat', back_populates='room')
    chat_room_user = relationship('ChatRoomUser', back_populates='room')
    room_notification = relationship('ChatRoomNotification', back_populates='room')


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    type = Column(Integer, default=1, comment='1:메시지, 99:초대or퇴장')
    chat_room_id = Column(Integer, ForeignKey('chat_room.id'), comment='')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    message = Column(String(255), comment='메시지')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='chat')
    room = relationship('ChatRoom', back_populates='chat')


class ChatRoomUser(Base):
    __tablename__ = 'chat_room_user'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    chat_room_id = Column(Integer, ForeignKey('chat_room.id'), comment='')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='chat_room_user')
    room = relationship('ChatRoom', back_populates='chat_room_user')


# 채팅방 확인 여부
class ChatRoomNotification(Base):
    __tablename__ = 'chat_room_notification'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, comment='1:활성화, 0:비활성화, -1:삭제')
    chat_room_id = Column(Integer, ForeignKey('chat_room.id'), comment='')
    user_id = Column(Integer, ForeignKey('user.id'), comment='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('User', back_populates='room_notification')
    room = relationship('ChatRoom', back_populates='room_notification')
