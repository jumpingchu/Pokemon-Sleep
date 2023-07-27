import pandas as pd
import streamlit as st

category_list = ['全部', '咖哩/濃湯', '沙拉', '點心/飲料']
curry_soup_list = [
    '特選蘋果咖哩',
    '炙燒尾肉咖哩',
    '太陽之力番茄咖哩',
    '絕對睡眠奶油咖哩',
    '辣味蔥勁十足咖哩',
    '蘑菇孢子咖哩',
    '親子愛咖哩',
    '吃飽飽起司肉排咖哩',
    '窩心白醬濃湯',
    '單純白醬濃湯',
    '豆製肉排咖哩',
    '寶寶甜蜜咖哩',
    '忍者咖哩',
    '日照炸肉排咖哩',
    '入口即化蛋捲咖哩',
    '健美豆子咖哩',
]

salad_list = [
    '呆呆獸尾巴的胡椒沙拉',
    '蘑菇孢子沙拉',
    '撥雪凱撒沙拉',
    '貪吃鬼洋芋沙拉',
    '濕潤豆腐沙拉',
    '蠻力豪邁沙拉',
    '豆製火腿沙拉',
    '好眠番茄沙拉',
    '哞哞起司番茄沙拉',
    '心情不定肉沙拉淋巧克力醬',
    '過熱沙拉',
    '特選蘋果沙拉',
    '免疫蔥花沙拉',
    '迷人蘋果起司沙拉',
    '忍者沙拉',
    '熱風豆腐沙拉',
]

snack_drink_list = [
    '熟成甜薯燒',
    '不屈薑餅',
    '特選蘋果汁',
    '手製勁爽汽水',
    '火花薑茶',
    '胖丁百匯布丁',
    '惡魔之吻水果牛奶',
    '祈願蘋果派',
    '橙夢的排毒茶',
    '甜甜香氣巧克力蛋糕',
    '哞哞熱鮮奶',
    '輕裝豆香蛋糕',
    '活力蛋白飲',
    '我行我素蔬菜汁',
    '大馬拉薩達',
    '大力士豆香甜甜圈',
]

all_recipe_list = ['全部'] + curry_soup_list + salad_list + snack_drink_list

show_cols = [
    '食譜',
    '分類',
    '食材1數量', 
    '食材2數量', 
    '食材3數量', 
    '食材4數量'
]

@st.cache_data
def get_can_cook(df, have_ingredients):
    index_match = []
    for row in df.itertuples():
        if all(i in row.all_food for i in have_ingredients):
            index_match.append(row.Index)

    can_cook = df.iloc[index_match]

    if len(can_cook) > 0:
        can_cook = can_cook[show_cols]
    else:
        can_cook = df[show_cols]

    return can_cook[show_cols].set_index('食譜').T