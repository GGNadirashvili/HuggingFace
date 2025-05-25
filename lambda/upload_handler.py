import boto3
import base64
import uuid
import os
from requests_toolbelt.multipart import decoder
from urllib.parse import parse_qs

s3 = boto3.client("s3")
BUCKET_NAME = "huggingface-image-upload"  

def parse_form_data(event):
    content_type = event['headers'].get('content-type') or event['headers'].get('Content-Type')
    if not content_type:
        raise Exception("Missing content-type header")

    body = base64.b64decode(event['body']) if event.get('isBase64Encoded', False) else event['body']
    multipart_data = decoder.MultipartDecoder(body, content_type)

    file_content = None
    filename = None
    model_name = None

    for part in multipart_data.parts:
        disposition = part.headers.get(b'Content-Disposition', b'').decode()
        if 'name="image"' in disposition:
            file_content = part.content
            if 'filename=' in disposition:
                filename = disposition.split('filename=')[1].strip('"')
        elif 'name="model"' in disposition:
            model_name = part.text

    if not all([file_content, filename, model_name]):
        raise Exception("Missing image, filename, or model")

    return file_content, filename, model_name

def lambda_handler(event, context):
    try:
        file_content, filename, model_name = parse_form_data(event)

        key = f"uploads/{uuid.uuid4()}_{model_name.replace('/', '-')}_{filename}"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=file_content,
            Metadata={"model": model_name}
        )

        return {
            "statusCode": 200,
            "body": f"Image uploaded successfully to {key}"
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }
