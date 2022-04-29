# Monitoring: DD APM
# https://docs.datadoghq.com/serverless/installation/python/?tab=serverlessframework
import logging
import boto3
from botocore.exceptions import ClientError
from ddtrace import tracer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@tracer.wrap()
def main(event, context):
    try:
        stream_name='hdStream'
        kinesis_client=boto3.client('kinesis')
        response = kinesis_client.get_shard_iterator(
            StreamName=stream_name, ShardId='0',
            ShardIteratorType='LATEST')
        shard_iter = response['ShardIterator']
        record_count = 0
        while record_count < 10:
            response = kinesis_client.get_records(
                ShardIterator=shard_iter, Limit=10)
            shard_iter = response['NextShardIterator']
            records = response['Records']
            logger.info('Reading data from kinesis succeed!')
            logger.info("Got %s records.", len(records))
            record_count += len(records)
    except ClientError:
        logger.exception("Couldn't get records from stream %s.", stream_name)
        raise
