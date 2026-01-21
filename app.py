from flask import Flask, render_template, request, flash, redirect, url_for
from extensions import db
from models import Reservation  


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Настройка PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5129@localhost/resutoran'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  


categories = {
    'russian': {
        'name': 'ロシア料理',
        'description': '温かみのある伝統的なロシアの味',
        'icon': '🇷🇺',
        'color': "#6E64ED",
        'dishes': [
            
            {
                'name': 'ブリン',
                'price': '¥600',
                'description': 'ロシア風パンケーキ',
                'type': 'dessert',
                'image': 'russian-blin.jpg'
            },
            {
                'name': 'クリチ',
                'price': '¥550', 
                'description': '伝統的なイースターケーキ',
                'type': 'dessert',
                'image': 'russian-kulich.jpg'
            },
            {
                'name': 'メドヴィーク',
                'price': '¥700',
                'description': 'はちみつケーキ',
                'type': 'dessert',
                'image': 'russian-medovik.jpg'
            },
            {
                'name': 'ナポレオン',
                'price': '¥650',
                'description': '層状のクリームケーキ',
                'type': 'dessert',
                'image': 'russian-napoleon.jpg'
            },
            {
                'name': 'シルニキ',
                'price': '¥500',
                'description': 'カッテージチーズパンケーキ',
                'type': 'dessert',
                'image': 'russian-sirnik.jpg'
            },
            # Đồ uống (5 món)
            {
                'name': 'カゴール',
                'price': '¥800',
                'description': '甘口の教会ワイン',
                'type': 'drink',
                'image': 'russian-kagor.jpg'
            },
            {
                'name': 'クワス',
                'price': '¥400',
                'description': '伝統的な発酵飲料',
                'type': 'drink',
                'image': 'russian-kvas.jpg'
            },
            {
                'name': 'メドヴーハ',
                'price': '¥750',
                'description': 'はちみつ酒',
                'type': 'drink',
                'image': 'russian-medovuha.jpg'
            },
            {
                'name': 'ナストイカ',
                'price': '¥900',
                'description': 'ハーブリキュール',
                'type': 'drink',
                'image': 'russian-nastoika.jpg'
            },
            {
                'name': 'ウォッカ',
                'price': '¥850',
                'description': '伝統的なロシアウォッカ',
                'type': 'drink',
                'image': 'russian-vodka.jpg'
            },
            # Món chính (5 món)
            {
                'name': 'ベフストロガノフ',
                'price': '¥1,800',
                'description': '牛肉のクリーム煮込み',
                'type': 'main',
                'image': 'russian-bestrog.jpg'
            },
            {
                'name': 'ボルシチ',
                'price': '¥1,200',
                'description': '伝統的な赤いビーツスープ',
                'type': 'main',
                'image': 'russian-borsch.jpg'
            },
            {
                'name': 'キャベツロール',
                'price': '¥1,100',
                'description': 'キャベツの肉巻き',
                'type': 'main',
                'image': 'russian-cabbage-rolls.jpg'
            },
            {
                'name': 'コトレタ',
                'price': '¥950',
                'description': 'ロシア風カツレツ',
                'type': 'main',
                'image': 'russian-kotleta.jpg'
            },
            {
                'name': 'オリヴィエサラダ',
                'price': '¥850',
                'description': '伝統的なロシアサラダ',
                'type': 'main',
                'image': 'russian-olivier-salad.jpg'
            }
        ]
    },
    'vietnamese': {
        'name': 'ベトナム料理',
        'description': 'さっぱりとした味わい',
        'icon': '🇻🇳',
        'color': '#FF0000',
        'dishes': [
            # Món chính (5 món)
            {
                'name': 'フォー',
                'price': '¥1,100',
                'description': 'ベトナムの米粉麺スープ',
                'type': 'main',
                'image': 'vietnamese-pho.jpg'
            },
            {
                'name': 'バインミー',
                'price': '¥850',
                'description': 'ベトナム風サンドイッチ',
                'type': 'main',
                'image': 'vietnamese-banh-mi.jpg'
            },
            {
                'name': '生春巻き',
                'price': '¥700',
                'description': '新鮮な野菜とエビの生春巻き',
                'type': 'main',
                'image': 'vietnamese-spring-rolls.jpg'
            },
            {
                'name': 'バインセオ',
                'price': '¥950',
                'description': 'ベトナム風クレープ',
                'type': 'main',
                'image': 'vietnamese-banh-xeo.jpg'
            },
            {
                'name': 'ブンチャー',
                'price': '¥1,050',
                'description': 'ブン麺のグリル豚肉',
                'type': 'main',
                'image': 'vietnamese-bun-cha.jpg'
            },
            # Món tráng miệng (5 món)
            {
                'name': 'チェー',
                'price': '¥450',
                'description': 'ベトナム風デザートドリンク',
                'type': 'dessert',
                'image': 'vietnamese-che.jpg'
            },
            {
                'name': 'バインフラン',
                'price': '¥400',
                'description': 'ベトナム風カスタード',
                'type': 'dessert',
                'image': 'vietnamese-banh-flan.jpg'
            },
            {
                'name': 'コムネプ',
                'price': '¥380',
                'description': 'もち米デザート',
                'type': 'dessert',
                'image': 'vietnamese-com-nep.jpg'
            },
            {
                'name': 'バインダウ',
                'price': '¥420',
                'description': '緑豆ケーキ',
                'type': 'dessert',
                'image': 'vietnamese-banh-dau.jpg'
            },
            {
                'name': 'ホアイチェー',
                'price': '¥480',
                'description': 'タロイモのデザート',
                'type': 'dessert',
                'image': 'vietnamese-hoai-che.jpg'
            },
            # Đồ uống (5 món)
            {
                'name': 'ベトナムコーヒー',
                'price': '¥350',
                'description': '濃厚なドリップコーヒー',
                'type': 'drink',
                'image': 'vietnamese-coffee.jpg'
            },
            {
                'name': '砂糖キビジュース',
                'price': '¥300',
                'description': '新鮮な砂糖キビジュース',
                'type': 'drink',
                'image': 'vietnamese-sugar-cane.jpg'
            },
            {
                'name': 'レモングラスティー',
                'price': '¥280',
                'description': 'さわやかなレモングラス茶',
                'type': 'drink',
                'image': 'vietnamese-lemongrass-tea.jpg'
            },
            {
                'name': 'シンハー',
                'price': '¥400',
                'description': 'ベトナムビール',
                'type': 'drink',
                'image': 'vietnamese-saigon-beer.jpg'
            },
            {
                'name': 'ノニジュース',
                'price': '¥320',
                'description': '健康ノニジュース',
                'type': 'drink',
                'image': 'vietnamese-noni-juice.jpg'
            }
        ]
    },
    'chinese': {
        'name': '中華料理',
        'description': '多様な味と香り',
        'icon': '🇨🇳',
        'color': '#FF8C00',
        'dishes': [
            # Món chính (5 món)
            {
                'name': '北京ダック',
                'price': '¥2,500',
                'description': '伝統的な北京ダック',
                'type': 'main',
                'image': 'chinese-peking-duck.jpg'
            },
            {
                'name': '餃子',
                'price': '¥800',
                'description': '手作り餃子',
                'type': 'main',
                'image': 'chinese-dumplings.jpg'
            },
            {
                'name': '小籠包',
                'price': '¥950',
                'description': '辛い豆腐料理',
                'type': 'main',
                'image': 'chinese-mapo-tofu.jpg'
            },
            {
                'name': '毛ガニ',
                'price': '¥1,200',
                'description': '甘辛エビ料理',
                'type': 'main',
                'image': 'chinese-shrimp-chili.jpg'
            },
            {
                'name': '東坡豚肉',
                'price': '¥1,100',
                'description': 'ピーマンと肉の炒め物',
                'type': 'main',
                'image': 'chinese-green-pepper-pork.jpg'
            },
            # Món tráng miệng (5 món)
            {
                'name': '月餅',
                'price': '¥550',
                'description': '伝統的な月餅',
                'type': 'dessert',
                'image': 'chinese-mooncake.jpg'
            },
            {
                'name': 'タンユロ',
                'price': '¥350',
                'description': '中華あんまん',
                'type': 'dessert',
                'image': 'chinese-tango.jpg'
            },
            {
                'name': '芝麻球',
                'price': '¥400',
                'description': 'ごま団子',
                'type': 'dessert',
                'image': 'chinese-sesame-ball.jpg'
            },
            {
                'name': '砂糖漬けのフルーツ',
                'price': '¥450',
                'description': 'アーモンドプリン',
                'type': 'dessert',
                'image': 'chinese-almond-tofu.jpg'
            },
            {
                'name': '楊枝甘露',
                'price': '¥380',
                'description': '揚げバナナ',
                'type': 'dessert',
                'image': 'chinese-fried-banana.jpg'
            },
            # Đồ uống (5 món)
            {
                'name': 'ウーロン茶',
                'price': '¥300',
                'description': '中国烏龍茶',
                'type': 'drink',
                'image': 'chinese-oolong-tea.jpg'
            },
            {
                'name': 'オレンジジュース',
                'price': '¥280',
                'description': '香り高いジャスミン茶',
                'type': 'drink',
                'image': 'chinese-jasmine-tea.jpg'
            },
            {
                'name': '茅台酒',
                'price': '¥1,200',
                'description': '高級中国酒',
                'type': 'drink',
                'image': 'chinese-maotai.jpg'
            },
            {
                'name': '珍珠奶茶',
                'price': '¥320',
                'description': 'タピオカミルクティー',
                'type': 'drink',
                'image': 'chinese-bubble-tea.jpg'
            },
            {
                'name': '菊花茶',
                'price': '¥290',
                'description': '菊の花茶',
                'type': 'drink',
                'image': 'chinese-chrysanthemum-tea.jpg'
            }
        ]
    },
    'nepalese': {
        'name': 'ネパール料理',
        'description': 'ヒマラヤの素朴な味',
        'icon': '🇳🇵',
        'color': '#800080',
        'dishes': [
            # Món chính (5 món) - ĐÃ CẬP NHẬT
            {
                'name': 'モモ',
                'price': '¥900',
                'description': 'ネパール風餃子',
                'type': 'main',
                'image': 'nepalese-momo.jpg'
            },
            {
                'name': 'タカリセト',
                'price': '¥1,300',
                'description': '伝統的な定食',
                'type': 'main',
                'image': 'nepalese-dal-bhat.jpg'
            },
            {
                'name': 'パニプリ',
                'price': '¥750',
                'description': 'スパイシーなスナック',
                'type': 'main',
                'image': 'nepalese-panipuri.jpg'
            },
            {
                'name': 'セル・ロティ',
                'price': '¥680',
                'description': 'リング状のライスパン',
                'type': 'main',
                'image': 'nepalese-sel-roti.jpg'
            },
            {
                'name': 'チャタパテ',
                'price': '¥820',
                'description': '混ぜ合わせたスパイシーなスナック',
                'type': 'main',
                'image': 'nepalese-chatamari.jpg'
            },
            # Món tráng miệng (5 món)
            {
                'name': ' アナルサ',
                'price': '¥350',
                'description': 'ネパールのゼリー',
                'type': 'dessert',
                'image': 'nepalese-jeri.jpg'
            },
            {
                'name': 'ココナシラドゥ',
                'price': '¥300',
                'description': 'チャナ豆のお菓子',
                'type': 'dessert',
                'image': 'nepalese-ladoo.jpg'
            },
            {
                'name': 'カジュバルフィ',
                'price': '¥400',
                'description': '米のデザート',
                'type': 'dessert',
                'image': 'nepalese-barsi.jpg'
            },
            {
                'name': 'ヨマーリ',
                'price': '¥450',
                'description': 'ネパール風プディング',
                'type': 'dessert',
                'image': 'nepalese-pudding.jpg'
            },
            {
                'name': 'キール',
                'price': '¥380',
                'description': '甘いパン',
                'type': 'dessert',
                'image': 'nepalese-malcha.jpg'
            },
            # Đồ uống (5 món) - ĐÃ CẬP NHẬT
            {
                'name': 'ククリラ-ム',
                'price': '¥500',
                'description': '米の発酵酒',
                'type': 'drink',
                'image': 'nepalese-chang.jpg'
            },
            {
                'name': 'クリーム・ヨーグルト・ラシ',
                'price': '¥450',
                'description': 'クリーミーなヨーグルトドリンク',
                'type': 'drink',
                'image': 'nepalese-lassi.jpg'
            },
            {
                'name': 'コドコ・ラクシー',
                'price': '¥350',
                'description': '伝統的なミルクドリンク',
                'type': 'drink',
                'image': 'nepalese-tea.jpg'
            },
            {
                'name': 'トウンバ',
                'price': '¥550',
                'description': 'ミレットビール',
                'type': 'drink',
                'image': 'nepalese-tomba.jpg'
            },
            {
                'name': 'マンゴーラッシ',
                'price': '¥420',
                'description': 'マンゴーのヨーグルトドリンク',
                'type': 'drink',
                'image': 'nepalese-sikan.jpg'
            }
        ]
    }
}

@app.route('/') 
def index():
    return render_template('index.html', categories=categories)

@app.route('/menu')
def menu():
    category = request.args.get('category', 'all')
    dish_type = request.args.get('type', 'all')
    
    return render_template('menu.html', 
                         categories=categories,
                         selected_category=category,
                         selected_type=dish_type)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']


        flash('お問い合わせありがとうございます！メッセージを受け付けました。', 'success')
        return redirect(url_for('contact'))   

    return render_template("contact.html")


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form.get('reservation_name')
        email = request.form.get('reservation_email')
        phone = request.form.get('reservation_phone')
        date = request.form.get('reservation_date')
        time = request.form.get('reservation_time')
        guests = request.form.get('reservation_guests')
        note = request.form.get('reservation_note')

        new_res = Reservation(
            name=name,
            email=email,
            phone=phone,
            reservation_date=date,
            reservation_time=time,
            guests=guests,
            note=note
        )

        db.session.add(new_res)
        db.session.commit()

        flash('予約リクエストが保存されました！', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)