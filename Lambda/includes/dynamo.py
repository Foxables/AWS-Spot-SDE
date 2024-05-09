from includes.utilities import epoch, remapDynamoResponse

dynamoClient=None

def initiateClientSession(SESSION):
    global dynamoClient
    if dynamoClient is None:
        dynamoClient = SESSION.resource('dynamodb', region_name="ap-southeast-2") # Create new DynamoDB Client.

    return dynamoClient

def getAllDynamoItems(DYNAMO_TABLE, SESSION=None):
    table = initiateClientSession(SESSION).Table(DYNAMO_TABLE)

    response = table.scan()
    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return remapDynamoResponse(items)

def addDynamoItem(DYNAMO_TABLE, instanceId, SESSION=None):
    response = initiateClientSession(SESSION).Table(DYNAMO_TABLE).put_item(
        Item={
            'instanceId': instanceId,
            'LastUpdated': epoch(),
            'Expiration': epoch() + 300, # 5 minutes from now.
        }
    )

    print("Info: Added InstanceId {} to DynamoDB - {}".format(instanceId, response))