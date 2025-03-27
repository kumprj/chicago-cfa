resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "ChickfilaData"
  billing_mode   = "PAY_PER_REQUEST"
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