import streamlit as st
import pandas as pd
from PIL import Image

from img_util.parse_img import (
    TransformImage,
    pokemons,
    main_skills,
    sub_skills,
    natures
)

st.set_page_config(page_title='Pokemon Sleep App', layout="wide")
st.title('Pokemon Sleep 寶可夢能力計算機')
st.caption('上傳寶可夢的截圖，自動取得技能和性格等資訊')
st.warning('目前僅能辨識圖片，尚無計算功能', icon="⚠️")

uploaded_file = st.file_uploader("上傳寶可夢截圖", type=['jpg', 'png'])
st.divider()
if uploaded_file is not None:
    # 處理圖片
    img = Image.open(uploaded_file)
    transform_img = TransformImage(img)
    df_text = transform_img.run()
    
    # 顯示圖片
    st.header('上傳的圖片')
    st.image(img)
    
    # 擷取主技能
    main_skill_mask = (
        df_text['height'].between(34, 36)
        & df_text['left'].between(300, 320)
    )
    main_skill_in_df = df_text[main_skill_mask]['full_text'].values[0]
    
    # 擷取副技能
    sub_skills_mask = (
        df_text['height'].between(28, 32)
    )
    sub_skills_in_df = df_text[sub_skills_mask]
    try:
        lv10 = sub_skills_in_df[
            sub_skills_in_df['left'].between(200, 250)
            & sub_skills_in_df['top'].between(1200, 1300)
            ]['full_text'].values[0]
    except:
        lv10 = ''
    
    try:
        lv25 = sub_skills_in_df[
            sub_skills_in_df['left'].between(700, 750)
            & sub_skills_in_df['top'].between(1200, 1300)
            ]['full_text'].values[0]
    except:
        lv25 = ''
    
    try:
        lv50 = sub_skills_in_df[
            sub_skills_in_df['left'].between(200, 250)
            & sub_skills_in_df['top'].between(1400, 1500)
            ]['full_text'].values[0]
    except:
        lv50 = ''
    
    try:
        lv75 = sub_skills_in_df[
            sub_skills_in_df['left'].between(700, 750)
            & sub_skills_in_df['top'].between(1400, 1500)
            ]['full_text'].values[0]
    except:
        lv75 = ''
    
    try:
        lv100 = sub_skills_in_df[
            sub_skills_in_df['left'].between(200, 250)
            & sub_skills_in_df['top'].between(1600, 1700)
            ]['full_text'].values[0]
    except:
        lv100 = ''
    
    if len(main_skill_in_df) > 0:
        main_skills.insert(0, main_skill_in_df)

    
    # 顯示擷取結果到下拉式選單
    st.header('圖片辨識結果')

    pokemons.insert(0, '<請選擇>')
    st.selectbox('寶可夢', pokemons, index=0)
    st.selectbox('主技能', main_skills, index=0)
    
    if lv10 in sub_skills:
        idx = sub_skills.index(lv10)
        st.selectbox('副技能Lv10', sub_skills, index=idx)
    else:
        sub_skills.insert(0, '<請選擇>')
        st.selectbox('副技能Lv10', sub_skills, index=0)
    
    if lv25 in sub_skills:
        idx = sub_skills.index(lv25)
        st.selectbox('副技能Lv25', sub_skills, index=idx)
    else:
        sub_skills.insert(0, '<請選擇>')
        st.selectbox('副技能Lv25', sub_skills, index=0)
    
    if lv50 in sub_skills:
        idx = sub_skills.index(lv50)
        st.selectbox('副技能Lv50', sub_skills, index=idx)
    else:
        sub_skills.insert(0, '<請選擇>')
        st.selectbox('副技能Lv50', sub_skills, index=0)
    
    if lv75 in sub_skills:
        idx = sub_skills.index(lv75)
        st.selectbox('副技能Lv75', sub_skills, index=idx)
    else:
        sub_skills.insert(0, '<請選擇>')
        st.selectbox('副技能Lv75', sub_skills, index=0)
    
    if lv100 in sub_skills:
        idx = sub_skills.index(lv100)
        st.selectbox('副技能Lv100', sub_skills, index=idx)
    else:
        sub_skills.insert(0, '<請選擇>')
        st.selectbox('副技能Lv100', sub_skills, index=0)
    
    nature_selected = st.selectbox('性格', natures, index=0)
    st.write(':small_red_triangle: UP: ', natures[nature_selected]['up'])
    st.write(':small_blue_diamond: DOWN: ', natures[nature_selected]['down'])
    
else:
    st.write('截圖範例（左上角寶可夢方框剛好遮住第一個食材）')
    st.image('img/test3.PNG', width=200)
