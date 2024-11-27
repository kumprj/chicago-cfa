from src.get_name_and_number import getNameAndNumber
from twilio.rest import Client
import os

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def send_text(goal_result):
    if goal_result == True:
        nameList = []
        nameList = getNameAndNumber()
        for name, number in nameList:
            safeNumber = polish_number(number)
            client.messages.create(
                body=f"Good morning {name}! Free Chick-fil-a has landed in your CFA App",
                from_="+18559770899",
                to="+1" + number,
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
