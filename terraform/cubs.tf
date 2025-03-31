module "cubs_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name          = "cubs-cfa-texter"
  description            = "Lambda Function to send text alerts about free Chick-fil-a sandwiches when the cubs win at home."
  handler                = "cubs.lambda_handler"
  runtime                = "python3.13"
  timeout                = 90
  create_package         = false
  maximum_retry_attempts = 0
  local_existing_package = "../package.zip" # Dummy zip to be updated via a Github Action
  environment_variables = {
    TWILIO_ACCOUNT_SID = var.twilio_account_id
    TWILIO_AUTH_TOKEN  = var.twilio_auth_token
    SENDER_NUMBER      = var.sender_number
  }
  # Have to re-add Env vars and IAM role
  # with:
  # aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
  # aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
}
