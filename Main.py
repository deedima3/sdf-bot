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

GWK_TEXT = "Taman Budaya Garuda Wisnu Kencana, atau kerap disebut dengan GWK, adalah sebuah taman wisata budaya di bagian selatan pulau Bali. Taman wisata ini terletak di Desa Ungasan, Kecamatan Kuta Selatan, Kabupaten Badung, kira-kira 40 kilometer di sebelah selatan Denpasar, ibu kota provinsi Bali.Di sini berdiri megah sebuah landmark atau maskot Bali, yakni patung Garuda Wisnu Kencana yang menggambarkan sosok Dewa Wisnu menunggangi tunggangannya, Garuda, setinggi 121 meter."
MARGARANA_TEXT = "Monumen Nasional Taman Pujaan Bangsa Margarana adalah sebuah Monumen peringatan yang didirikan untuk mengenang tragedi Puputan Margarana, di Desa Marga, Kecamatan Marga, Kabupaten Tabanan, Bali. Pada Tanggal 20 November 1946 terjadilah pertempuran habis-habisan antara pasukan pejuang Republik Indonesia melawan kaum penjajah Belanda,di Banjar Kelaci, Desa Marga oleh pasukan Ciung Wanara di bawah pimpinan Kolonel I Gusti Ngurah Rai. "
SANUR_TEXT = "Pantai Sanur adalah salah satu pantai wisata yang terkenal di pulau Bali. Tempat ini letaknya adalah persis di sebelah timur kota Denpasar, ibu kota Bali. Sanur berada di Kotamadya Denpasar."
BAJRA_TEXT = "Monumen Bajra Sandhi atau disebut juga Monumen Perjuangan Rakyat Bali adalah monumen perjuangan rakyat Bali yang terletak di Renon, Kota Denpasar, Bali. Monumen ini menempati areal yang sangat luas, ada beberapa lapangan bola di sekelilingnya. "


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
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

        
if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

