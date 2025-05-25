import os
import json
import uuid
import boto3
from upload_handler import parse_form_data, query_huggingface

s3 = boto3.client("s3")
dynamodb = boto3.client("dynamodb")

BUCKET_NAME = "huggingface-image-upload"
DYNAMODB_TABLE = "huggingface-inference-results"
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")


def lambda_handler(event, context):
    try:
        image_bytes, model_id = parse_form_data(event)

        if not image_bytes or not model_id:
            return _response(400, {"error": "Missing 'image' or 'model'"})

        image_key = f"uploads/{uuid.uuid4()}.jpg"
        s3.put_object(Bucket=BUCKET_NAME, Key=image_key, Body=image_bytes)

        parsed_result = query_huggingface(image_bytes, model_id, HF_API_TOKEN)

        dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                "id": {"S": str(uuid.uuid4())},
                "model": {"S": model_id},
                "s3key": {"S": image_key},
                "result": {"S": json.dumps(parsed_result)}
            }
        )

        return _response(200, {
            "message": "Success",
            "result": parsed_result,
            "image_key": image_key
        })

    except Exception as e:
        print("ERROR:", str(e))
        return _response(500, {"error": str(e)})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
