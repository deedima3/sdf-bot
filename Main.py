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
    ImageSendMessage, CarouselContainer)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

GWK_TEXT = "adalah sebuah taman wisata budaya di selatan pulau Bali"
MARGARANA_TEXT = "adalah sebuah Monumen untuk mengenang Puputan Margarana"
SANUR_TEXT = "adalah salah satu pantai wisata yang terkenal di pulau Bali"
BAJRA_TEXT = "adalah monumen perjuangan rakyat Bali yang terletak di Renon"

WATINIASIH_TEXT = "Nama: Ni Luh Watiniasih, M.Sc.,Ph.D. \n "
GANDHIADI_TEXT = "Nama: Dr. Drs. GK Gandhiadi, M.T. \n"
SUKADANA_TEXT = "Nama: Dr. Drs. I Made Sukadana, M.Si \n"
GUNAWAN_TEXT = "Nama: Prof. Dr. I Wayan Gede Gunawan S.Si, M.Si."


SEJARAH_FMIPA = "Pada awalnya Fakultas MIPA Udayana disebut Program Studi MIPA yang terbentuk melalui surat Keputusan Rektor Universitas Udayana No. 613/PT.17/I.a.012/1984 pada tanggal 1 Juli 1984."

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#Utitlitiy Function

def createBubble(title, imageURL, text, actionURL):
    bubble = BubbleContainer(
        direction='ltr',
        header=BoxComponent(
            layout="vertical",
            contents=[
                TextComponent(text=title, weight='bold',
                              size='xl', align="center", color="#291749")
            ]
        ),
        hero=ImageComponent(
            url=imageURL,
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover'
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                # info
                TextComponent(text=text, size='sm',
                              align="start", color="#000000", wrap=True)
            ]),
        footer=BoxComponent(
            layout='vertical',
            spacing='sm',
            contents=[
                    # callAction
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=URIAction(label='Selengkapnya',
                                         uri=actionURL),
                        color="#291749"
                    )]
        )
    )
    return bubble


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
        bubble1 = createBubble(
            "Dekan FMIPA", 
            "https://simdos.unud.ac.id/uploads/file_foto_dir/b68c3163efaef4e08ac00b8a3e0e3b8ae1cf5cdb.jpg",
            WATINIASIH_TEXT,
            "https://udayananetworking.unud.ac.id/lecturer/2302-ni-luh-watiniasih")
        bubble2 = createBubble(
            "Wakil Dekan I Bidang Akademik dan Perencanaan",
            "https://simdos.unud.ac.id/uploads/file_foto_dir/c846fc105e2f2f845a4015fc8edeaa90fd0088db.jpg",
            GANDHIADI_TEXT,
            "https://udayananetworking.unud.ac.id/lecturer/2268-gk-gandhiadi"
        )
        bubble3 = createBubble(
            "Wakil Dekan II Bidang Umum dan Keuangan",
            "https://simdos.unud.ac.id/uploads/file_foto_dir/7b479289d3cc1ab53944113d03763d70.jpg",
            SUKADANA_TEXT,
            "https://udayananetworking.unud.ac.id/lecturer/2326-i-made-sukadana"
        )
        bubble4 = createBubble(
            "Wakil Dekan III Bidang Kemahasiswaan dan Informasi",
            "https://udayananetworking.unud.ac.id/protected/storage/foto_biografi/foto%203x4.jpg",
            GUNAWAN_TEXT,
            "https://udayananetworking.unud.ac.id/professor/credential/2298-i-wayan-gede-gunawan"
        )
        container = CarouselContainer(contents=[bubble1, bubble2, bubble3, bubble4])
        message = FlexSendMessage(alt_text="Jajaran Pimpinan", contents=container)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif 'peta' in msg:
        image_message = ImageSendMessage(
            original_content_url='https://i5.wikimapia.org/?x=13433&y=8593&zoom=14&type=map&lng=0',
            preview_image_url='https://i5.wikimapia.org/?x=13433&y=8593&zoom=14&type=map&lng=0'
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    
    elif 'sejarah mipa' in msg:
        bubble1 = createBubble(
            "Sejarah FMIPA Unud", 
            "https://dkarmanax.files.wordpress.com/2013/06/img00175-20111231-0830.jpg?w=650",
            SEJARAH_FMIPA,
            "https://dkarmanax.wordpress.com/2013/06/23/mengenal-fmipa-universitas-udayana/")
        container = CarouselContainer(contents=[bubble1])
        message = FlexSendMessage(alt_text="Sejarah Unud", contents=container)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

