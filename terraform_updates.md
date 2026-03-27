# Terraform Updates for Cubs Schedule

## Replace existing Cubs scheduler with these two:

```terraform
resource "aws_scheduler_schedule" "cubs_4pm" {
  name       = "CubsCfaScheduler4pmTf"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 21 * * ? *)"  # 9 PM UTC = 4 PM Central

  target {
    arn      = "arn:aws:lambda:us-east-1:875660052076:function:cubs-cfa-texter"
    role_arn = "arn:aws:iam:us-east-1:875660052076:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_d214280288"
  }
}

resource "aws_scheduler_schedule" "cubs_9pm" {
  name       = "CubsCfaScheduler9pmTf"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 2 * * ? *)"  # 2 AM UTC = 9 PM Central (previous day)

  target {
    arn      = "arn:aws:lambda:us-east-1:875660052076:function:cubs-cfa-texter"
    role_arn = "arn:aws:iam:us-east-1:875660052076:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_d214280288"
  }
}
```

## Remove this existing scheduler:
```terraform
resource "aws_scheduler_schedule" "cubs" {
  name       = "CubsCfaSchedulerTf"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 3 * * ? *)"

  target {
    arn      = "arn:aws:lambda:us-east-1:875660052076:function:cubs-cfa-texter"
    role_arn = "arn:aws:iam:us-east-1:875660052076:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_d214280288"
  }
}
```

## DynamoDB Usage
The code will use the existing `ChickfilaData` table with:
- Key format: `cubs-YYYY-MM-DD` (e.g., `cubs-2025-03-26`)
- Fields: `text_sent`, `date`, `timestamp`
- Ensures only one text per day even with multiple runs
