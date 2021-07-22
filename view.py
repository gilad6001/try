import flask
import json
from pip._vendor import requests
from controller import BotController
from logger import Logger

# get url from ngrok ("ngrok http 5002") #
TOKEN = '1871680584:AAF0AGe7b5zxfJ8qWNeCbcCB_qdKgcEwRmo'
WEBHOOK_URL = 'https://c27271535fb3.ngrok.io/message'
TELEGRAM_INIT_WEBHOOK_URL = \
    'https://api.telegram.org/bot{}/setWebhook?url={}'.format(TOKEN, WEBHOOK_URL)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)
isPrimeBot_username = 'gokamanaganbot'
app = flask.Flask(__name__)
app.secret_key = b'd5%Xds\t3ss\n^^d271sc]/'


@app.route('/sanity')
def sanity():
    return "Server is running"


@app.route('/')
def index():
    return "Main root active"


@app.route('/message', methods=["POST"])
def handle_message() -> flask.Response:
    """
    function represents the message handler, receives a message from a user and reply,
    it's check if it's a legal command and if so it responds with a boolean answer,
    example: "/palindrome 123" will answer "not palindrome"
    :return: if the command was legal returns "success", else: "failure"
    """
    print("got message")
    answer = ""
    Logger.get().debug(f'data:{flask.request.data}')
    try:
        message_as_json = flask.request.get_json()
        if message_as_json.get('message'):
            message_content = message_as_json['message']
        else:  # if message_as_json.get('edited_message'):
            message_content = message_as_json['edited_message']

        chat_id = message_content['chat']['id']
        chat_text = message_content['text']
        status_comment = "success"

        try:
            if chat_text[0] == '/':
                answer = BotController.get_command(chat_id, chat_text[1:])
                res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                                   .format(TOKEN, chat_id, answer))

        except Exception as e:
            answer = e
            Logger.get().error(f'error:{e}', exc_info=True)
            status_comment = "failure"
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                               .format(TOKEN, chat_id, e))
    except Exception as e:
        answer = e
        Logger.get().error(f'error:{e}', exc_info=True)
        status_comment = "failure"
        print(e)
    return flask.Response(json.dumps([]))


