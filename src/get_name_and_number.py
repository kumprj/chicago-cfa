import boto3
import json
import os
# account_sid = os.environ["AWS_ACCESS_KEY_ID"]
# auth_token = os.environ["AWS_SECRET_ACCESS_KEY"]

def getNameAndNumber():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BlackhawksCfa')
    response = table.scan()
    nameList = []
    for i in response['Items']:
        nameList.append((i['Name'], i['Phone']))
    print(nameList)
    return nameList

def main():
    getNameAndNumber()

if __name__ == "__main__":
    main()
