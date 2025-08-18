import firebase_admin
from firebase_admin import credentials, messaging

# 1. 다운로드한 서비스 계정 키 파일 경로를 지정합니다.
service_key = 'dance-mate-fc3af-firebase-adminsdk-fbsvc-6c05bb4dab.json'
cred = credentials.Certificate(service_key)
firebase_admin.initialize_app(cred)

# 2. 알림을 보낼 디바이스 토큰을 입력합니다.
registration_token = 'dD3Kx-wJPkengFc1BIxyIH:APA91bHD4E4fV3e0fmHk0p85H_i1O-tUykmR72ipKGNh1LID2rabhED2z0ZWrKhEAw0aV921yqkJ2Cp1VZ8TzfZendVrF6CdpdjTd87NH1m5zrPZUqGw7i0'

# 3. 알림 내용과 데이터를 구성합니다.
message = messaging.Message(
    notification=messaging.Notification(
        title='파이썬 테스트 알림',
        body='파이썬으로 보낸 FCM 알림입니다.'
    ),
    data={
        'score': '850',
        'time': '2:45',
    },
    token=registration_token,
)

# 4. 메시지를 보냅니다.
try:
    response = messaging.send(message)
    print('Successfully sent message:', response)
except Exception as e:
    print('Error sending message:', e)