import pytest
from flask import Flask
import json
from view import app



def command_test(client, text, expected_result, expected_response):
    """
    generic function which get a message text, expected answer from bot and expected response from the url function
    and check assert if the expected results are the same as the actual.
    :param client: the client which sends the message
    :param text: the context of the message
    :param expected_result: what the bot should responds
    :param expected_response: what the functions should returns ("success" or "failure")
    :return: nothing
    """
    chat_id = 913511633
    results = json.loads(client.post('/message',
                                     json={"message": {"chat": {"id": chat_id}, "text": text}}).data.decode())
    assert (results['response'] == expected_response
            and results['text'] == expected_result)


def test_prime(app_client):
    """
    tests on command: prime
    :param app_client: fixture function returns the application client instance
    :return: nothing
    """
    command_test(app_client, "/prime 6", 'Come on dude, you know even numbers are not prime!', 'success')
    command_test(app_client, "/prime 5", 'prime', 'success')
    command_test(app_client, "/prime 0", 'not prime', 'success')
    command_test(app_client, "/prime 15", 'not prime', 'success')
    command_test(app_client, "/prime -5", 'not prime', 'success')
    command_test(app_client, "/prime ",
                 "/prime's value input is missing.\ncommand for example: /prime 13", 'failure')
    command_test(app_client, "/prime minister",
                 "'minister' is not a valid input.\nusage for example: /prime 7", 'failure')
    command_test(app_client, "/prime 1 12",
                 '/prime has more than one input param. should have only one', 'failure')


def test_factorial(app_client):
    """
    tests on command: factorial
    :param app_client: fixture function returns the application client instance
    :return: nothing
    """
    command_test(app_client, "/factorial 6", 'factorial', 'success')
    command_test(app_client, "/factorial 0", 'not factorial', 'success')
    command_test(app_client, "/factorial 12", 'not factorial', 'success')
    command_test(app_client, "/factorial -5", 'not factorial', 'success')
    command_test(app_client, "/factorial ",
                 "/factorial's value input is missing.\ncommand for example: /factorial 13", 'failure')
    command_test(app_client, "/factorial banana",
                 "'banana' is not a valid input.\nusage for example: /factorial 7", 'failure')
    command_test(app_client, "/factorial 1 1",
                 '/factorial has more than one input param. should have only one', 'failure')


def test_palindrome(app_client):
    """
    tests on command: palindrome
    :param app_client: fixture function returns the application client instance
    :return: nothing
    """
    command_test(app_client, "/palindrome 6", 'palindrome', 'success')
    command_test(app_client, "/palindrome 0", 'palindrome', 'success')
    command_test(app_client, "/palindrome 123767321", 'palindrome', 'success')
    command_test(app_client, "/palindrome 76776", 'not palindrome', 'success')
    command_test(app_client, "/palindrome 00100", 'not palindrome', 'success')
    command_test(app_client, "/palindrome -123767321", 'not palindrome', 'success')
    command_test(app_client, "/palindrome ",
                 "/palindrome's value input is missing.\ncommand for example: /palindrome 13", 'failure')
    command_test(app_client, "/palindrome potato",
                 "'potato' is not a valid input.\nusage for example: /palindrome 7", 'failure')
    command_test(app_client, "/palindrome 121 787",
                 '/palindrome has more than one input param. should have only one', 'failure')


def test_sqrt(app_client):
    """
    tests on command: sqrt
    :param app_client: fixture function returns the application client instance
    :return: nothing
    """
    command_test(app_client, "/sqrt 9", 'sqrt', 'success')
    command_test(app_client, "/sqrt 4", 'sqrt', 'success')
    command_test(app_client, "/sqrt 0", 'sqrt', 'success')
    command_test(app_client, "/sqrt 8", 'not sqrt', 'success')
    command_test(app_client, "/sqrt 014", 'not sqrt', 'success')
    command_test(app_client, "/sqrt -4", 'not sqrt', 'success')
    command_test(app_client, "/sqrt ",
                 "/sqrt's value input is missing.\ncommand for example: /sqrt 13", 'failure')
    command_test(app_client, "/sqrt potato",
                 "'potato' is not a valid input.\nusage for example: /sqrt 7", 'failure')
    command_test(app_client, "/sqrt 4 16",
                 '/sqrt has more than one input param. should have only one', 'failure')


@pytest.fixture
def app_client():
    """
    function that returns the application client instance
    :return: the application client instance
    """
    return app.test_client()
