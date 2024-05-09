import boto3
from includes.dynamo import *

region = 'ap-southeast-2'
instances = ['i-00913b8e800294465']
DYNAMO_TABLE='InstanceList'

SESSION=boto3.Session()
ec2 = SESSION.client('ec2', region_name=region)

def lambda_handler(event, context):
    try:
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