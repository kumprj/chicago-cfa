# blackhawks-cfa
Text alerts if the Blackhawks or Cubs got us free chick fil a by scoring in the first period of a home game or winning a home baseball game. App hosted on AWS with API Gateway, Lambda, and DynamoDB.

# Terraform Scripts
https://github.com/kumprj/terraform-cfa

# Frontend
The frontend folder contains a single page HTML with some small javascript code to send the data entered to API Gateway. It is hosted on S3 as a static webpage.

# Backend
The backend is triggered when a user submits to add their data. It is a NodeJS Lambda that handles the API Gateway request. It receives a JSON Object ('body') which is then parsed to determine to load the user into the database.

# src
Python src code. This handles the NHL API requests and text message sends. `get_name_and_number` fetches the names and phone numbers to text message. `send_text` iterates through this list and sends it out. `free_cfa `is what queries the NHL api and determines if we need to send the text at all based on the NHL information. Lastly, has a `cubs.py` file that queries the MLB API and determines if the Cubs were winners at home. Uses `send_text` to alert if so. 


### GitHub Actions configured to deploy:
* Python Lambda which runs the check against NHL API and checks if the Hawks are at home. This is managed with Terraform.
* Python Lambda which runs the check against MLB API and checks if the Cubs win at home. This is managed with Terraform.
* Backend API Gateway lambda which loads the user's data to DynamoDB. The lambda is managed by GitHub actions but the API Gateway was manually configured.
* Front end hosted in S3 - this is a simple aws s3 cp of the file.
  
