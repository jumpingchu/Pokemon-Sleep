import streamlit as st
import pandas as pd
from PIL import Image

from img_util.parse_img import TransformImage

st.set_page_config(page_title='Pokemon Sleep App', layout="wide")
st.title('Pokemon Sleep 寶可夢能力計算機')
st.caption('上傳寶可夢的截圖，自動取得技能和性格等資訊')
st.warning('施工中', icon="⚠️")

uploaded_file = st.file_uploader("上傳寶可夢截圖", type=['jpg', 'png'])
st.divider()
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    transform_img = TransformImage(img)
    df_text = transform_img.run()
    img_col, info_col = st.columns(2)
    with img_col:
        st.image(img)
    with info_col:
        st.dataframe(df_text)
else:
    st.write('截圖範例（左上角寶可夢方框剛好遮住第一個樹果）')
    st.image('img/test3.PNG', width=600)
