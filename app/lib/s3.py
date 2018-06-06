import os

import boto3


def upload_file_to_s3(path, key):
    """Uploads a file to s3."""
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['S3_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY'],
    )
    s3.upload_file(path, os.environ['S3_BUCKET_NAME'], key)
