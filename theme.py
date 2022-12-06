import random

_theme = "冬休み 春休み 副業 アルバイト 風呂掃除 食器洗い Twitter Line 水族館 動物園 ドラえもん ドラミちゃん ファミレス カフェ アルバイト面接 就活 お年玉 誕生日プレゼント ガラケー 固定電話 太陽 月 マフラー 手袋 エレベーター エスカレーター コンビニ スーパー 海 プール 年末 年始 コンタクトレンズ メガネ セロテープ ガムテープ 東京タワー スカイツリー コップ グラス カブトムシ クワガタ 飛行機 新幹線 カレー シチュー はさみ カッター テニス 卓球 スケート スキー りす ハムスター ぞう きりん タクシー バス セミ 鈴虫 扇風機 クーラー ディズニーランド USJ 洗濯機 食洗機 ブランコ シーソー 浮き輪 ゴーグル 電圧 電流 バレーボール ビーチボール ベッド 布団 浴衣 着物 テスト 卓球"
_theme2 = "ショッピングモール 商店街 加湿器 エアコン スマートスピーカー タブレット端末 テレホンカード 図書カード 健康診断 予防接種 エコバッグ マスク 公園 遊園地 昼寝 夜更かし 寝坊 忘れ物 出前 再配達 常備薬 サプリメント 金魚 カメ 図書館 古本屋 同窓会 結婚式 蝶ネクタイ リボン 体温計 体重計 財布 電子マネー 天気予報 星座占い 推理小説 謎解きゲーム 充電ケーブル 延長コード スニーカー 革靴 枕 クッション キーホルダー ぬいぐるみ ショートカット 黒髪 トートバッグ リュックサック ガムテープ 接着剤 ウノ ジェンガ ティッシュペーパー トイレットペーパー コンビニ スーパー ネックレス 指輪 スリッパ サンダル フィギュア 缶バッジ 運転免許証 保険証 トイレ 風呂 シーソー ブランコ あやとり ヨーヨー パチンコ 宝くじ 二日酔い 風邪 ハリウッド映画 韓国ドラマ 夢 人生 アルコール タバコ 環境問題 格差社会 ソロキャンプ 一人カラオケ ソーシャルディスタンス テレワーク 耳かき 爪切り"

_theme_list = _theme.split(" ")
_theme_list += _theme2.split(" ")

def select() -> list:
    num = random.randint(0, (len(_theme_list) - 2)/ 2) * 2 # 最後の番号ははみ出る、かつすべてのペアとして出るようにする
    result = [_theme_list[num], _theme_list[num + 1]]
    random.shuffle(result)
    return result