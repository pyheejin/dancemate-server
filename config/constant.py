IS_DEPLOY = True
IS_REAL_SERVER = False

STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
STATUS_DELETED = -1

USER_TYPE_MATE = 1
USER_TYPE_DANCER = 50

ERROR_DATA_NOT_EXIST = 'data_not_exist'
ERROR_NAME_EXISTS = 'name_exists'
ERROR_EMAIL_EXISTS = 'email_exists'
ERROR_COURSE_RESERVE_EXISTS = 'course_reserve_exists'
ERROR_PAYMENT_TICKET_EXISTS = 'payment_ticket_exists'
ERROR_PAST_SESSION_CANNOT_BE_RESERVED = 'past_session_cannot_be_reserved'
ERROR_PAST_SESSION_CANNOT_BE_CANCELED = 'past_session_cannot_be_canceled'
ERROR_DANCER_ONLY = 'dancer_only'
ERROR_PAST_SESSION_CANNOT_BE_CREATED = 'past_session_cannot_be_created'
ERROR_BAD_REQUEST = 'bad_request'
ERROR_UNAUTHORIZED = 'unauthorized'
ERROR_TOKEN_EXPIRED = 'token_expired'
ERROR_PROCESSING = 'processing_error'

ERROR_DIC = {
    ERROR_DATA_NOT_EXIST: (205, '데이터가 존재 하지 않습니다'),
    ERROR_NAME_EXISTS: (206, '중복된 이름입니다.'),
    ERROR_EMAIL_EXISTS: (207, '중복된 이메일입니다.'),
    ERROR_COURSE_RESERVE_EXISTS: (208, '이미 예약한 회차입니다.'),
    ERROR_PAYMENT_TICKET_EXISTS: (209, '이미 결제한 티켓입니다.'),
    ERROR_PAST_SESSION_CANNOT_BE_RESERVED: (210, '지난 회차는 예약할 수 없습니다.'),
    ERROR_PAST_SESSION_CANNOT_BE_CANCELED: (211, '지난 수업은 취소할 수 없습니다.'),
    ERROR_DANCER_ONLY: (212, '댄서 유저만 이용할 수 있습니다.'),
    ERROR_PAST_SESSION_CANNOT_BE_CREATED: (213, '날짜를 확인해주세요.'),
    ERROR_BAD_REQUEST: (400, '잘못된 요청입니다'),
    ERROR_UNAUTHORIZED: (401, '로그인이 필요합니다'),
    ERROR_TOKEN_EXPIRED: (404, '토큰이 만료되었습니다.'),
    ERROR_PROCESSING: (500, '처리 중 오류가 발생하였습니다.'),
}