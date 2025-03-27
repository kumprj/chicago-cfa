

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
  # Have to re-add Env vars and IAM role
}

