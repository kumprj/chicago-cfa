import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand, DeleteCommand } from "@aws-sdk/lib-dynamodb";
// Download the helper library from https://www.twilio.com/docs/node/install
// const twilio = require("twilio"); // Or, for ESM: import twilio from "twilio";
import twilio from "twilio";
// Find your Account SID and Auth Token at twilio.com/console
// and set the environment variables. See http://twil.io/secure
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const client = twilio(accountSid, authToken);

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

    if (action === "Add My Number") {
      const params = {
        TableName: TABLE_NAME,
        Item: { Name: name, SK: "GRP1#" + phone, Phone: phone, Blackhawks: "true" },
      };
      await dynamoDb.send(new PutCommand(params));
      createMessage(phone);
    } else if (action === "Delete My Number") {
      const deleteParams = {
        TableName: TABLE_NAME,
        Key: {
          Name: name,
          SK: "GRP1#" + phone,
        },
      };
      await dynamoDb.send(new DeleteCommand(deleteParams));
      deleteMessage(phone);
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

async function createMessage(phone) {
  console.log("got here create");
  const message = client.messages.create({

    body: "You're in for Blackhawks Chick-fil-a breakfast alerts! Reply STOP to unsubscribe. Msg&Data Rates May Apply",

    from: "+15138668921",

    to: "+1" + phone,

  })
    .then(message => console.log('Message sent: ', message.status));


  // console.log("You're in for Blackhawks Chick-fil-a breakfast alerts! Reply HELP for help. Reply STOP to unsubscribe. Msg&Data Rates May Apply");

}

async function deleteMessage(phone) {
  console.log("got here delete");
  const message = client.messages.create({

    body: "Your data has been successfully deleted from the database. Reply HELP for help. Reply STOP to unsubscribe. Msg&Data Rates May Apply",

    from: "+15138668921",

    to: "+1" + phone,

  }).then(message => console.log('Message sent: ', message.status));


  // console.log("Your data has been successfully deleted from the database. Reply HELP for help. Reply STOP to unsubscribe. Msg&Data Rates May Apply");

}

