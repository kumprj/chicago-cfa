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
table_name = "ChickfilaData"
phone_numbers_table = ddb_resource.Table(table_name)


# If there is a goal at home, this funtction executes and we alert the user.
def send_text(team, player_scoring):
    sender_number = outgoing_number
    nameList = []
    message = message_to_send(team, player_scoring)

    nameList = getNameAndNumber()

    for name, number, cubs, hawks in nameList:
        message_sent = f"Great news, {name}! {message}"
        safeNumber = polish_number(number)
        print(f"Sending to {name} at {safeNumber}")

        if verify_user(cubs, hawks, team) == False:
            continue

        twilio_msg_fire(message_sent, sender_number, safeNumber)


# Test these and phone number to ensure they are coming in as Strings.
def verify_user(cubs, hawks, team):
    if team == "Blackhawks" and hawks == "false":
        return False
    if team == "Cubs" and cubs == "false":
        return False
    return True


# Test phone number to ensure they are coming in as Strings.
def twilio_msg_fire(message_sent, sender_number, safeNumber):
    try:
        client.messages.create(
            body=message_sent,
            from_=sender_number,
            to="+1" + safeNumber,
        )
    except TwilioException as e:
        print(e.msg)
        print(e.code)
        # Twilio Unsubscribed error code is 21610.
        if e.code == 21610:
            print(f"Deleting {safeNumber} due to unsubscribing.")
            delete_data(safeNumber, safeNumber)


def message_to_send(team, player_scoring):
    text_factor_in_sunday = (
        "Today is Sunday - free sandwich is available for Monday."
        if is_sunday()
        else "Free sandwich has landed for tomorrow."
    )
    if team == "Blackhawks":
        return f"{player_scoring} scored in the first period at home. {text_factor_in_sunday}"
    elif team == "Cubs":
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
#     send_text(True)


# For Local dev
# if __name__ == "__main__":
#     main()
