import os
import streamlit as st
from PIL import Image
from google.cloud import bigquery as bq
from google.oauth2 import service_account

st.set_page_config(page_title="Pokemon Sleep App", layout="wide")
st.title("Pokemon Sleep 寶可夢潛力計算機")
st.caption("上傳寶可夢的截圖，自動取得圖片資訊，並可一鍵計算潛力評價")
st.caption("- 2024/02/01 更新最新寶可夢，包含童偶熊、拉魯拉絲、迷你龍")
st.caption("- 並且依照原計算機的調整：調降夢之碎片的能量值")

uploaded_file = st.file_uploader("上傳截圖", type=["jpg", "png"])
st.divider()

if uploaded_file is not None:
    with st.status("圖片上傳中...") as status:
        from pages.util.util import process_img
        img = uploaded_file.getvalue()
        status.update(label="辨識圖片中...", state="running")
        info = process_img(img)
        status.update(label="圖片辨識完成！", state="complete")

    # 顯示圖片
    # st.header('上傳的圖片')
    st.image(Image.open(uploaded_file))

    # 顯示擷取結果到文字輸入框
    st.header("圖片辨識結果")

    with st.form("my_form"):

        if info["pokemon"]:
            from pages.util.util import (
                get_pokemon_info_from_bq,
                get_rank_color_text,
                get_item_list_from_bq,
                get_nature_dict_from_bq,
                get_ingredient_dict_from_bq,
            )
            from google.cloud import bigquery as bq

            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"]
            )
            client = bq.Client(credentials=credentials)

            # Pokemon
            pokemon_info = get_pokemon_info_from_bq(info["pokemon"])
            show_info = {
                'name': '寶可夢',
                'fruit': '樹果',
                'ingredient': '食材 1',
                'main_skill': '主技能',
            }
            for k, v in pokemon_info.items():
                if k in show_info.keys():
                    k_zhtw = show_info.get(k)
                    st.markdown(f'- **{k_zhtw}**: {v}')

            # Sub Skills
            sub_skills_list = get_item_list_from_bq("SubSkill")
            sub_skills_list = sorted(sub_skills_list)
            sub_skills_list.insert(0, "---")
            try:
                sub_skill_1 = st.text_input("副技能1", value=f"{info['sub_skill_1']}")
            except:
                sub_skill_1 = st.selectbox(":orange[副技能1]", sub_skills_list)
            try:
                sub_skill_2 = st.text_input("副技能2", value=f"{info['sub_skill_2']}")
            except:
                sub_skill_2 = st.selectbox(":orange[副技能2]", sub_skills_list)
            try:
                sub_skill_3 = st.text_input("副技能3", value=f"{info['sub_skill_3']}")
            except:
                sub_skill_3 = st.selectbox(":orange[副技能3]", sub_skills_list)
            try:
                sub_skill_4 = st.text_input("副技能4", value=f"{info['sub_skill_4']}")
            except:
                sub_skill_4 = st.selectbox(":orange[副技能4]", sub_skills_list)
            try:
                sub_skill_5 = st.text_input("副技能5", value=f"{info['sub_skill_5']}")
            except:
                sub_skill_5 = st.selectbox(":orange[副技能5]", sub_skills_list)

            sub_skills = [sub_skill_1, sub_skill_2, sub_skill_3, sub_skill_4, sub_skill_5]

            # Ingredient 2 and 3
            ingredient_list = get_item_list_from_bq("Ingredient")
            ingredient_list.insert(0, "---")
            ingredient_2 = st.selectbox(
                ":orange[食材2]", ingredient_list, index=ingredient_list.index(pokemon_info['ingredient'])
            )
            ingredient_2_num = st.slider(
                ":orange[食材2數量]", value=2, min_value=1, max_value=10, step=1
            )

            ingredient_3 = st.selectbox(
                ":orange[食材3]", ingredient_list, index=ingredient_list.index(pokemon_info['ingredient'])
            )
            ingredient_3_num = st.slider(
                ":orange[食材3數量]", value=4, min_value=1, max_value=10, step=1
            )

            # Nature
            nature = st.text_input("性格", value=f"{info.get('nature', '')}")
            if nature:
                nature_data = get_nature_dict_from_bq(nature)
                nature_up = nature_data["up"] if nature_data["up"] else '無性格效果'
                nature_down = nature_data["down"] if nature_data["down"] else '無性格效果'
                st.write(":small_red_triangle: UP: ", nature_up)
                st.write(":small_blue_diamond: DOWN: ", nature_down)
                submitted = st.form_submit_button("計算能力")

            if submitted:
                with st.status("計算中...") as status:
                    from img_util.calculator import calculator
                    ingredient_2_energy = get_ingredient_dict_from_bq(ingredient_2)['energy']
                    ingredient_3_energy = get_ingredient_dict_from_bq(ingredient_3)['energy']
                    info_dict = {
                        'pokemon_info': pokemon_info,
                        'nature_up': nature_up,
                        'nature_down': nature_down,
                        'sub_skills': sub_skills,
                        'ingredient_2_num': int(ingredient_2_num),
                        'ingredient_2_energy': int(ingredient_2_energy),
                        'ingredient_3_num': int(ingredient_3_num),
                        'ingredient_3_energy': int(ingredient_3_energy),
                    }

                    energy_score, rank = calculator(**info_dict)
                    status.update(label="計算完成！", state="complete", expanded=True)

                    st.header(f"能量積分: :blue[{energy_score}]")
                    st.header(get_rank_color_text(rank))
        else:
            print('無法辨識寶可夢名稱！請更換圖片後再試試看～')

else:
    st.header("截圖範例")
    st.write("左上角寶可夢方框剛好「遮住第一個食材」，並且最底部剛好出現「性格」")
    st.image("img/test1.PNG")
