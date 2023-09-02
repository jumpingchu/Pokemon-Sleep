import re
import warnings; warnings.filterwarnings('ignore')
import pandas as pd
import pytesseract


class TransformImage:
    def __init__(self, img):
        self.img = img
        self.config = r'--psm 12 --dpi 300' # 6, 11 and 12 are more accurate
        self.output_type = 'dict'
        self.lang = 'chi_tra'
    
    def img_to_dataframe(self):
        data = pytesseract.image_to_data(self.img, output_type=self.output_type, lang=self.lang, config=self.config)
        df = pd.DataFrame(data)
        return df
    
    def pre_filter(self, df):
        mask = (
            (df['level'] == 5) & 
            (df['conf'] > 0)
        )

        df_text = df[mask]
        df_text = df_text.drop(['page_num', 'par_num', 'word_num'], axis=1)
        return df_text

    def create_full_text(self, df_text):
        df_full_text = df_text[['block_num', 'line_num', 'text']].copy()
        df_full_text = df_full_text.groupby(['block_num', 'line_num'], as_index=False).transform(lambda x: ''.join(x))
        df_text['full_text'] = df_full_text['text']
        return df_text

    def post_filter(self, df_text):

        def find_zh(x):
            if re.search(u'[\u4e00-\u9fff]', x):
                return True
            return False

        def modify_text(x):
            if '$' in x:
                x = x.replace('$', 'S')
                return x
            return x
            
        df_text = df_text.drop_duplicates(['block_num', 'line_num', 'full_text'])
        df_text = df_text.drop(['level', 'block_num', 'line_num'], axis=1)
        mask = (
            (df_text['full_text'].str.len() > 3)
            & (df_text['full_text'].str.len() < 10)
            & (df_text['text'] != '一')
            & (df_text['left'] > 190)
            & (df_text['top'] > 200)
        )
        df_text = df_text[mask]
        df_text = df_text.drop('text', axis=1)
        df_text = df_text[df_text['full_text'].apply(find_zh)]
        df_text['full_text'] = df_text['full_text'].apply(modify_text)
        return df_text
    
    def run(_self):
        df = _self.img_to_dataframe()
        df_text = _self.pre_filter(df)
        df_text = _self.create_full_text(df_text)
        df_text = _self.post_filter(df_text)
        return df_text
    
main_skills = [
    '能量填充S',
    '能量填充M',
    '夢之碎片獲取S',
    '活力療癒S',
    '能量填充Sn',
    '夢之碎片獲取Sn',
    '活力填充S',
    '活力全體療癒S',
    '幫手支援S',
    '食材獲取S',
    '料理強化S',
    '揮指'
]

sub_skills = [
    '樹果數量S',
    '夢之碎片獎勵',
    '活力回復獎勵',
    '幫手獎勵',
    '幫忙速度M',
    '幫忙速度S',
    '食材機率提升M',
    '食材機率提升S',
    '持有上限提升L',
    '持有上限提升M',
    '持有上限提升S',
    '研究EXP獎勵',
    '技能等級提升M',
    '技能等級提升S',
    '技能機率提升M',
    '技能機率提升S',
    '睡眠EXP獎勵',
]

pokemons = [
    '妙蛙種子',
    '妙蛙草',
    '妙蛙花',
    '小火龍',
    '火恐龍',
    '噴火龍',
    '傑尼龜',
    '卡咪龜',
    '水箭龜',
    '綠毛蟲',
    '鐵甲蛹',
    '巴大蝶',
    '小拉達',
    '拉達',
    '阿柏蛇',
    '阿柏怪',
    '皮丘',
    '皮卡丘',
    '雷丘',
    '寶寶丁',
    '胖丁',
    '胖可丁',
    '地鼠',
    '三地鼠',
    '喵喵',
    '貓老大',
    '可達鴨',
    '哥達鴨',
    '猴怪',
    '火爆猴',
    '卡蒂狗',
    '風速狗',
    '喇叭芽',
    '口呆花',
    '大食花',
    '小拳石',
    '隆隆石',
    '隆隆岩',
    '呆呆獸',
    '呆殼獸',
    '呆呆王',
    '小磁怪',
    '三合一磁怪',
    '自爆磁怪',
    '嘟嘟',
    '嘟嘟利',
    '鬼斯',
    '鬼斯通',
    '耿鬼',
    '卡拉卡拉',
    '嘎啦嘎啦',
    '袋獸',
    '凱羅斯',
    '百變怪',
    '伊布',
    '仙子伊布',
    '水伊布',
    '雷伊布',
    '火伊布',
    '太陽伊布',
    '月亮伊布',
    '葉伊布',
    '冰伊布',
    '菊草葉',
    '月桂葉',
    '大竺葵',
    '火球鼠',
    '火岩鼠',
    '火爆獸',
    '小鋸鱷',
    '藍鱷',
    '大力鱷',
    '波克比',
    '波克基古',
    '波克基斯',
    '咩利羊',
    '茸茸羊',
    '電龍',
    '盆才怪',
    '樹才怪',
    '小果然',
    '果然翁',
    '赫拉克羅斯',
    '戴魯比',
    '黑魯加',
    '幼基拉斯',
    '沙基拉斯',
    '班基拉斯',
    '懶人獺',
    '過動猿',
    '請假王',
    '勾魂眼',
    '溶食獸',
    '吞食獸',
    '青綿鳥',
    '七夕青鳥',
    '阿勃梭魯',
    '海豹球',
    '海魔獅',
    '帝牙海獅',
    '利歐路',
    '路卡利歐',
    '不良蛙',
    '毒骷蛙',
]

natures = {
'怕寂寞': {'up': '幫忙速度', 'down': '活力回復'},
'固執': {'up': '幫忙速度', 'down': '食材發現'},
'頑皮': {'up': '幫忙速度', 'down': '主技能'},
'勇敢': {'up': '幫忙速度', 'down': 'EXP'},
'大膽': {'up': '活力回復', 'down': '幫忙速度'},
'淘氣': {'up': '活力回復', 'down': '食材發現'},
'樂天': {'up': '活力回復', 'down': '主技能'},
'悠閒': {'up': '活力回復', 'down': 'EXP'},
'內斂': {'up': '食材發現', 'down': '幫忙速度'},
'慢吞吞': {'up': '食材發現', 'down': '活力回復'},
'馬虎': {'up': '食材發現', 'down': '主技能'},
'冷靜': {'up': '食材發現', 'down': 'EXP'},
'溫和': {'up': '主技能', 'down': '幫忙速度'},
'溫順': {'up': '主技能', 'down': '活力回復'},
'慎重': {'up': '主技能', 'down': '食材發現'},
'自大': {'up': '主技能', 'down': 'EXP'},
'膽小': {'up': 'EXP', 'down': '幫忙速度'},
'急躁': {'up': 'EXP', 'down': '活力回復'},
'爽朗': {'up': 'EXP', 'down': '食材發現'},
'天真': {'up': 'EXP', 'down': '主技能'},
'害羞': {'up': '沒有性格帶來的特色', 'down': '沒有性格帶來的特色'},
'勤奮': {'up': '沒有性格帶來的特色', 'down': '沒有性格帶來的特色'},
'坦率': {'up': '沒有性格帶來的特色', 'down': '沒有性格帶來的特色'},
'浮躁': {'up': '沒有性格帶來的特色', 'down': '沒有性格帶來的特色'},
'認真': {'up': '沒有性格帶來的特色', 'down': '沒有性格帶來的特色'},
}