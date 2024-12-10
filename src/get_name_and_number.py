import boto3
import os
# account_sid = os.environ["AWS_ACCESS_KEY_ID"]
# auth_token = os.environ["AWS_SECRET_ACCESS_KEY"]

# Crawl the DynamoDB table for the users to message.
def getNameAndNumber():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BlackhawksCfa')
    response = table.scan()
    nameList = []
    for i in response['Items']:
        nameList.append((i['Name'], i['Phone']))
    # print(nameList)
    return nameList

# For Local dev
def main():
    getNameAndNumber()
# For Local dev
if __name__ == "__main__":
    main()
