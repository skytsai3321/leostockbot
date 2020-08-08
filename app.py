# 載入LineBot所需要的套件
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import mongodb

import re

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'qK1vqjTedFkoKmscVd3SQDNRce35llWyRkiN5JQs2cgYvVlUqGq6Sz+PLJsasuvuN6PQ+HHxOq70+lKgAW2l5+boqm87Ey+CbZ4bnlmRiQY1Aj6iEu1/1dVlpI0dEIx/t0EGsk8kMWFsmtRSsoLC/QdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('c59969ee92306eac22f70f27c563a7d8')

line_bot_api.push_message(
    'U59877be6684a4d35fec0194931c8c62d', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request


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
        abort(400)

    return 'OK'

# 訊息傳遞區塊


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id
    usespeak = str(event.message.text)
    if re.match('[0-9]{4}[<>][0-9]', usespeak):
        mongodb.write_user_stock_fountion(
            stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        line_bot_api.push_message(
            uid, TextSendMessage(usespeak[0:4] + '已經儲存成功'))
        return 0
    elif re.match('刪除[0-9]{4}', usespeak):
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak + '已經刪除成功'))
        return 0


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 443))
    app.run(host='0.0.0.0', port=port)
