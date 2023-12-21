import boto3


def delete_album(bucket_name, aws_access_key, aws_secret_access_key, album, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.resource(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    my_bucket = s3.Bucket(bucket_name)
    try:
        obj = s3.Object(bucket_name, f'{album}/').get()
        for my_bucket_object in my_bucket.objects.filter(Prefix=f'{album}/'):
            s3.Object(bucket_name, my_bucket_object.key).delete()
    except:
        raise Exception(f"Album '{album}' does not exist")


def delete_photo_in_album(bucket_name, aws_access_key, aws_secret_access_key, album, photo, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.resource(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    my_bucket = s3.Bucket(bucket_name)
    try:
        obj = s3.Object(bucket_name, f'{album}/').get()
    except:
        raise Exception(f"Album '{album}' does not exist")
    try:
        path = f'{album}/{photo}'
        obj = s3.Object(bucket_name, path).get()
        s3.Object(bucket_name, path).delete()
    except:
        raise Exception(f"Photo '{photo}' does not exist")
