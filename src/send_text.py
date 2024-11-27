from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

def send_text(goal_result):
    if goal_result == True:
        message = client.messages.create(
            body="This is the ship that made the Kessel Run in fourteen parsecs?",
            from_="+15017122661",
            to="+15558675310",
        )
    # Else no free chimkin :(

# numbers_to_message = ['+15558675310', '+14158141829', '+15017122661']
# for number in numbers_to_message:
#     client.messages.create(
#         body='Hello from my Twilio number!',
#         from_='+15017122662',
#         to=number
#     )