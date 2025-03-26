

module "hawks_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "blackhawks-cfa-texter"
  description   = "Lambda Function to send text alerts about free Chick-fil-a breakfast when the blackhawks score."
  handler       = "free_cfa.lambda_handler"
  runtime       = "python3.13"
  
  create_package         = false
  local_existing_package = "../package.zip" # Dummy zip to be updated via a Github Action

}

