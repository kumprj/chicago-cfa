# blackhawks-cfa
Text alerts if the Blackhawks got us free chick fil a by scoring in the first period of a home game. App hosted on AWS with API Gateway, Lambda, and DynamoDB.



# Frontend
The frontend folder contains a single page HTML with some small javascript code to send the data entered to API Gateway.

# Backend
The backend is a NodeJS Lambda that handles the API Gateway request. It receives a JSON Object ('body') which is then parsed to determine if we have a DDB insert or delete.

# src
Python src code. This handles the NHL API requests and text message sends. `get_name_and_number` fetches the names and phone numbers to text message. `send_text` iterates through this list and sends it out. `free_cfa `is what queries the NHL api and determines if we need to send the text at all based on the NHL information.


### GitHub Actions configured to deploy:
* Python Lambda which runs the check against NHL API and checks if the Hawks are at home. This is managed with Terraform.
* Backend API Gateway lambda which loads the user's data to DynamoDB. The lambda is managed by GitHub actions but the API Gateway was manually configured.
* Front end hosted in S3 - this is a simple aws s3 cp of the file.

TODO Items:
* Review python code - 
  - Schedule the lambda
  - Add Env vars for Twilio in both places.
* Configure CloudFront distribution so that URL looks nicer -> look up how to do this properly
* Verify Twilio status and campaign so texts can send
