from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('w3F448+AlZjMv/pyINyMtGRk9vkCKy6/BR5oajT+C5PNPYJMySq/hUSP0au8/JFC8gcoJd/1Uyz937GJD/F22AI7y6aViU3vmdRHh4HHHi1zDYhGUAgLeotYtbVjTuxXeOaG3ryP8x/j49PkBaqWFAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2206e955eab5c0b6ced2a1e70f01c769')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
