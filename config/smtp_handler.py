import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config.config import EMAIL, PASSWORD


class SMTP:
    def __init__(self):
        self.email = EMAIL
        self.password = PASSWORD

    def send_email(self, to_email, title, msg):
        with smtplib.SMTP('smtp.gmail.com') as connection:
            message = MIMEMultipart()

            # 메일 제목
            message['Subject'] = title
            message['To'] = to_email

            # 메일 본문 내용
            content = MIMEText(msg, 'plain')
            message.attach(content)

            connection.starttls()  # Transport Layer Security : 메시지 암호화
            connection.login(user=self.email, password=self.password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs=to_email,
                msg=message.as_string(),
            )
