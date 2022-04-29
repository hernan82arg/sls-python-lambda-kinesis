# Monitoring: DD APM
# https://docs.datadoghq.com/serverless/installation/python/?tab=serverlessframework
import json
from enum import Enum
import random
import logging
import boto3
from ddtrace import tracer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class RateType(Enum):
    normal = 'NORMAL'
    high = 'HIGH'

@tracer.wrap()
def get_heart_rate(rate_type):
    if rate_type == RateType.normal:
        rate = random.randint(60, 100)
    elif rate_type == RateType.high:
        rate = random.randint(150, 200)
    else:
        raise TypeError
    return {'heartRate': rate, 'rateType': rate_type.value}

@tracer.wrap()
def generate(stream_name, kinesis_client):
    rnd = random.random()
    rate_type = RateType.high if rnd < 0.01 else RateType.normal
    heart_rate = get_heart_rate(rate_type)
    kinesis_client.put_record(
        StreamName=stream_name,
        Data=json.dumps(heart_rate),
        PartitionKey="partitionkey")
    logger.info('Sending data to kinesis succeed!')
    return heart_rate

def main(event, context):
    try:
        heartRate = generate('hdStream', boto3.client('kinesis'))
        body = {
            "message": "I've received your request and pushed some shit to kinesis!",
            "heartRate": heartRate,
            "input": event,
        }
        response = {"statusCode": 200, "body": json.dumps(body)}
        return response
    except Exception as e:
        logger.exception('Sending data to kinesis failed!')
        response = {"statusCode": 500, "body": str(e)}
        return response
