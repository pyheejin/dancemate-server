from datetime import datetime
from marshmallow import Schema, fields


class TokenPayloadSchema(Schema):
    id = fields.Int()


token_payload_schema = TokenPayloadSchema(many=False)


class UserPayloadSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()
    image_url = fields.String()


user_payload_schema = UserPayloadSchema(many=False)


class UserListSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()
    image_url = fields.String()


user_list_schema = UserListSchema(many=True)
user_schema = UserListSchema(many=False)


class UserCourseLikeSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    order = fields.Int()
    user_id = fields.Int()
    course_id = fields.Int()


class SimpleLessonListSchema(Schema):
    id = fields.Int()
    title = fields.String()
    image_url = fields.String()

    dancer = fields.Nested(UserListSchema(), many=False)


simple_lesson_schema = SimpleLessonListSchema(many=False)


class SimpleCourseListSchema(Schema):
    id = fields.Int()
    title = fields.String()
    course_date = fields.DateTime('%Y-%m-%d')

    lesson = fields.Nested(SimpleLessonListSchema(), many=False)


simple_course_schema = SimpleCourseListSchema(many=False)
simple_courses_schema = SimpleCourseListSchema(many=True)


class SimpleCourseSchema(Schema):
    id = fields.Int()
    title = fields.String()
    address = fields.String()
    start_time = fields.String()
    end_time = fields.String()
    course_date = fields.DateTime('%Y-%m-%d')


class SimpleUserCourseSchema(Schema):
    id = fields.Int()

    course = fields.Nested(SimpleCourseSchema(), many=False)


class ReviewSchema(Schema):
    id = fields.Int()
    satisfaction = fields.Int()
    description = fields.String()


class ReviewDetailSchema(Schema):
    id = fields.Int()
    satisfaction = fields.Float()
    description = fields.String()

    lesson = fields.Nested(SimpleLessonListSchema(), many=False)
    user_course = fields.Nested(SimpleUserCourseSchema(), many=False)


review_schema = ReviewDetailSchema(many=False)


class UserCourseReviewSchema(Schema):
    id = fields.Int()

    review = fields.Nested(ReviewSchema(), many=True)


class CourseSchema(Schema):
    id = fields.Int()
    title = fields.String()
    address = fields.String()
    start_time = fields.String()
    end_time = fields.String()
    course_date = fields.DateTime('%Y-%m-%d')
    is_like = fields.Method('get_is_like')

    lesson = fields.Nested(SimpleLessonListSchema(), many=False)
    user_course = fields.Nested(UserCourseReviewSchema(), many=True)

    @classmethod
    def get_is_like(cls, obj):
        if len(obj.like_user) > 0:
            return True
        else:
            return False


courses_schema = CourseSchema(many=True)
course_schema = CourseSchema(many=False)


class LessonImageSchema(Schema):
    id = fields.Int()
    order = fields.Int()
    image_url = fields.String()


class LessonListSchema(Schema):
    id = fields.Int()
    title = fields.String()
    image_url = fields.String()
    user_id = fields.Int()
    count = fields.Int()
    description = fields.String()
    last_course_date = fields.DateTime('%Y-%m-%d')

    dancer = fields.Nested(UserListSchema(), many=False)
    course = fields.Nested(CourseSchema(), many=True)
    lesson_image = fields.Nested(LessonImageSchema(), many=True)


lessons_schema = LessonListSchema(many=True)
lesson_schema = LessonListSchema(many=False)


class SearchKeywordSchema(Schema):
    id = fields.Int()
    keyword = fields.String()


search_keyword_schema = SearchKeywordSchema(many=True)


class SearchCourseListSchema(Schema):
    id = fields.Int()
    title = fields.String()
    image_url = fields.String()
    user_id = fields.Int()
    count = fields.Int()
    last_course_date = fields.DateTime('%Y-%m-%d')

    dancer = fields.Nested(UserListSchema(), many=False)


search_lessons_schema = SearchCourseListSchema(many=True)


class SearchCourseDetailSchema(Schema):
    id = fields.Int()
    title = fields.String()
    course_date = fields.DateTime('%Y-%m-%d')

    course = fields.Nested(SearchCourseListSchema(), many=False)


search_course_detail_schema = SearchCourseDetailSchema(many=True)


class UserCourseSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    course_id = fields.Int()

    course = fields.Nested(CourseSchema(), many=False)


class TicketSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    user_id = fields.Int()
    count = fields.Int()
    cost = fields.Int()
    price = fields.Int()
    discount_rate = fields.Int()

    dancer = fields.Nested(UserListSchema(), many=False)


tickets_schema = TicketSchema(many=True)
ticket_schema = TicketSchema(many=False)


class UserTicketSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    user_id = fields.Int()
    ticket_id = fields.Int()
    count = fields.Int()
    remain_count = fields.Int()
    expired_date = fields.DateTime('%Y.%m.%d까지')
    created_at = fields.DateTime('%Y-%m-%d')

    ticket = fields.Nested(TicketSchema(), many=False)


user_tickets_schema = UserTicketSchema(many=True)
user_ticket_schema = UserTicketSchema(many=False)


class SimpleUserDetailSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()
    introduction = fields.String()
    image_url = fields.String()


simple_user_detail_schema = SimpleUserDetailSchema(many=False)


class UserProfileSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()
    introduction = fields.String()
    image_url = fields.String()

    reserve_course = fields.Nested(UserCourseSchema(), many=True)
    mate_ticket = fields.Nested(UserTicketSchema(), many=True)


user_profile_schema = UserProfileSchema(many=False)


class UserDetailSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()
    introduction = fields.String()
    image_url = fields.String()
    expired_day = fields.Int()

    dancer_lesson = fields.Nested(LessonListSchema(), many=True)
    dancer_ticket = fields.Nested(TicketSchema(), many=True)


user_detail_schema = UserDetailSchema(many=False)


class PaymentDetailSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    ticket_id = fields.Int()
    user_ticket_id = fields.Int()
    data = fields.String()
    price = fields.Int()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')

    user_ticket = fields.Nested(UserTicketSchema(), many=False)


payment_detail_schema = PaymentDetailSchema(many=False)


class NotificationSchema(Schema):
    id = fields.Int()
    lesson = fields.Method('get_lesson')
    ticket = fields.Method('get_ticket')
    community = fields.Method('get_community')

    @classmethod
    def get_lesson(cls, obj):
        if obj.lesson == 1:
            return True
        else:
            return False

    @classmethod
    def get_ticket(cls, obj):
        if obj.ticket == 1:
            return True
        else:
            return False

    @classmethod
    def get_community(cls, obj):
        if obj.community == 1:
            return True
        else:
            return False


notification_schema = NotificationSchema(many=False)


class QnaSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    user_id = fields.Int()
    is_reply = fields.Int()
    title = fields.String()
    question = fields.String()
    answer = fields.String()
    email = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


qnas_schema = QnaSchema(many=True)
qna_schema = QnaSchema(many=False)


class ChatRoomNotificationSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    user_id = fields.Int()
    chat_room_id = fields.Int()


class ChatRoomSchema(Schema):
    id = fields.Int()
    type = fields.Int()
    status = fields.Int()
    user_id = fields.Int()
    lesson_id = fields.Int()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    last_chat = fields.Method('get_last_chat')
    last_chat_time = fields.Method('get_last_chat_time')

    user = fields.Nested(SimpleUserDetailSchema(), many=False)
    friend = fields.Nested(SimpleUserDetailSchema(), many=False)
    lesson = fields.Nested(SimpleLessonListSchema(), many=False)
    room_notification = fields.Nested(ChatRoomNotificationSchema(), many=True)

    @classmethod
    def get_last_chat(cls, obj):
        if len(obj.chat) > 0:
            return obj.chat[0].message
        else:
            return ''

    @classmethod
    def get_last_chat_time(cls, obj):
        if len(obj.chat) > 0:
            if datetime.today().date() <= obj.chat[0].created_at.date():
                return obj.chat[0].created_at.strftime('%H:%M')
            else:
                return obj.chat[0].created_at.strftime('%Y-%m-%d')
        else:
            return ''


chat_rooms_schema = ChatRoomSchema(many=True)


class ChatSchema(Schema):
    id = fields.Int()
    type = fields.Int()
    status = fields.Int()
    user_id = fields.Int()
    message = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M')


class ChatRoomDetailSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    user_id = fields.Int()
    message = fields.String()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')

    chat = fields.Nested(ChatSchema(), many=True)
    lesson = fields.Nested(SimpleLessonListSchema(), many=False)
    user = fields.Nested(SimpleUserDetailSchema(), many=False)
    friend = fields.Nested(SimpleUserDetailSchema(), many=False)


chat_room_schema = ChatRoomDetailSchema(many=False)