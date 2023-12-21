import boto3
from pathlib import Path

IMG_EXTENSIONS = [".jpg", ".jpeg"]


def upload_album(bucket, aws_access_key_id, aws_secret_access_key, album, path, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    path = Path(path)

    if album.count("/"):
        raise Exception("album cannot contain '/'")
    count = 0

    if not path.is_dir():
        raise Exception(f"{str(path)} album does not exist")

    if not is_album_exist(s3, bucket, album):
        s3.put_object(Bucket=bucket, Key=(album + '/'))
        print(f"{album} album creating...")

    for file in path.iterdir():
        if is_image(file):
            try:
                print(f"{file.name} photo uploading...")
                key = f"{album}/{file.name}"
                s3.upload_file(str(file), bucket, key)
                count += 1
            except Exception as ex:
                raise Exception(f"{str(path)} got error with uploading")


def is_image(file):
    return file.is_file() and file.suffix in IMG_EXTENSIONS


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
