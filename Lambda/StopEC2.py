import boto3, os
from includes.dynamo import *

REGION = 'ap-southeast-2' if os.environ.get('REGION') is None else os.environ.get('REGION')
TARGET_TAG=os.environ.get('TARGET_TAG')
DYNAMO_TABLE=os.environ.get('DYNAMO_TABLE')

SESSION=boto3.Session()

ec2 = SESSION.client('ec2', region_name=REGION)

def get_all_instances_with_tag():
    instances = []
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance["Tags"]:
                if tag["Name"] == TARGET_TAG:
                    instances.append(instance["InstanceId"])
    return instances

def lambda_handler(event, context):
    instances = get_all_instances_with_tag()
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
    for instance in instances:
        try:
            addDynamoItem(DYNAMO_TABLE, instance, SESSION)
        except Exception as e:
            print(str(e))

    return 'Complete'