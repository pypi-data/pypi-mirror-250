import io
import logging

import boto3
from botocore.exceptions import ClientError

from schedulesy_qrcode.config import S3_CONF
from schedulesy_qrcode.generate import multi

logger = logging.getLogger(__name__)


class S3_client:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=S3_CONF['access_key'],
            aws_secret_access_key=S3_CONF['secret_key'],
            endpoint_url=S3_CONF['endpoint'],
        )

        self.bucket = S3_CONF['bucket']

        response = self.client.list_buckets()

        if self.bucket in [b["Name"] for b in response["Buckets"]]:
            logger.info(f"🪣 Bucket {self.bucket} already exists")
        else:
            logger.info(f"🪣 Creating bucket {self.bucket}")
            self.client.create_bucket(Bucket=self.bucket)
            self.client.put_bucket_cors(
                Bucket=self.bucket,
                CORSConfiguration={
                    "CORSRules": [
                        {
                            "AllowedMethods": ["GET", "HEAD"],
                            "AllowedOrigins": [
                                "*",
                            ],
                            "ExposeHeaders": ["*"],
                            "AllowedHeaders": ["Content-Type", "Authorization"],
                        }
                    ]
                },
            )

    def upload(self, content, filename, mime_type):
        logger.info(f"⬆️ Uploading file {filename}")
        self.client.upload_fileobj(
            content,
            self.bucket,
            filename,
            ExtraArgs={
                "ContentType": mime_type,
                "ACL": "public-read",
            },
        )

    def get(self, filename):
        logger.info(f"⬇️ Downloading {filename}")
        output = io.BytesIO()
        self.client.download_fileobj(self.bucket, filename, output)
        return output.getvalue()

    def exists(self, filename):
        try:
            self.client.get_object_acl(Bucket=self.bucket, Key=filename)
        except ClientError as ex:
            return ex.response['Error']['Code'] != 'NoSuchKey'
        return True

    def clean(self, rooms):
        room_ids = [int(room["id"]) for room in rooms]
        for prefix in room_ids:
            response = self.client.list_objects(Bucket=self.bucket, Prefix=f'{prefix}-')
            # logger.info(f'{prefix}- {response}')
            if response.get('Contents') and len(response.get('Contents')) > 0:
                for filename in [
                    i['Key']
                    for i in response.get('Contents')
                    if i['Key'] != f'{multi(rooms)}.png'
                ]:
                    logger.info(f"🗑️ Removing {filename}")
                    self.client.delete_object(Bucket=self.bucket, Key=filename)
