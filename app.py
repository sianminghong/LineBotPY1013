# encoding: utf-8
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

line_bot_api = LineBotApi('zmWBpCj5sgkK2gyoRKV0Cyk7cQaLwZAwkKx9koVGjEDriKM10LEdmd478Uz3Qquf18Dn6DoPKWCWbMlm2d2/OAiWu2ZGNFWm2zoiWJWvTyz73gkCxs6FIEf5ncvc6drEe/8ATJrhuO5v+aPapjojZwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('129e226166e73165e344323b7836868c')

@app.route("https://linebotpy1013.herokuapp.com:443/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "{}: {}".format(event.source.user_id, event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
