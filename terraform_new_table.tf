# New DynamoDB table for tracking sent notifications
resource "aws_dynamodb_table" "chickfila-sent-notifications" {
  name           = "ChickFilADataSent"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "NotificationKey"

  attribute {
    name = "NotificationKey"
    type = "S"
  }

  tags = {
    Name        = "chickfila-sent-notifications"
    Environment = "production"
  }
}
