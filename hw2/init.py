import boto3
from botocore.client import ClientError


def make_bucket(bucket_name, aws_access_key, aws_secret_access_key, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' exists.")
    except ClientError as e:
        s3.create_bucket(Bucket=bucket_name, ACL='public-read')
