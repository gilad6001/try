from model import BotModelWrapper, Number


class BotController:
    """
    class represents the controller of the telegram bot,
    considering all the logical level in this class
    check if inputs are valid and raises exceptions with information accordingly to kind of invalidation.
    """
    @classmethod
    def get_command(cls, chat_id, command: str):
        # print(f'state now is {BotModelWrapper.get_all()}')
        if not command:
            raise Exception('command is empty.\ncommand for example: prime 13')

        command_separated = command.split()
        command_mapper = {'prime': is_prime,
                          'factorial': is_factorial,
                          'palindrome': is_palindrome,
                          'sqrt': is_sqrt}

        # COMMAND WITH 0 PARAMETERS
        if command_separated[0] == 'popular':
            if not BotModelWrapper.empty(chat_id):
                return BotModelWrapper.get_popular_from(chat_id)
            else:
                return "isPrimeBot's history for this user is empty"

        if not command_mapper.get(command_separated[0]):
            raise Exception(f"'/{command}' is not a valid command.\ncommand for example: /prime 13")

        # COMMAND WITH 1 PARAMETER
        if len(command_separated) <= 1:
            raise Exception(f"/{command_separated[0]}'s value input is missing."
                            f"\ncommand for example: /{command_separated[0]} 13")
        if len(command_separated) > 2:
            raise Exception(f"/{command_separated[0]} has more than one input param. should have only one")
        if not (command_separated[1].isnumeric()
                or (command_separated[1][0] == '-' and command_separated[1][1:].isnumeric())):
            raise Exception(f"'{command_separated[1]}'"
                            f" is not a valid input.\nusage for example: /{command_separated[0]} 7")

        value = int(command_separated[1])
        boolean_res = command_mapper.get(command_separated[0])(value)

        # ANSWER PART
        if command_separated[0] == 'prime' and not boolean_res and is_even(value):
            answer = "Come on dude, you know even numbers are not prime!"
        else:
            answer = ('not ' if not boolean_res else "") + command_separated[0]
        BotModelWrapper.insert(Number(number=value, chat_id=chat_id))
        return answer


def is_even(num: int):
    return num > 2 and num % 2 == 0


def is_prime(num: int):
    if num <= 0:
        return False
    if num > 1:
        for i in range(2, num // 2):
            if (num % i) == 0:
                return False
    return True


def is_factorial(num: int):
    if num <= 0:
        return False
    i = 1
    while num > 1:
        if num % i != 0:
            return False
        num /= i
        i += 1
    return True


def is_palindrome(num: int):
    if num < 0:
        return False
    str_num = str(num)
    for i in range(len(str_num) // 2):
        if not str_num[i] == str_num[-i - 1]:
            return False
    return True


def is_sqrt(num: int):
    return 0 <= num == int(num ** 0.5) * int(num ** 0.5)
