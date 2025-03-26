module "cubs_lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "cubs-cfa-texter"
  description   = "Lambda Function to send text alerts about free Chick-fil-a sandwiches when the cubs win at home."
  handler       = "cubs.lambda_handler"
  runtime       = "python3.13"
  
  create_package         = false
  local_existing_package = "../package.zip" # Dummy zip to be updated via a Github Action

}