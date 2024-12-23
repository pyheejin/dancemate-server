IS_DEPLOY = True
IS_REAL_SERVER = False

USER_TYPE_MATE = 1
USER_TYPE_DANCER = 50

ERROR_DATA_NOT_EXIST = 'data_not_exist'
ERROR_NAME_EXISTS = 'name_exists'
ERROR_EMAIL_EXISTS = 'email_exists'
ERROR_BAD_REQUEST = 'bad_request'
ERROR_UNAUTHORIZED = 'unauthorized'
ERROR_TOKEN_EXPIRED = 'token_expired'
ERROR_PROCESSING = 'processing_error'

ERROR_DIC = {
    ERROR_DATA_NOT_EXIST: (205, '데이터가 존재 하지 않습니다'),
    ERROR_NAME_EXISTS: (206, '중복된 이름입니다.'),
    ERROR_EMAIL_EXISTS: (207, '중복된 이메일입니다.'),
    ERROR_BAD_REQUEST: (400, '잘못된 요청입니다'),
    ERROR_UNAUTHORIZED: (401, '로그인이 필요합니다'),
    ERROR_TOKEN_EXPIRED: (404, '토큰이 만료되었습니다.'),
    ERROR_PROCESSING: (500, '처리 중 오류가 발생하였습니다.'),
}