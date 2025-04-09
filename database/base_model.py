from pydantic import BaseModel


class DefaultModel(BaseModel):
    result_code: int = 200
    result_msg: str = '성공'
    result_data: dict = {}

    class Config:
        orm_mode = True


class DefaultLoginModel(BaseModel):
    result_code: int = 200
    result_msg: str = '성공'
    user_id: int = 0
    access_token: str = ''
    refresh_token: str = ''

    class Config:
        orm_mode = True