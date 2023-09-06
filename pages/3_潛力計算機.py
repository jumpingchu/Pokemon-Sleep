import streamlit as st
from PIL import Image
from pymongo.mongo_client import MongoClient

st.set_page_config(page_title='Pokemon Sleep App', layout="wide")
st.title('Pokemon Sleep 寶可夢潛力計算機')
st.caption('上傳寶可夢的截圖，自動取得圖片資訊，並可一鍵計算潛力評價')

uploaded_file = st.file_uploader("上傳截圖", type=['jpg', 'png'])
st.divider()

if uploaded_file is not None:
    
    from img_util.parse_img import (
        TransformImage,
        pokemons,
        main_skills,
        sub_skills,
        natures
    )
    
    with st.status("圖片上傳中...") as status:
        
        @st.cache_data(max_entries=10)
        def process_img(uploaded_file):
            # 處理圖片
            img = uploaded_file.getvalue()
            status.update(label="辨識圖片中...", state="running")
            transform_img = TransformImage(img)
            info = transform_img.run()
            status.update(label="圖片辨識完成！", state="complete")
            return info
        
        info = process_img(uploaded_file)
        status.update(label="圖片辨識完成！", state="complete")
    
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
            pokemon = st.selectbox(':orange[寶可夢]', pokemons)
        
        # Main Skills
        try:
            main_skill = st.text_input('主技能', value=f"{info['main_skill']}")
        except:
            main_skill = st.selectbox(':orange[主技能]', main_skills)
        
        # Sub Skills
        try:
            sub_skill_1 = st.text_input('副技能1', value=f"{info['sub_skill_1']}")
        except:
            sub_skill_1 = st.selectbox(':orange[副技能1]', sub_skills)   
        try:
            sub_skill_2 = st.text_input('副技能2', value=f"{info['sub_skill_2']}")
        except:
            sub_skill_2 = st.selectbox(':orange[副技能2]', sub_skills)            
        try:
            sub_skill_3 = st.text_input('副技能3', value=f"{info['sub_skill_3']}")
        except:
            sub_skill_3 = st.selectbox(':orange[副技能3]', sub_skills)            
        try:
            sub_skill_4 = st.text_input('副技能4', value=f"{info['sub_skill_4']}")
        except:
            sub_skill_4 = st.selectbox(':orange[副技能4]', sub_skills)            
        try:
            sub_skill_5 = st.text_input('副技能5', value=f"{info['sub_skill_5']}")
        except:
            sub_skill_5 = st.selectbox(':orange[副技能5]', sub_skills)            
        
        sub_skills = [
            sub_skill_1,
            sub_skill_2,
            sub_skill_3,
            sub_skill_4,
            sub_skill_5
            ]

        username = st.secrets["db_username"]
        password = st.secrets["db_password"]
        uri = f"mongodb+srv://{username}:{password}@cluster0.dhzzdc6.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        db = client['PokemonSleep']
        ingredient_collection = db['Ingredient']
        ingredient_all = ingredient_collection.find({})
        ingredient_list = list(set([i['_id'] for i in ingredient_all]))
        try:
            pokemon_collection = db['Pokemon']
            pokemon_info = pokemon_collection.find_one(pokemon)
            ingredient = pokemon_info['ingredient']
            ingredient_num = pokemon_info['ingredient_num']
            ingredient_1 = st.text_input('食材1', value=ingredient)
            ingredient_num_1 = st.slider('食材1數量', value=ingredient_num, min_value=1, max_value=10, step=1)
        except:
            ingredient_1 = st.selectbox(':orange[食材1]', ingredient_list)
            ingredient_num_1 = st.slider(':orange[食材1數量]', value=1, min_value=1, max_value=10, step=1)
        
        ingredient_2 = st.selectbox(':orange[食材2]', ingredient_list, index=ingredient_list.index(ingredient_1))
        ingredient_num_2 = st.slider(':orange[食材2數量]', value=2, min_value=1, max_value=10, step=1)

        ingredient_3 = st.selectbox(':orange[食材3]', ingredient_list, index=ingredient_list.index(ingredient_1))
        ingredient_num_3 = st.slider(':orange[食材3數量]', value=4, min_value=1, max_value=10, step=1)
        
        # Nature
        try:
            nature = st.text_input('性格', value=f"{info.get('nature', '')}")
        except:
            nature = st.selectbox(':orange[性格]', natures.keys())

        st.write(':small_red_triangle: UP: ', natures[nature]['up'])
        st.write(':small_blue_diamond: DOWN: ', natures[nature]['down'])
        
        submitted = st.form_submit_button("計算能力")
        if submitted:
            with st.status("計算中...") as status:
                from img_util.calculator import calculator
                energy_score, rank = calculator(
                    uri, 
                    pokemon, 
                    main_skill, 
                    nature, 
                    sub_skills, 
                    ingredient_2,
                    ingredient_num_2,
                    ingredient_3,
                    ingredient_num_3
                )
                status.update(label="計算完成！", state="complete", expanded=True)
                
                st.header(f"能量積分: :blue[{energy_score}]")
                if rank == 'C':
                    st.header(f"評價: :blue[{rank}]")
                elif rank == 'B':
                    st.header(f"評價: :violet[{rank}]")
                elif rank == 'A':
                    st.header(f"評價: :red[{rank}]")
                elif 'S' in rank:
                    st.header(f"評價: :rainbow[{rank}]")
                else:
                    st.header(f"評價: {rank}")
            

else:
    st.write('截圖範例（左上角寶可夢方框剛好遮住第一個食材）')
    st.image('img/test3.PNG', width=200)
