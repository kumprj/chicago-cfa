

module "hawks_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name          = "blackhawks-cfa-texter"
  description            = "Lambda Function to send text alerts about free Chick-fil-a breakfast when the blackhawks score."
  handler                = "free_cfa.lambda_handler"
  runtime                = "python3.13"
  timeout                = 90
  create_package         = false
  maximum_retry_attempts = 0
  local_existing_package = "../package.zip" # Dummy zip to be updated via a Github Action
  # Have to re-add IAM role for dynamodb full read access
  environment_variables = {
    TWILIO_ACCOUNT_SID = var.twilio_account_sid
    TWILIO_AUTH_TOKEN  = var.twilio_auth_token
    SENDER_NUMBER      = var.sender_number
  }
}

