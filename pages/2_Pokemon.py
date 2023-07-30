import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

from data.data_filepath import POKEMON_SHEET
from util import (
    load_gsheet_data,

)
st.set_page_config(page_title='Pokemon Sleep App', layout="wide")
st.title('Pokemon Sleep 寶可夢')
st.caption('寶可夢＆食材、樹果')

df = load_gsheet_data(POKEMON_SHEET)
df = df.replace('無', '')
df = df.fillna('')
ingredient_unique_list = df['食材'].unique()
ingredient_unique_list = ['全部'] + [i for i in ingredient_unique_list if i is not np.nan]
selected_ingredient = st.selectbox('食材', ingredient_unique_list)
df['all_ingredients'] = (
    df['食材'] + \
    df['食材.1'] + \
    df['食材.2']
)
df['來源島嶼'] = (
    df['萌綠之島'] + ' / ' + \
    df['天青沙灘'] + ' / ' + \
    df['灰褐洞窟'] + ' / ' + \
    df['白花雪原'] + ' / ' + \
    df['脂紅火山'] + ' / ' + \
    df['寶藍湖畔']
)
df['來源島嶼'] = df['來源島嶼'].apply(lambda x: x.strip(' / '))
df = df.rename(
    columns={
        '食材': '基本食材',
        '食材.1': 'Lv30食材',
        '食材.2': 'Lv60食材'
    }
)

if selected_ingredient != '全部':
    match_list = []
    for row in df.itertuples():
        if selected_ingredient in row.all_ingredients:
            match_list.append(row)
    match_df = pd.DataFrame(match_list)
else:
    match_df = df

match_df.set_index('名稱', inplace=True, drop=True)
cols = [
    # '進化條件',
    # '糖果數量',
    '樹果',
    '基本食材',
    'Lv30食材',
    'Lv60食材',
    # 'all_ingredients'
    '來源島嶼',
    # '萌綠之島',
    # '睡眠類型',
    # '天青沙灘',
    # '睡眠類型.1',
    # '灰褐洞窟',
    # '睡眠類型.2',
    # '白花雪原',
    # '睡眠類型.3',
    # '脂紅火山',
    # '睡眠類型.4',
    # '寶藍湖畔',
    # '睡眠類型.5',
]

def color_ingredients(val):
    color = '#ffff99'
    if val is not np.nan and selected_ingredient == val:
        return f'background-color: {color}'

match_df = match_df[cols]
st.dataframe(
    match_df.style.applymap(color_ingredients),
    use_container_width=True
)
