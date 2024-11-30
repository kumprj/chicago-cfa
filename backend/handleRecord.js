import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand, DeleteCommand } from "@aws-sdk/lib-dynamodb";

// DynamoDB Configuration
const REGION = "us-east-1"; // Replace with your region
const TABLE_NAME = "BlackhawksCfa"; // Replace with your table name

// Create a DynamoDB Document Client
const dynamoDbClient = new DynamoDBClient({ region: REGION });
const dynamoDb = DynamoDBDocumentClient.from(dynamoDbClient);

export const handler = async (event) => {
  try {
    // Log the incoming event for debugging
    console.log("Event received:", JSON.stringify(event));

    // Parse and validate the request body
    if (!event.body) {
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Missing request body" }),
      };
    }

    let body;
    try {
      body = typeof event.body === "string" ? JSON.parse(event.body) : event.body;
    } catch (error) {
      console.error("Invalid JSON in body:", error);
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Invalid JSON format in request body" }),
      };
    }

    const { name, phone, action } = body;
    console.log("action is " + action);
    // Validate input fields
    if (!name || !phone) {
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Both 'name' and 'phone' are required fields" }),
      };
    }

    // // Construct the PutCommand parameters
    // const params = {
    //   TableName: TABLE_NAME,
    //   Item: { Name: name, SK: "GRP1#" + phone, Phone: phone },
    // };

    // // Perform the Put or Delete operation
    // if (action === "Add My Number") {
    //   await dynamoDb.send(new PutCommand(params));
    // } else {
    //   await dynamoDb.send(new DeleteCommand(params));
    // }
    if (action === "Add My Number") {
      console.log("got here add");
      const params = {
        TableName: TABLE_NAME,
        Item: { Name: name, SK: "GRP1#" + phone, Phone: phone },
      };
      await dynamoDb.send(new PutCommand(params));
    } else if (action === "Delete My Number") {
      console.log("got here delete");
      const deleteParams = {
        TableName: TABLE_NAME,
        Key: {
          Name: name,
          SK: "GRP1#" + phone,
        },
      };
      await dynamoDb.send(new DeleteCommand(deleteParams));
    } else {
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Invalid action specified" }),
      };
    }

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*", // Required for CORS support to work
        "Access-Control-Allow-Credentials": true // Required for cookies, authorization headers with HTTPS
      },
      body: JSON.stringify({ message: `${action} successful` }),
    };
  } catch (error) {
    console.error("Error inserting data:", error);

    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Internal Server Error", error: error.message }),
    };
  }
};