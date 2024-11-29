terraform {
  backend "s3" {
    bucket = "blackhawks-cfa-statefiles"
    key = "global/s3/state-files/blackhawks-cfa-texter/terraform.tfstate"
    region = "us-east-1"
    dynamodb_table = "terraform-state-lock-dynamo"
    encrypt = true
  }
}