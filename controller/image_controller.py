import pillow_heif

from fastapi import HTTPException, UploadFile
from PIL import Image
from io import BytesIO

from database.models import *
from database.base_model import DefaultModel
from config.constant import *
from config.s3 import *


def post_image_upload(session, request, g):
    response = DefaultModel()

    user = session.query(User).filter(User.id == g.id).first()
    if user is None:
        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                            detail=ERROR_DATA_NOT_EXIST)

    # 이미지 업로드
    if request.images is not None:
        if len(request.images) > 0:
            for image in request.images:
                file_data = image.filename.split('.')
                if len(file_data[0]) < 5:
                    name = file_data[0][:len(file_data)]
                else:
                    name = file_data[0][:5]

                if request.bucket == 'lesson':
                    bucket = f'lesson_{request.lesson_id}'
                else:
                    bucket = request.bucket

                filename = f'user_{g.id}_{bucket}_{name}'
                extension = file_data[1]

                if extension.upper() == 'HEIC':
                    heif_file = pillow_heif.read_heif(image.file.read())
                    img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, 'raw')
                else:
                    img = Image.open(BytesIO(image.file.read()))

                webp_data = BytesIO()
                img.save(webp_data, format='jpeg', quality=75)
                webp_data.seek(0)

                webp_upload_file = UploadFile(webp_data, filename=filename)

                # aws에 이미지 업로드
                file_path, image_url = upload_file(file=webp_upload_file,
                                                   bucket_folder=request.bucket,
                                                   object_name=filename)

                # 프로필 이미지
                if request.bucket == 'profile':
                    user.image_url = image_url
                else:  # 수업 썸네일, 수업 리뷰
                    lesson = session.query(Lesson).filter(Lesson.id == request.lesson_id).first()
                    if lesson is None:
                        raise HTTPException(status_code=ERROR_DIC[ERROR_DATA_NOT_EXIST][0],
                                            detail=ERROR_DATA_NOT_EXIST)

                    # 수업 썸네일
                    if request.bucket == 'lesson':
                        lesson.image_url = image_url


                response.result_data = {
                    'image_url': image_url,
                }
    return response