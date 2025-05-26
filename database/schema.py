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


class UserDetailSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()
    introduction = fields.String()
    image_url = fields.String()

    reserve_course = fields.Nested(UserCourseSchema(), many=True)
    mate_ticket = fields.Nested(UserTicketSchema(), many=True)


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
