import boto3
from os import path
import os
import random
import shutil
import string
import pathlib
import jinja2
from pathlib import Path
from jinja2 import Template

ROOT_DIRECTORY = path.dirname(pathlib.Path(__file__))

SITE_CONFIGURATION = {
    "ErrorDocument": {"Key": "error.html"},
    "IndexDocument": {"Suffix": "index.html"},
}


def mksite_album(bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    url = f"https://{bucket}.website.yandexcloud.net"
    albums = get_albums_data(s3, bucket)

    template = get_template("album.html")

    albums_rendered = []
    i = 1
    for album, photos in albums.items():
        print(photos)
        template_name = f"album{i}.html"
        rendered_album = Template(template).render(album=album, images=photos, url=url)
        path = save_temporary_template(rendered_album)

        s3.upload_file(path, bucket, template_name)
        albums_rendered.append({"name": template_name, "album": album})
        i += 1

    template = get_template("index.html")
    rendered_index = Template(template).render(template_objects=albums_rendered)
    path = save_temporary_template(rendered_index)
    s3.upload_file(path, bucket, "index.html")

    template = get_template("error.html")
    path = save_temporary_template(template)
    s3.upload_file(path, bucket, "error.html")

    s3.put_bucket_website(Bucket=bucket, WebsiteConfiguration=SITE_CONFIGURATION)
    remove_temporary_dir()
    print(url)


def get_albums_data(session, bucket: str):
    albums = {}
    list_objects = session.list_objects(Bucket=bucket)
    for key in list_objects["Contents"]:
        album_img = key["Key"].split("/")
        if len(album_img) != 2:
            continue
        album, img = album_img
        if img == '':
            continue
        if album in albums:
            albums[album].append(img)
        else:
            albums[album] = [img]

    return albums


def get_template(name):
    template_path = Path(ROOT_DIRECTORY) / "resources" / name
    with open(template_path, "r") as file:
        return file.read()


def save_temporary_template(template) -> str:
    filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".html"
    path = Path(ROOT_DIRECTORY) / "temp" / filename
    if not path.parent.exists():
        os.mkdir(path.parent)

    with open(path, "w") as file:
        file.write(template)

    return str(path)


def remove_temporary_dir():
    path = Path(ROOT_DIRECTORY) / "temp"
    shutil.rmtree(path)
