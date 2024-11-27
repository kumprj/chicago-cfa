const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
  try {
    const { name, phone } = JSON.parse(event.body);

    // Input validation
    if (!name || !phone) {
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Invalid input: Name and Phone are required" }),
      };
    }

    const params = {
      TableName: "BlackhawksCfa", // Replace with your table name
      Item: { Name: name, Phone: phone },
    };

    await dynamoDB.put(params).promise();

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Data inserted successfully" }),
    };
  } catch (error) {
    console.error("Error inserting data:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Failed to insert data" }),
    };
  }
};