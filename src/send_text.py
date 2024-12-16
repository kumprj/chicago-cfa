from get_name_and_number import getNameAndNumber
from twilio.rest import Client  # type: ignore
import os

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
outgoing_number = os.environ["SENDER_NUMBER"]
client = Client(account_sid, auth_token)


# If there is a goal at home, this funtction executes and we alert the user.
def send_text():
    sender_number = outgoing_number
    nameList = []
    nameList = getNameAndNumber()
    for name, number in nameList:
        safeNumber = polish_number(number)
        print(f"Sending to {name} at {safeNumber}")
        client.messages.create(
            body=f"Great news, {name}! Free Chick-fil-a breakfast has landed in your CFA App.",
            from_=sender_number,
            to="+1" + number,
        )


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
def main():
    send_text(True)


# For Local dev
if __name__ == "__main__":
    main()
