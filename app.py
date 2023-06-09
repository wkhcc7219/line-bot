from flask import Flask,request,abort
from linebot import(
    LineBotApi,WebhookHandler
)
from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.models import(
    MessageEvent,TextMessage,TextSendMessage
)
import json
import os

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

@app.route("/callback",methods=["POST"])
def callback():
    signature = request.headers["X-Line_Signature"]
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    json_str = json.dumps(json_data,indent=4)
    print(json_str)
    
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    json_data = json.loads(str(event))
    json_str = json.dumps(json_data,indent=4)
    print(json_str)
    msg = event.message.text
    line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))
    


if __name__ == "__main__":
    app.run(port=3000)
