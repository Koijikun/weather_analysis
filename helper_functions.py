import json
import datetime
def get_user_input(message):
    while True:
        try:
            user_input = int(input(message))
            return user_input
        except ValueError:
            print("Please only enter a valid integer.")


def get_string_input(message):
    return str(input(message))

def pretty_print(variable):
    return print(json.dumps(variable, indent=4, sort_keys=True))

def get_today():
    return int(json.loads(json.dumps({'date': datetime.date.today()}, default=str))['date'].replace("-", ""))