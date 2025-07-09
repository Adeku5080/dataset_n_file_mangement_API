import boto3
from uuid import uuid4
from app.file.schemas import CompleteUploadModel
import os
from dotenv import load_dotenv

load_dotenv()

# Global S3 client
s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def start_upload(filename: str):
    key = f"uploads/{uuid4()}_{filename}"
    response = s3_client.create_multipart_upload(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        Key=key
    )
    return {"upload_id": response["UploadId"], "key": key}


def generate_part_url(key: str, upload_id: str, part_number: int):
    """
    Generates a presigned URL for uploading a specific part of a file.
    """
    url = s3_client.generate_presigned_url(
        "upload_part",
        Params={
            "Bucket": os.getenv("AWS_BUCKET_NAME"),
            "Key": key,
            "UploadId": upload_id,
            "PartNumber": part_number
        },
        ExpiresIn=3600
    )
    return {"url": url}


def complete_upload(data: CompleteUploadModel):
    """
    Completes the multipart upload by assembling the uploaded parts.
    """
    parts = sorted(
        [{"ETag": p.ETag, "PartNumber": p.PartNumber} for p in data.parts],
        key=lambda x: x["PartNumber"]
    )

    response = s3_client.complete_multipart_upload(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        Key=data.key,
        UploadId=data.upload_id,
        MultipartUpload={"Parts": parts}
    )
    return {"location": response["Location"]}
