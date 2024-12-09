from get_name_and_number import getNameAndNumber
from twilio.rest import Client # type: ignore
import os

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def send_text(goal_result):
    sender_number = '+15138668921'
    if goal_result == True:
        nameList = []
        nameList = getNameAndNumber()
        for name, number in nameList:
            safeNumber = polish_number(number)
            print(f'Sending to {name} at {safeNumber}')
            client.messages.create(
                body=f"Good morning {name}! Free Chick-fil-a breakfast has landed in your CFA App.",
                from_=sender_number,
                to="+1" + number
            )

def polish_number(number):
    new_number = ''

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


def main():
    send_text()


if __name__ == "__main__":
    main()
