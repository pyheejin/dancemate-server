from marshmallow import Schema, fields


class TokenPayloadSchema(Schema):
    id = fields.Int()


token_payload_schema = TokenPayloadSchema(many=False)


class UserListSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()


user_list_schema = UserListSchema(many=True)


class UserDetailSchema(Schema):
    id = fields.Int()
    email = fields.String()
    nickname = fields.String()


user_detail_schema = UserDetailSchema(many=False)