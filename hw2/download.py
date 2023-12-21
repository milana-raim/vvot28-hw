import boto3
from pathlib import Path


def download_album(bucket, aws_access_key_id, aws_secret_access_key, album, path, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    path = Path(path)
    if not is_album_exist(s3, bucket, album):
        raise Exception(f"Album {album} does not exist")

    if not path.is_dir():
        raise Exception(f"{str(path)} is not directory")

    list_object = s3.list_objects(Bucket=bucket, Prefix=album + '/', Delimiter='/')
    for key in list_object["Contents"]:
        if not key["Key"].endswith("/"):
            obj = s3.get_object(Bucket=bucket, Key=key["Key"])
            filename = Path(key['Key']).name

            filepath = path / filename
            with filepath.open("wb") as file:
                file.write(obj["Body"].read())


def is_album_exist(session, bucket, album):
    list_objects = session.list_objects(
        Bucket=bucket,
        Prefix=album + '/',
        Delimiter='/',
    )
    if "Contents" in list_objects:
        for _ in list_objects["Contents"]:
            return True
    return False
