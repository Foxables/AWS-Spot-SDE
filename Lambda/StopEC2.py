import boto3
from includes.dynamo import *

region = 'ap-southeast-2'
instances = ['i-00913b8e800294465']
DYNAMO_TABLE = 'InstanceList'
SESSION=boto3.Session()
ec2 = SESSION.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
    for instance in instances:
        try:
            addDynamoItem(DYNAMO_TABLE, instance, SESSION)
        except Exception as e:
            print(str(e))

    return 'Complete'