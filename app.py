import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

from util import (
    get_can_cook,
    category_list,
    curry_soup_list,
    salad_list,
    snack_drink_list,
    all_recipe_list,
    show_cols
)

st.set_page_config(page_title='Pokemon Sleep App', layout="wide")
st.title('Pokemon Sleep')

css='''
<style>
    section.main > div {
        max-width:90rem;
    }
    html, body {
        overflow-x: hidden;
    }
    body {
        position: relative
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

image = Image.open('pokemon_sleep.png')
st.image(image, use_column_width=True, output_format='png')

def get_ingredient_unique_list(df):
    ingredient_list = [
        *df['食材1'], 
        *df['食材2'],
        *df['食材3'],
        *df['食材4'],
    ]
    ingredient_unique_list = list(set(ingredient_list))
    ingredient_unique_list = [i for i in ingredient_unique_list if i is not np.nan]
    return ingredient_unique_list

df = pd.read_csv('recipe_transformed.csv')
ingredient_unique_list = get_ingredient_unique_list(df)

col1, col2 = st.columns(2)
with col1:
    have_ingredients = st.multiselect('食材', ingredient_unique_list)
    st.divider()
with col2:
    ingredients_str_list = ', '.join(have_ingredients)
    st.write(f"目前選擇的食材:")
    st.info(f"{ingredients_str_list}")
    can_cook = get_can_cook(df, have_ingredients)
    st.write(f"可料理食譜:")
    can_cook