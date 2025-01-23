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


class SimpleCourseListSchema(Schema):
    id = fields.Int()
    title = fields.String()
    image_url = fields.String()

    dancer = fields.Nested(UserListSchema(), many=False)


class CourseDetailSchema(Schema):
    id = fields.Int()
    title = fields.String()
    course_date = fields.DateTime('%m/%d')

    course = fields.Nested(SimpleCourseListSchema(), many=False)


course_detail_schema = CourseDetailSchema(many=True)


class CourseListSchema(Schema):
    id = fields.Int()
    title = fields.String()
    image_url = fields.String()
    user_id = fields.Int()
    count = fields.Int()
    last_course_date = fields.DateTime('%m/%d')

    dancer = fields.Nested(UserListSchema(), many=False)
    course_detail = fields.Nested(CourseDetailSchema(), many=True)


course_list_schema = CourseListSchema(many=True)


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
    last_course_date = fields.DateTime('%m/%d')

    dancer = fields.Nested(UserListSchema(), many=False)


search_course_list_schema = SearchCourseListSchema(many=True)


class SearchCourseDetailSchema(Schema):
    id = fields.Int()
    title = fields.String()
    course_date = fields.DateTime('%m/%d')

    course = fields.Nested(SearchCourseListSchema(), many=False)


search_course_detail_schema = SearchCourseDetailSchema(many=True)


class UserCourseSchema(Schema):
    id = fields.Int()
    status = fields.Int()
    course_detail_id = fields.Int()

    course_detail = fields.Nested(CourseDetailSchema(), many=False)


class UserDetailSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()
    introduction = fields.String()
    image_url = fields.String()

    reserve_course = fields.Nested(UserCourseSchema(), many=True)


user_detail_schema = UserDetailSchema(many=False)