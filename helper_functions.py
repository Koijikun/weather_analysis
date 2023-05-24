

def get_user_input(message):
    while True:
        try:
            user_input = int(input(message))
            return user_input
        except ValueError:
            print("Please only enter a valid integer.")

@staticmethod
def get_string_input(message):
    return str(input(message))

@staticmethod
def pretty_print(variable):
    return print(json.dumps(variable, indent=4, sort_keys=True))