import os
import pandas as pd
import numpy as np
import streamlit as st
from google.cloud import bigquery as bq
from google.oauth2 import service_account
from img_util.parse_img import TransformImage

# Create API client.

category_list = ["全部", "點心/飲料", "沙拉", "咖哩/濃湯"]
curry_soup_list = [
    "特選蘋果咖哩",
    "炙燒尾肉咖哩",
    "太陽之力番茄咖哩",
    "絕對睡眠奶油咖哩",
    "辣味蔥勁十足咖哩",
    "蘑菇孢子咖哩",
    "親子愛咖哩",
    "吃飽飽起司肉排咖哩",
    "窩心白醬濃湯",
    "單純白醬濃湯",
    "豆製肉排咖哩",
    "寶寶甜蜜咖哩",
    "忍者咖哩",
    "日照炸肉排咖哩",
    "入口即化蛋捲咖哩",
    "健美豆子咖哩",
]
salad_list = [
    "呆呆獸尾巴的胡椒沙拉",
    "蘑菇孢子沙拉",
    "撥雪凱撒沙拉",
    "貪吃鬼洋芋沙拉",
    "濕潤豆腐沙拉",
    "蠻力豪邁沙拉",
    "豆製火腿沙拉",
    "好眠番茄沙拉",
    "哞哞起司番茄沙拉",
    "心情不定肉沙拉淋巧克力醬",
    "過熱沙拉",
    "特選蘋果沙拉",
    "免疫蔥花沙拉",
    "迷人蘋果起司沙拉",
    "忍者沙拉",
    "熱風豆腐沙拉",
]
snack_drink_list = [
    "熟成甜薯燒",
    "不屈薑餅",
    "特選蘋果汁",
    "手製勁爽汽水",
    "火花薑茶",
    "胖丁百匯布丁",
    "惡魔之吻水果牛奶",
    "祈願蘋果派",
    "橙夢的排毒茶",
    "甜甜香氣巧克力蛋糕",
    "哞哞熱鮮奶",
    "輕裝豆香蛋糕",
    "活力蛋白飲",
    "我行我素蔬菜汁",
    "大馬拉薩達",
    "大力士豆香甜甜圈",
]

all_recipe_dict = {
    "全部": ["全部"] + curry_soup_list + salad_list + snack_drink_list,
    "點心/飲料": ["全部"] + snack_drink_list,
    "沙拉": ["全部"] + salad_list,
    "咖哩/濃湯": ["全部"] + curry_soup_list,
}

show_cols = [
    "食譜",
    # '分類',
    # '食材1圖示',
    "食材1數量",
    # '食材2圖示',
    "食材2數量",
    # '食材3圖示',
    "食材3數量",
    # '食材4圖示',
    "食材4數量",
]


def get_ingredient_unique_list(df):
    ingredient_list = [
        *df["食材1"],
        *df["食材2"],
        *df["食材3"],
        *df["食材4"],
    ]
    ingredient_unique_list = list(set(ingredient_list))
    ingredient_unique_list = [i for i in ingredient_unique_list if i is not np.nan]
    return ingredient_unique_list


# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)  # Time to Live = 600 seconds
def load_gsheet_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url, on_bad_lines="skip")


@st.cache_data
def get_can_cook(df, have_ingredients, match_mode):
    if not have_ingredients:
        return df

    index_match = []
    for row in df.itertuples():
        if match_mode == "任一食材符合":
            if any(i in row.all_food for i in have_ingredients):
                index_match.append(row.Index)
        else:
            if all(i in row.all_food for i in have_ingredients):
                index_match.append(row.Index)

    can_cook = df.iloc[index_match]
    return can_cook


def filter_category(df, category):
    return df.query(f"分類 == '{category}'") if category != "全部" else df


def filter_recipe(df, recipe):
    return df.query(f"食譜 == '{recipe}'") if recipe != "全部" else df


@st.cache_data
def get_pokemon_info_from_bq(pokemon):
    sql = f"""
        SELECT
            p.* EXCEPT (_airbyte_raw_id,
                _airbyte_extracted_at,
                _airbyte_meta),
            i.name AS ingredient,
            i.energy AS ingredient_energy,
            f.name AS fruit,
            f.lv60_energy AS fruit_energy,
            m.name AS main_skill,
            m.Lv1,
            m.Lv2,
            m.Lv3,
            m.Lv4,
            m.Lv5,
            m.Lv6,
        FROM
            `PokemonSleep.Pokemon` AS p
        JOIN
            `PokemonSleep.Ingredient` AS i
        ON
            i.name = p.ingredient
        JOIN
            `PokemonSleep.Fruit` AS f
        ON
            f.name = p.fruit
        JOIN
            `PokemonSleep.MainSkill` AS m
        ON
            m.name = p.main_skill
        WHERE p.name = '{pokemon}'
    """
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bq.Client(credentials=credentials)
    query_job = client.query(sql)
    result_dict = [dict(result) for result in query_job][0]
    return result_dict


@st.cache_data
def get_item_list_from_bq(table_name):
    sql = f"""
        SELECT
            DISTINCT(name)
        FROM
            `PokemonSleep.{table_name}`
    """
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bq.Client(credentials=credentials)
    query_job = client.query(sql)
    result_list = [result.values()[0] for result in query_job]
    return result_list


@st.cache_data
def get_nature_dict_from_bq(nature_name):
    sql = f"""
        SELECT
            name,
            up,
            down,
        FROM
            `PokemonSleep.Nature`
        WHERE name = '{nature_name}'
    """
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bq.Client(credentials=credentials)
    query_job = client.query(sql)
    result_dict = [dict(result) for result in query_job][0]
    return result_dict

@st.cache_data
def get_ingredient_dict_from_bq(ingredient):
    sql = f"""
        SELECT
            name,
            energy,
        FROM
            `PokemonSleep.Ingredient`
        WHERE name = '{ingredient}'
    """
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bq.Client(credentials=credentials)
    query_job = client.query(sql)
    result_dict = [dict(result) for result in query_job][0]
    return result_dict

def get_rank_color_text(rank):
    rank_color_dict = {
        "SSS": f"評價: :rainbow[{rank}]",
        "SS": f"評價: :rainbow[{rank}]",
        "S": f"評價: :rainbow[{rank}]",
        "A": f"評價: :red[{rank}]",
        "B": f"評價: :violet[{rank}]",
        "C": f"評價: :blue[{rank}]",
        "D": f"評價: {rank}",
        "E": f"評價: {rank}",
    }
    return rank_color_dict.get(rank)


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets['bq_credentials_filepath']
# client = bq.Client()
# get_nature_dict_from_bq(client, '認真')


@st.cache_data(max_entries=3)
def process_img(img):
    transform_img = TransformImage(img)
    info = transform_img.run()
    return info
