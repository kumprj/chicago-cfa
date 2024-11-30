# blackhawks-cfa
Text alerts if the Blackhawks got us free chick fil a. 

GitHub Actions configured to deploy:
* Python Lambda which runs the check against NHL API and checks if the Hawks are at home.
* Backend API Gateway lambda which loads the user's data to DynamoDB.
* Front end hosted in S3.


TODO Item in:
* Review python code - 
*   Test whether it is successfully querying DynamoDB with scan (feel good about the loop, just need to query)
*   Test as a lambda
*   Schedule the lambda
* Add delete Logic to remove self from database
* Configure CloudFront distribution so that URL looks nicer -> look up how to do this properly
* Verify Twilio status and campaign so texts can send
