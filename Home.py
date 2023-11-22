import streamlit as st
from PIL import Image
from img.img_filepath import POKEMON_SLEEP_IMG
from streamlit.components.v1 import html


class Pages:
    base_url = "https://pokemon-sleep.streamlit.app/"
    calculator = base_url + "潛力計算機"
    recipe = base_url + "Recipe"
    pokemon_info = base_url + "Pokemon"


st.title("Pokemon Sleep 小幫手首頁")
image = Image.open(POKEMON_SLEEP_IMG)
st.image(image, use_column_width=True, output_format="png")

col1, col2, col3 = st.columns(3)
with col1:
    image1 = Image.open("img/calculator.jpeg")
    image1 = image1.resize((600, 500))
    st.image(image1)
    st.link_button("寶可夢潛力計算機", Pages.calculator, type="primary", use_container_width=True)
with col2:
    image1 = Image.open("img/recipe.png")
    image1 = image1.resize((600, 500))
    st.image(image1)
    st.link_button("食材與料理食譜", Pages.recipe, type="primary", use_container_width=True)
with col3:
    image1 = Image.open("img/pokemon.png")
    image1 = image1.resize((600, 500))
    st.image(image1)
    st.link_button("寶可夢資料與食材", Pages.pokemon_info, type="primary", use_container_width=True)
