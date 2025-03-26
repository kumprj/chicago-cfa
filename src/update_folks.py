from get_name_and_number import getNameAndNumber
from twilio.rest import Client  # type: ignore
from twilio.base.exceptions import TwilioException  # type: ignore
import datetime
import os
import boto3

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
outgoing_number = os.environ["SENDER_NUMBER"]
client = Client(account_sid, auth_token)

ddb_resource = boto3.resource("dynamodb")
table_name = "BlackhawksCfa"
phone_numbers_table = ddb_resource.Table(table_name)


# If there is a goal at home, this funtction executes and we alert the user.
def send_text():
    sender_number = outgoing_number
    nameList = []

    nameList = getNameAndNumber()

    for name, number in nameList:
        message_sent = f"Interested in free chick-fil-a sandwiches when the Chicago Cubs win at home? Enter your name: {name} exactly as preceding on freethingsfrommyteam.com and check the toggle for both Cubs and Blackhawks."
        safeNumber = polish_number(number)
        print(f"Sending to {name} at {safeNumber}")
        # try:
        #     client.messages.create(
        #         body=message_sent,
        #         from_=sender_number,
        #         to="+1" + number,
        #     )
        # except TwilioException as e:
        #     print(e.msg)
        #     print(e.code)
        #     # Twilio Unsubscribed error code is 21610.
        #     if e.code == 21610:
        #         print(f"Deleting {name} due to unsubscribing.")
        #         delete_data(name, number)


def message_to_send(sport, player_scoring):
    text_factor_in_sunday = (
        "Today is Sunday - free sandwich is available for Monday."
        if is_sunday()
        else "Free sandwich has landed."
    )
    if sport == "hockey":
        return f"{player_scoring} scored in the first period at home. {text_factor_in_sunday}"
    elif sport == "baseball":
        return f"Cubs won at home! {text_factor_in_sunday}"
    else:
        return ""


def is_sunday():
    today = datetime.date.today()
    if today.weekday() == 6:  #  6 represents Sunday
        return True
    return False


def delete_data(name, number):
    dynamo_response = phone_numbers_table.delete_item(
        Key={"Name": name, "SK": "GRP1#" + number}
    )
    print(dynamo_response)


# Scrub the number of any +1 and hyphens (unlikely, but just in case).
def polish_number(number):
    new_number = ""

    if "+1" and "-" in number:
        new_number2 = number.replace("+1", "")
        new_number = new_number2.replace("-", "")
    elif "+1" in number:
        new_number = number.replace("+1", "")
    elif "-" in number:
        new_number = number.replace("-", "")
    else:
        new_number = number

    return new_number


# For Local dev
# def main():
#     send_text()


# For Local dev
# if __name__ == "__main__":
#     main()
