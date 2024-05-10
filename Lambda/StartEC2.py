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
    try:
        instances = get_all_instances_with_tag()
        lockedInstances = getAllDynamoItems(DYNAMO_TABLE, SESSION)
        print('Locked Instances: {}'.format(", ".join(lockedInstances)))

        intersecting = set(instances).intersection(lockedInstances)
        print('Intersecting Instances: {}'.format(", ".join(intersecting)))
        subtracted = list(set(instances) - set(intersecting))

        print('Subtracted Instances: {}'.format(", ".join(subtracted)))
        if len(intersecting) != 0:
            print("The following instances are locked and cannot be started... " + ", ".join(intersecting))

    except Exception as e:
        subtracted = []
        print(str(e))

    if len(subtracted) == 0:
        return 'Complete - No Action'

    try:
        ec2.start_instances(InstanceIds=subtracted)
        print('started your instances: ' + ", ".join(subtracted))
    except Exception as e:
        print('Could not start instances ' + ", ".join(subtracted))
        print(str(e))

    return 'Complete'