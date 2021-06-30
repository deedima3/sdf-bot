from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = (event.message.text).lower()

    # 3 Main menu, used in rich menu
    if 'sdf' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="SDF")
        )
    elif 'unud' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Unud")
        )
    elif 'games' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Games")
        )
    
    # Submenu
    elif 'landmark bali' in msg:
        carousel_template = CarouselTemplate(thumbnail_image_url="https://www.rentalmobilbali.net/wp-content/uploads/2020/03/Tempat-Wisata-Di-Bali-GWK.jpg"columns=[
            CarouselColumn(text='hoge1', title='fuga1', , actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', thumbnail_image_url="https://www.rentalmobilbali.net/wp-content/uploads/2020/03/Tempat-Wisata-Di-Bali-GWK.jpg", actions=[
                PostbackAction(label='ping with text',
                               data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

        
if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
