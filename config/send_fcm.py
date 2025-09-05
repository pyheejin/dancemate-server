import firebase_admin

from firebase_admin import credentials, messaging

from config.config import FCM_SERVICE_KEY


class FCM:
    def send_push(self, token, data):
        if not firebase_admin._apps:
            cred = credentials.Certificate(FCM_SERVICE_KEY)
            firebase_admin.initialize_app(cred)

            message = messaging.Message(
                # ios
                notification=messaging.Notification(
                    title=data['title'],
                    body=data['body']
                ),
                # android
                data={
                    'title': data['title'],
                    'body': data['body'],
                    'score': '850',
                    'time': '2:45',
                },
                token=token,
            )

            try:
                response = messaging.send(message)
                print('Successfully sent message:', response)
            except Exception as e:
                print('Error sending message:', e)


    def send_bulk_push(self, token_list, data):
        if not firebase_admin._apps:
            cred = credentials.Certificate(FCM_SERVICE_KEY)
            firebase_admin.initialize_app(cred)

            # notification = messaging.Notification(
            #     title=data['title'],
            #     body=data['body']
            # )
            message = messaging.MulticastMessage(
                tokens=token_list,
                # ios
                notification=messaging.Notification(
                    title=data['title'],
                    body=data['body']
                ),
                # android
                data={
                    'title': data['title'],
                    'body': data['body'],
                    'score': '850',
                    'time': '2:45',
                },
            )

            try:
                response = messaging.send_each_for_multicast(message, dry_run=False)
                print('성공적으로 발송된 메시지 수:', response.success_count)
                print('실패한 메시지 수:', response.failure_count)
                print('Successfully sent message:', response)

                # 실패한 경우, 어떤 토큰이 문제였는지 확인할 수 있습니다.
                if response.failure_count > 0:
                    for resp in response.responses:
                        if not resp.success:
                            print(f'발송 실패 이유: {resp.exception}')
            except Exception as e:
                print('Error sending message:', e)
