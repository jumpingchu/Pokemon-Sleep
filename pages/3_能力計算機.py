import streamlit as st
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

uploaded_file = st.file_uploader("上傳寶可夢截圖", type=['jpg', 'png'])
st.divider()
if uploaded_file is not None:
    
    with st.status("圖片上傳中...") as status:
        
        @st.cache_data()
        def process_img(uploaded_file):
            # 處理圖片
            img = uploaded_file.getvalue()
            status.update(label="辨識圖片中...", state="running")
            transform_img = TransformImage(img)
            info = transform_img.run()
            status.update(label="圖片辨識完成！", state="complete")
            return info
        
        status.update(label="圖片辨識完成！", state="complete")
        info = process_img(uploaded_file)
    
    # 顯示圖片
    # st.header('上傳的圖片')
    st.image(Image.open(uploaded_file))
    
    # 顯示擷取結果到文字輸入框
    st.header('圖片辨識結果')
    
    with st.form("my_form"):

        # Pokemon
        try:
            pokemon = st.text_input('寶可夢',  value=f"{info['pokemon']}")
        except:
            pokemon = st.selectbox('寶可夢', pokemons)
        
        # Main Skills
        try:
            main_skill = st.text_input('主技能', value=f"{info['main_skill']}")
        except:
            main_skill = st.selectbox('寶可夢', main_skills)
        
        # Sub Skills
        try:
            sub_skill_1 = st.text_input('副技能1', value=f"{info['sub_skill_1']}")
        except:
            sub_skill_1 = st.selectbox('寶可夢', sub_skills)   
        try:
            sub_skill_2 = st.text_input('副技能2', value=f"{info['sub_skill_2']}")
        except:
            sub_skill_2 = st.selectbox('寶可夢', sub_skills)            
        try:
            sub_skill_3 = st.text_input('副技能3', value=f"{info['sub_skill_3']}")
        except:
            sub_skill_3 = st.selectbox('寶可夢', sub_skills)            
        try:
            sub_skill_4 = st.text_input('副技能4', value=f"{info['sub_skill_4']}")
        except:
            sub_skill_4 = st.selectbox('寶可夢', sub_skills)            
        try:
            sub_skill_5 = st.text_input('副技能5', value=f"{info['sub_skill_5']}")
        except:
            sub_skill_5 = st.selectbox('寶可夢', sub_skills)            
        
        # Nature
        try:
            nature = st.text_input('性格', value=f"{info.get('nature', '')}")
        except:
            nature = st.selectbox('寶可夢', natures)            

        st.write(':small_red_triangle: UP: ', natures[nature]['up'])
        st.write(':small_blue_diamond: DOWN: ', natures[nature]['down'])
        
        submitted = st.form_submit_button("計算能力")
        if submitted:
            st.write(f"{pokemon=}")
            st.write(f"{main_skill=}")
            st.write(f"{sub_skill_1=}")
            st.write(f"{sub_skill_2=}")
            st.write(f"{sub_skill_3=}")
            st.write(f"{sub_skill_4=}")
            st.write(f"{sub_skill_5=}")
            st.write(f"{nature=}")

else:
    st.write('截圖範例（左上角寶可夢方框剛好遮住第一個食材）')
    st.image('img/test3.PNG', width=200)
