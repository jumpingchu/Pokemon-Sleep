# import warnings; warnings.filterwarnings('ignore')
# import pandas as pd
# from data_filepath import RECIPE_SHEET
# from util import (
#     load_gsheet_data,
#     get_ingredient_unique_list,
#     all_recipe_dict
# )

# data = load_gsheet_data(RECIPE_SHEET)

# df = data.copy()
# df.dropna(axis=1, how="all", inplace=True)
# df.fillna('', inplace=True)
# df.replace('無', '', inplace=True)

# food_unique_list = get_ingredient_unique_list(df)

# df['食材1數量'] = df['食材1'] + df['食材1數量']
# df['食材2數量'] = df['食材2'] + df['食材2數量']
# df['食材3數量'] = df['食材3'] + df['食材3數量']
# df['食材4數量'] = df['食材4'] + df['食材4數量']
# df['all_food'] = df['食材1'] + df['食材2'] + df['食材3'] + df['食材4'] 

# def get_category(x):
#     if x in all_recipe_dict['咖哩/濃湯']:
#         return '咖哩/濃湯'
#     elif x in all_recipe_dict['沙拉']:
#         return '沙拉'
#     elif x in all_recipe_dict['點心/飲料']:
#         return '點心/飲料'
#     else:
#         return '其他'

# df['分類'] = df['食譜'].apply(get_category)

# df.to_csv('data/transformed/recipe_transformed.csv')
