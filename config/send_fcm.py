import firebase_admin

from firebase_admin import credentials, messaging

from config.config import FCM_SERVICE_KEY


class FCM:
    def send(self, token, data):
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
