import streamlit as st
import pandas as pd
import numpy as np

from util import (
    get_can_cook,
    category_list,
    curry_soup_list,
    salad_list,
    snack_drink_list,
    all_recipe_list,
    show_cols
)

st.set_page_config(layout="wide")
st.title('Pokemon Sleep')

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
with col2:
    ingredients_str_list = ', '.join(have_ingredients)
    st.write(f"目前選擇的食材:")
    st.info(f"{ingredients_str_list}")
    can_cook = get_can_cook(df, have_ingredients)
    can_cook