resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "BlackhawksCfa2"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "Phone"
  range_key      = "Name"

  attribute {
    name = "Phone"
    type = "S"
  }

  attribute {
    name = "Name"
    type = "S"
  }


  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}