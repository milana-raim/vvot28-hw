# !pip install boto3
# !pip install jinja2

import argparse
import sys
import os
from functions import init, list, delete, download, upload, mksite


def main():
    parser = argparse.ArgumentParser(prog='cloudphoto')

    command_parser = parser.add_subparsers(title='command', dest='command')

    init_parser = command_parser.add_parser('init', help='Config program')

    upload_parser = command_parser.add_parser('upload', help='Upload photos')
    upload_parser.add_argument('--album', metavar='ALBUM', type=str, help='Album name', required=True)
    upload_parser.add_argument('--path', metavar='PHOTOS_DIR', type=str, default='.',
                               help='Path to photo directory',
                               required=False)

    download_parser = command_parser.add_parser('download', help="Download photos")
    download_parser.add_argument('--album', metavar='ALBUM', type=str, help='Photo album name', required=True)
    download_parser.add_argument('--path', metavar='PHOTOS_DIR', type=str, default='.',
                                 help='Path to photo directory',
                                 required=False)

    list_parser = command_parser.add_parser('list', help='List photos and albums')
    list_parser.add_argument('--album', metavar='ALBUM', type=str, help='Album name')

    delete_parser = command_parser.add_parser('delete', help='Delete album')
    delete_parser.add_argument('--album', metavar='ALBUM', type=str, help='Album name')
    delete_parser.add_argument('--photo', metavar='PHOTO', type=str, help='Photo name')

    mksite_parser = command_parser.add_parser('mksite', help='Make web site')

    args = parser.parse_args()

    try:
        if args.command == 'init':
            aws_access_key_id = input('aws_access_key_id == ')
            aws_secret_access_key = input('aws_secret_access_key == ')
            bucket_name = input('bucket_name == ')
            init(bucket_name, aws_access_key_id, aws_secret_access_key)
            print("init done")
            print("Exit with status 0")
            sys.exit(os.EX_OK)
        elif args.command == 'upload':
            album = args.album
            photo_dir = args.path if args.path else "."
            upload(album, photo_dir)
            print("upload done")
            print("Exit with status 0")
            sys.exit(os.EX_OK)
        elif args.command == 'download':
            album = args.album
            photo_dir = args.path if args.path else "."
            download(album, photo_dir)
            print("download done")
            print("Exit with status 0")
            sys.exit(os.EX_OK)
        elif args.command == 'list':
            list(args.album)
            print("list done")
            print("Exit with status 0")
            sys.exit(os.EX_OK)
        elif args.command == 'delete':
            delete(args.album, args.photo)
            print("delete done")
            print("Exit with status 0")
            sys.exit(os.EX_OK)
        elif args.command == 'mksite':
            mksite()
            print("mksite done")
            print("Exit with status 0")
            sys.exit(os.EX_OK)
    except Exception as err:
        print(f"Error: {err}")
        print("Exit with status 1")
        sys.exit(1)


if __name__ == "__main__":
    main()
