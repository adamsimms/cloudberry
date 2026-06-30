"""S3 upload logic for Cloudberry."""

from __future__ import annotations

import logging
from pathlib import Path

import boto3

logger = logging.getLogger("Cloudberry")


def create_s3_client(access_key: str, secret_key: str, region: str | None = None):
    session_kwargs = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
    }
    if region:
        session_kwargs["region_name"] = region
    return boto3.client("s3", **session_kwargs)


def build_object_key(prefix: str | None, filename: str) -> str:
    if prefix:
        return f"{prefix.strip('/')}/{filename}"
    return filename


def generate_presigned_url(
    s3_client,
    bucket: str,
    file_key: str,
    *,
    expires_in: int = 3600,
) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": file_key},
        ExpiresIn=expires_in,
    )


def push_picture_to_s3(
    s3_client,
    bucket: str,
    file_key: str,
    file_path: Path,
    *,
    make_public: bool = False,
    max_retries: int = 3,
) -> bool:
    upload_kwargs = {"ContentType": "image/jpeg"}
    if make_public:
        upload_kwargs["ACL"] = "public-read"

    for attempt in range(1, max_retries + 1):
        try:
            logger.info("Uploading to S3: s3://%s/%s from %s", bucket, file_key, file_path)
            s3_client.upload_file(str(file_path), bucket, file_key, ExtraArgs=upload_kwargs)
            logger.info("Uploaded to S3: s3://%s/%s", bucket, file_key)
            return True
        except Exception as exc:
            logger.error("S3 upload attempt %s/%s failed: %s", attempt, max_retries, exc)
            if attempt == max_retries:
                return False

    return False
