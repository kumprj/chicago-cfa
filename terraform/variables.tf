variable "twilio_account_sid" {
  description = "Value of the twilio account id."
  type        = string
  default     = "ExampleAppServerInstance"
}
variable "twilio_auth_token" {
  description = "Value of the twilio token."
  type        = string
  default     = "ExampleAppServerInstance"
}

variable "sender_number" {
  description = "Value of the twilio outbound number."
  type        = string
  default     = "ExampleAppServerInstance"
}
