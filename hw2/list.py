import boto3


def get_albums(bucket_name, aws_access_key, aws_secret_access_key, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    try:
        s3.list_objects(Bucket=bucket_name)['Contents']
    except:
        raise Exception("Bucket is empty")
    unique_albums = []
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        if key['Key'].endswith("/") and key['Key'].split("/")[0] not in unique_albums:
            unique_albums.append(key['Key'].split("/")[0])
    for value in unique_albums:
        print(value)


def get_files(bucket_name, aws_access_key, aws_secret_access_key, album, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.resource(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    my_bucket = s3.Bucket(bucket_name)
    count_objects = 0
    count_files = 0

    for my_bucket_object in my_bucket.objects.filter(Prefix=f'{album}/', Delimiter='/'):
        count_objects = count_objects + 1
        if my_bucket_object.key.endswith(".jpg") or my_bucket_object.key.endswith(".jpeg"):
            print(my_bucket_object.key.split(f'{album}/')[1])
            count_files = count_files + 1

    if count_objects == 0:
        raise Exception(f"{album} does not exist")
    if count_files == 0:
        raise Exception(f"{album} does not have files")
