#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('qK1vqjTedFkoKmscVd3SQDNRce35llWyRkiN5JQs2cgYvVlUqGq6Sz+PLJsasuvuN6PQ+HHxOq70+lKgAW2l5+boqm87Ey+CbZ4bnlmRiQY1Aj6iEu1/1dVlpI0dEIx/t0EGsk8kMWFsmtRSsoLC/QdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('c59969ee92306eac22f70f27c563a7d8')

line_bot_api.push_message('U59877be6684a4d35fec0194931c8c62d', TextSendMessage(text='你可以開始了'))

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

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 443))
    app.run(host='0.0.0.0', port=port)
