import boto3

from fastapi import UploadFile

from config.config import *


def s3_connection():
    try:
        s3 = boto3.client(
            service_name='s3',
            region_name='ap-northeast-2',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_ACCESS_SECRET_KEY,
        )
    except Exception as e:
        print(e)
    else:
        print('s3 bucket connected!')
        return s3


def upload_file(file: UploadFile, bucket_folder, object_name=None):
    """
    file: 업로드 할 파일
    bucket: 업로드 될 버킷
    object_name: S3 객체 이름, 없으면 file_name 사용
    """
    s3 = s3_connection()

    bucket = 'dance-mate'
    s3_url = f'https://{bucket}.s3.ap-northeast-2.amazonaws.com/'

    # S3 객체 이름이 정의 되지 않으면, file.filename 사용
    if object_name is None:
        object_name = file.filename

    # 저장할 버킷 폴더 선택
    object_key = f"{bucket_folder}/{object_name}.webp"
    try:
        s3.upload_fileobj(
            file.file,
            bucket,
            object_key,
            ExtraArgs={
                'ContentType': 'image/jpg',
                'ACL': 'public-read'
            },
        )
    except Exception as e:
        print(e)
    else:
        file_path = f'{s3_url}{bucket_folder}/'
        image_url = f'{s3_url}{object_key}'
        return file_path, image_url
    return None, None
