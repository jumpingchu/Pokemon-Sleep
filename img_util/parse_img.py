import re
import warnings; warnings.filterwarnings('ignore')
import pandas as pd
from paddleocr import PaddleOCR

class TransformImage:
    def __init__(self, img):
        self.img = img
        self.lang = "chinese_cht"
    
    def extract_text_from_img(self):
        ocr = PaddleOCR(lang=self.lang, show_log=False)
        result = ocr.ocr(self.img, cls=False)
        return result[0]
    
    def filter_text(self, result):
        info = {}
        sub_skill_idx = 1
        for idx, line in enumerate(result):
            text = line[1][0].strip()
            text = text.upper()
            # if find_zh(text):
            #     filter_result.append((idx, text))
            if idx < 10 and text in pokemons:
                info['pokemon'] = text
            elif idx > 10 and text in main_skills:
                info['main_skill'] = text
            elif idx > 25 and text in natures:
                info['nature'] = text
            elif text in sub_skills:
                info[f'sub_skill_{sub_skill_idx}'] = text
                sub_skill_idx += 1
            else:
                pass

        return info
    
    def run(_self):
        result = _self.extract_text_from_img()
        info = _self.filter_text(result)
        return info
    
main_skills = [
    '---',
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
    '---',
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
    '---',
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
    '---': {'up': '---', 'down': '---'},
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