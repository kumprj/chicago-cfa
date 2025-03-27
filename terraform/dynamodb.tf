resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "ChickfilaData"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "Phone"

  attribute {
    name = "Phone"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}