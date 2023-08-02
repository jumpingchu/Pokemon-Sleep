import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

from css.css_template import BASIC_CSS
from img.img_filepath import POKEMON_SLEEP_IMG, INGREDIENTS_IMG_LINKS
from data.data_filepath import RECIPE_TRANSFORMED
from util import (
    get_ingredient_unique_list,
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
st.markdown(BASIC_CSS, unsafe_allow_html=True)

image = Image.open(POKEMON_SLEEP_IMG)
st.image(image, use_column_width=True, output_format='png')

df = pd.read_csv(RECIPE_TRANSFORMED, index_col=0)
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
can_cook_filtered['食材1圖示'] = can_cook_filtered['食材1'].apply(lambda x: INGREDIENTS_IMG_LINKS.get(x, None))
can_cook_filtered['食材2圖示'] = can_cook_filtered['食材2'].apply(lambda x: INGREDIENTS_IMG_LINKS.get(x, None))
can_cook_filtered['食材3圖示'] = can_cook_filtered['食材3'].apply(lambda x: INGREDIENTS_IMG_LINKS.get(x, None))
can_cook_filtered['食材4圖示'] = can_cook_filtered['食材4'].apply(lambda x: INGREDIENTS_IMG_LINKS.get(x, None))
can_cook_filtered = can_cook_filtered[show_cols].set_index('食譜')
can_cook_filtered.dropna(axis='columns', how='all', inplace=True)
can_cook_filtered = can_cook_filtered.fillna('')
st.dataframe(
    can_cook_filtered.style.applymap(color_ingredients),
    column_config={
        "食材1圖示": st.column_config.ImageColumn("食材1圖示"),
        "食材2圖示": st.column_config.ImageColumn("食材2圖示"),
        "食材3圖示": st.column_config.ImageColumn("食材3圖示"),
        "食材4圖示": st.column_config.ImageColumn("食材4圖示")
    },
)