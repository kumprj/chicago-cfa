import boto3
import os

# Crawl the DynamoDB table for the users to message.
def getNameAndNumber():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("BlackhawksCfa")
    response = table.scan()
    nameList = []
    for i in response["Items"]:
        nameList.append((i["Name"], i["Phone"], i["Cubs"], i["Blackhawks"]))
    # print(nameList)
    return nameList


# For Local dev
def main():
    getNameAndNumber()


# For Local dev
if __name__ == "__main__":
    main()
