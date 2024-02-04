import boto3
import json
import logging
from constants import ENCRYPTED_IDENTIFIER, DECRYPT_S3_BUCKET_NAME

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')


def lambda_handler(event, context):
    logger.info(f"Event: {event}")
    source_bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    if ENCRYPTED_IDENTIFIER not in object_key:
        logger.warning(f"Invalid file name or file does not follow the approved naming convention: {object_key}")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid file name or file does not follow the approved naming convention.')
        }

    try:
        destination_object_key = object_key

        logger.info(f"Copying file: {object_key} from bucket: {source_bucket_name} to bucket: {DECRYPT_S3_BUCKET_NAME}")
        copy_source = {
            'Bucket': source_bucket_name,
            'Key': object_key
        }
        s3.copy_object(CopySource=copy_source, Bucket=DECRYPT_S3_BUCKET_NAME, Key=destination_object_key)

        logger.info(f"File successfully copied to {DECRYPT_S3_BUCKET_NAME}/{destination_object_key}")
        return {
            'statusCode': 200,
            'body': json.dumps(f'File successfully copied to {DECRYPT_S3_BUCKET_NAME}/{destination_object_key}')
        }
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(str(e))}
