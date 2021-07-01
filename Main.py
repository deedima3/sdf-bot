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

GWK_TEXT = "adalah sebuah taman wisata budaya di selatan pulau Bali"
MARGARANA_TEXT = "adalah sebuah Monumen untuk mengenang Puputan Margarana"
SANUR_TEXT = "adalah salah satu pantai wisata yang terkenal di pulau Bali"
BAJRA_TEXT = "adalah monumen perjuangan rakyat Bali yang terletak di Renon"


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
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text=GWK_TEXT, title='Garuda Wisnu Kencana', thumbnail_image_url="https://www.rentalmobilbali.net/wp-content/uploads/2020/03/Tempat-Wisata-Di-Bali-GWK.jpg", actions=[
                URIAction(label='Selengkapnya',
                          uri='https://id.wikipedia.org/wiki/Taman_Budaya_Garuda_Wisnu_Kencana')
            ]),
            CarouselColumn(text=MARGARANA_TEXT, title='Taman Makam Pahlawan Margarana', thumbnail_image_url="https://upload.wikimedia.org/wikipedia/id/d/db/Candi_Margarana.jpeg", actions=[
                URIAction(label='Selengkapnya',
                          uri='https://id.wikipedia.org/wiki/Taman_Pujaan_Bangsa_Margarana')
            ]),
            CarouselColumn(text=SANUR_TEXT, title='Pantai Sanur', thumbnail_image_url="https://www.indonesia.travel/content/dam/indtravelrevamp/en/destinations/bali-nusa-tenggara/sanurbeach_2.jpg", actions=[
                URIAction(label='Selengkapnya',
                          uri='https://id.wikipedia.org/wiki/Pantai_Sanur')
            ]),
            CarouselColumn(text=BAJRA_TEXT, title='Bajra Sandhi', thumbnail_image_url="https://2.bp.blogspot.com/-xjdOb22GTNc/VX_SZvEoEII/AAAAAAAABaA/ZA0J-LatwlY/s1600/Monumen%2BBajra%2BSandhi%2BBali%2B%252810%2529.jpg", actions=[
                URIAction(label='Selengkapnya',
                          uri='https://id.wikipedia.org/wiki/Monumen_Bajra_Sandhi')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Landmark Pulau Bali', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        
    elif 'jajaran pimpinan' in msg:
        bubble = BubbleContainer(
            direction='ltr',
            header=TextComponent(text='Rektor Udayana', weight='bold', size='xl', align="center", color=""),
            hero=ImageComponent(
                url='https://example.com/cafe.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Brown Cafe', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(
                                size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(
                                size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(
                                size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(
                                size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(
                                size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Shinjuku, Tokyo',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:000000'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(
                            label='WEBSITE', uri="https://example.com")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

