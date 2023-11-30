import boto3
import uuid
import json
import ydb
import ydb.iam
import os
import io
from PIL import Image
from io import BytesIO


def get_sqs_client():
    return boto3.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name = 'ru-central1'
    )


def get_s3_client():
    return boto3.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        region_name = 'ru-central1'
    )


def get_ydb_pool(db_endpoint, db_name):
    driver = ydb.Driver(
        endpoint=db_endpoint,
        database=db_name,
        credentials=ydb.iam.MetadataUrlCredentials(),
    )
    driver.wait(fail_fast=True, timeout=5)
    return ydb.SessionPool(driver)


def crop_image(image_data, x1, y1, x2, y2):
    image = Image.open(image_data)
    cropped_image = image.crop((x1, y1, x2, y2))
    cropped_image_data = io.BytesIO()
    cropped_image.save(cropped_image_data, format=image.format)
    return cropped_image_data.getvalue() 


def insert_photo_face(pool, table_name, key_id, origin_photo_key_id):
    def call(session):
        session.transaction(ydb.SerializableReadWrite()).execute(
            f"INSERT INTO {table_name} (key_id, origin_photo_key_id) VALUES ('{key_id}', '{origin_photo_key_id}');",
            commit_tx=True,
            settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
        )
        
    return pool.retry_operation_sync(call)


def handler(event, context):
    print('Start trigger face cut processing')

    db_endpoint = os.environ['DB_API_ENDPOINT']
    db_name = os.environ['DB_NAME']
    table_name = os.environ['TABLE_NAME']
    photos_bucket_id = os.environ['PHOTOS_BUCKET_ID']
    faces_bucket_id = os.environ['FACES_BUCKET_ID']
    
    sqs = get_sqs_client()
    s3 = get_s3_client()
    ydb_pool = get_ydb_pool(db_endpoint, db_name)
    
    for message in event['messages']:
        task = json.loads(message['details']['message']['body'])

        object_id = task['object_id']
        x1 = int(task['vertices'][0]['x'])
        y1 = int(task['vertices'][0]['y'])
        x2 = int(task['vertices'][2]['x'])
        y2 = int(task['vertices'][2]['y'])
    
        object_response = s3.get_object(Bucket=photos_bucket_id, Key=object_id)
    
        image_data = BytesIO(object_response['Body'].read())
        cropped_image_data = crop_image(image_data, x1, y1, x2, y2)
    
        new_object_id = str(uuid.uuid4()) + '.jpg'
        new_object_path = '/tmp/' + new_object_id

        s3.put_object(Bucket=faces_bucket_id, Key=new_object_id, Body=cropped_image_data, ContentType='image/jpeg')
        
        insert_photo_face(ydb_pool, table_name, new_object_id, object_id)


    return "OK"
