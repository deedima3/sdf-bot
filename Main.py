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

GWK_TEXT = "Taman Budaya Garuda Wisnu Kencana (bahasa Inggris: Garuda Wisnu Kencana Cultural Park), atau kerap disebut dengan GWK, adalah sebuah taman wisata budaya di bagian selatan pulau Bali. Taman wisata ini terletak di Desa Ungasan, Kecamatan Kuta Selatan, Kabupaten Badung, kira-kira 40 kilometer di sebelah selatan Denpasar, ibu kota provinsi Bali."
MARGARANA_TEXT = "Monumen Nasional Taman Pujaan Bangsa Margarana adalah sebuah Monumen peringatan yang didirikan untuk mengenang tragedi Puputan Margarana, di Desa Marga, Kecamatan Marga, Kabupaten Tabanan, Bali."
SANUR_TEXT = "Pantai Sanur adalah salah satu pantai wisata yang terkenal di pulau Bali. Tempat ini letaknya adalah persis di sebelah timur kota Denpasar, ibu kota Bali. Sanur berada di Kotamadya Denpasar. "
BAJRA_TEXT = "Monumen Bajra Sandhi atau disebut juga Monumen Perjuangan Rakyat Bali adalah monumen perjuangan rakyat Bali yang terletak di Renon, Kota Denpasar, Bali. Monumen ini menempati areal yang sangat luas, ada beberapa lapangan bola di sekelilingnya. "

WATINIASIH_TEXT = "Nama: Ni Luh Watiniasih, M.Sc.,Ph.D. \n "
GANDHIADI_TEXT = "Nama: Dr. Drs. GK Gandhiadi, M.T. \n"
SUKADANA_TEXT = "Nama: Dr. Drs. I Made Sukadana, M.Si \n"
GUNAWAN_TEXT = "Nama: Prof. Dr. I Wayan Gede Gunawan S.Si, M.Si."


SEJARAH_FMIPA = "Pada awalnya Fakultas MIPA Udayana disebut Program Studi MIPA yang terbentuk melalui surat Keputusan Rektor Universitas Udayana No. 613/PT.17/I.a.012/1984 pada tanggal 1 Juli 1984."

AKREDITASI_FIS = "Akreditasi BAN-PT Jurusan Fisika FMIPA Universitas Udayana yang diperoleh selalu baik (B)."
AKREDITASI_KIM = "Akreditasi BAN-PT Jurusan Kimia FMIPA Universitas Udayana dilaksanakan tahun 2001, 2006, dan 2012. Selama tiga kali akreditasi, nilai akreditasi yang diperoleh selalu baik (B)."
AKREDITASI_BIO = "Akreditasi dari Program Studi Biologi dengan No SK Akreditasi : 025/BAN-PT/Ak-XIV/S1/IX/2011 dengan nilai baik (B)."
AKREDITASI_MAT = "Jurusan Matematika terakreditasi B dan berlaku selama lima tahun. Akreditasi ini berdasarkan SK BAN-PT nomor 217/SK/BAN-PT/Ak-XVI/S/X/2013."
AKREDITASI_FARMA = "Berdasarkan Keputusan Badan Akreditasi Nasional Perguruan Tinggi No 383/SK/BAN PT/akred/S/IX/2014 dinyatakan terakreditasi dengan nilai B."
AKREDITASI_KOM = "Akreditasi BAN-PT Jurusan Informatika FMIPA Universitas Udayana diperoleh selalu baik (B)."

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#Utitlitiy Function


def createBubble(title, imageURL, text, actionURL="0", titleSize="xl", imageAspectRatio="20:13", button=True, textAllignment="start"):
    if button:
        footerTemp = BoxComponent(
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
    else:
        footerTemp = None

    bubble = BubbleContainer(
        direction='ltr',
        header=BoxComponent(
            layout="vertical",
            contents=[
                TextComponent(text=title, weight='bold',
                              size=titleSize, align="center", color="#291749", wrap=True)
            ]
        ),
        hero=ImageComponent(
            url=imageURL,
            size='full',
            aspect_ratio=imageAspectRatio,
            aspect_mode='cover'
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                # info
                TextComponent(text=text, size='sm',
                              align=textAllignment, color="#000000", wrap=True)
            ]),
        footer=footerTemp
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
        bubble1 = createBubble(
            "Garuda Wisnu Kencana",
            "https://www.rentalmobilbali.net/wp-content/uploads/2020/03/Tempat-Wisata-Di-Bali-GWK.jpg",
            GWK_TEXT,
            "https://id.wikipedia.org/wiki/Taman_Budaya_Garuda_Wisnu_Kencana",
            "xl",
            textAllignment="center"
        )
        bubble2 = createBubble(
            "Taman Makam Pahlawan Margarana",
            "https://upload.wikimedia.org/wikipedia/id/d/db/Candi_Margarana.jpeg",
            MARGARANA_TEXT,
            "https://id.wikipedia.org/wiki/Taman_Pujaan_Bangsa_Margarana",
            "xl",
            textAllignment="center"
        )
        bubble3 = createBubble(
            "Pantai Sanur",
            "ttps://www.indonesia.travel/content/dam/indtravelrevamp/en/destinations/bali-nusa-tenggara/sanurbeach_2.jpg",
            SANUR_TEXT,
            "https://id.wikipedia.org/wiki/Pantai_Sanur",
            "xl",
            textAllignment="center"
        )
        bubble4 = createBubble(
            "Bajra Sandhi",
            "https://2.bp.blogspot.com/-xjdOb22GTNc/VX_SZvEoEII/AAAAAAAABaA/ZA0J-LatwlY/s1600/Monumen%2BBajra%2BSandhi%2BBali%2B%252810%2529.jpg",
            BAJRA_TEXT,
            "https://id.wikipedia.org/wiki/Monumen_Bajra_Sandhi",
            "xl",
            textAllignment="center"
        )
        container = CarouselContainer(
            contents=[bubble1, bubble2, bubble3, bubble4])
        message = FlexSendMessage(
            alt_text="Landmark Bali", contents=container)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif 'jajaran pimpinan' in msg:
        bubble1 = createBubble(
            "Dekan FMIPA", 
            "https://simdos.unud.ac.id/uploads/file_foto_dir/b68c3163efaef4e08ac00b8a3e0e3b8ae1cf5cdb.jpg",
            WATINIASIH_TEXT,
            "https://udayananetworking.unud.ac.id/lecturer/2302-ni-luh-watiniasih",
            "xl",
            "4:5",
            False
        )
        bubble2 = createBubble(
            "Wakil Dekan I",
            "https://simdos.unud.ac.id/uploads/file_foto_dir/c846fc105e2f2f845a4015fc8edeaa90fd0088db.jpg",
            GANDHIADI_TEXT,
            "https://udayananetworking.unud.ac.id/lecturer/2268-gk-gandhiadi",
            "xl",
            "4:5",
            False
        )
        bubble3 = createBubble(
            "Wakil Dekan II",
            "https://simdos.unud.ac.id/uploads/file_foto_dir/7b479289d3cc1ab53944113d03763d70.jpg",
            SUKADANA_TEXT,
            "https://udayananetworking.unud.ac.id/lecturer/2326-i-made-sukadana",
            "xl",
            "4:5",
            False
        )
        bubble4 = createBubble(
            "Wakil Dekan III",
            "https://udayananetworking.unud.ac.id/protected/storage/foto_biografi/foto%203x4.jpg",
            GUNAWAN_TEXT,
            "https://udayananetworking.unud.ac.id/professor/credential/2298-i-wayan-gede-gunawan",
            "xl",
            "4:5",
            False
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

    elif 'akreditasi mipa' in msg:
        bubble1 = createBubble(
            "Prodi Fisika", 
            "https://pbs.twimg.com/profile_images/378800000108493477/15e18cf46738f7e061951d832d2771fb_400x400.jpeg",
            AKREDITASI_FIS,
            "https://www.unud.ac.id/in/prodi82-Fisika.html")
        bubble2 = createBubble(
            "Prodi Kimia", 
            "https://pbs.twimg.com/profile_images/1218403600897998848/LrMOBFNC_400x400.jpg",
            AKREDITASI_KIM,
            "https://www.unud.ac.id/in/prodi47-Kimia.html")
        bubble3 = createBubble(
            "Prodi Biologi", 
            "https://pbs.twimg.com/profile_images/1090447974025486336/RdQazE4S_400x400.jpg",
            AKREDITASI_BIO,
            "https://www.unud.ac.id/in/prodi77-Biologi.html")
        bubble4 = createBubble(
            "Prodi Matematika", 
            "https://pbs.twimg.com/profile_images/598791010345357313/DTg7nXkL.jpg",
            AKREDITASI_MAT,
            "https://www.unud.ac.id/in/prodi81-Matematika.html")
        bubble5 = createBubble(
            "Prodi Farmasi", 
            "https://pbs.twimg.com/profile_images/344513261572834650/c1d8d52b7589005ee3a9549f55815cb4.jpeg",
            AKREDITASI_FARMA,
            "https://www.unud.ac.id/in/prodi79-Farmasi.html")
        bubble6 = createBubble(
            "Prodi Informatika", 
            "https://pbs.twimg.com/profile_images/3661069144/e1f2a6dd7129b5dd2d46584743f29d02_400x400.jpeg",
            AKREDITASI_KOM,
            "https://www.unud.ac.id/in/prodi80-Ilmu%20Komputer-Teknik%20Informatika.html")
        container = CarouselContainer(contents=[bubble1, bubble2, bubble3, bubble4, bubble5, bubble6])
        message = FlexSendMessage(alt_text="Akreditasi MIPA", contents=container)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif 'nyaaa' in msg:
        text = TextSendMessage(text="Nyaa~")
        image_message = ImageSendMessage(
            original_content_url='https://1.bp.blogspot.com/-A_gFX5Dh04s/V6OwMNgsW0I/AAAAAAAAizQ/h0iPEF9qrdIwlNToRXp0DT8IAhKyfoQTACPcB/s1600/Omake%2BGif%2BAnime%2B-%2BNew%2BGame%2521%2B-%2BEpisode%2B5%2B-%2BHajime%2BNyaa%2BTee%2BHee.gif',
            preview_image_url='https://1.bp.blogspot.com/-A_gFX5Dh04s/V6OwMNgsW0I/AAAAAAAAizQ/h0iPEF9qrdIwlNToRXp0DT8IAhKyfoQTACPcB/s1600/Omake%2BGif%2BAnime%2B-%2BNew%2BGame%2521%2B-%2BEpisode%2B5%2B-%2BHajime%2BNyaa%2BTee%2BHee.gif'
        )
        line_bot_api.reply_message(event.reply_token, [text, image_message])


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

