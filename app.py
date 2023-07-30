import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

from util import (
    get_can_cook,
    category_list,
    all_recipe_dict,
    filter_category,
    filter_recipe,
    show_cols
)

st.set_page_config(page_title='Pokemon Sleep App', layout="wide")
st.title('Pokemon Sleep 食譜')
st.caption('利用自己現有的食材篩選能做出哪些食譜料理')

css='''
<style>
    section.main > div {
        max-width:90rem;
    }
    html, body {
        overflow-x: hidden;
    }
    body {
        width: 100%;
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

df = pd.read_csv('recipe_transformed.csv', index_col=0)
ingredient_unique_list = get_ingredient_unique_list(df)

ingredient_col, match_mode_col = st.columns([2, 1])
with ingredient_col:
    have_ingredients = st.multiselect(
        '食材', 
        ingredient_unique_list,
        placeholder='請選擇食材（可多選）'
    )
with match_mode_col:
    # match_mode = st.checkbox('任一食材符合', False)
    match_mode = st.radio('篩選方式', ['所有食材符合', '任一食材符合'], 0)

category_col, recipe_col = st.columns(2)
with category_col:
    category = st.selectbox('食譜分類', category_list)
with recipe_col:
    recipe = st.selectbox('食譜名稱', all_recipe_dict.get(category, all_recipe_dict['全部']))

st.divider()

ingredients_str_list = ', '.join(have_ingredients) if have_ingredients else '全部'
st.write(f"目前選擇的食材:")
st.info(f"{ingredients_str_list}")

can_cook = get_can_cook(df, have_ingredients, match_mode)
can_cook_filtered = (
    can_cook
    .pipe(filter_category, category)
    .pipe(filter_recipe, recipe)
)

def color_ingredients(val):
    color = '#ffff99'
    if val is not np.nan and any(i in val for i in have_ingredients):
        return f'background-color: {color}'

st.write(f"可料理食譜:")
can_cook_filtered = can_cook_filtered[show_cols].set_index('食譜').T
can_cook_filtered = can_cook_filtered.fillna('')
st.dataframe(can_cook_filtered.style.applymap(color_ingredients))
