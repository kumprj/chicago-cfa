import boto3
import json

def getNameAndNumber():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BlackhawksCfa')
    response = table.scan()

    nameList = []
    for i in response['Items']:
        nameList.append(i['Name'])
    return nameList

def main():
    getNameAndNumber()

if __name__ == "__main__":
    main()
