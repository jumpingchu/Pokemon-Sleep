import os
from pymongo.mongo_client import MongoClient
import pandas as pd
import streamlit as st


def load_gsheet_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(csv_url, on_bad_lines="skip")
    return df


def conn_mongodb(username, password):
    uri = f"mongodb+srv://{username}:{password}@cluster0.dhzzdc6.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client["PokemonSleep"]
    # collection = db['Nature']
    collection = db["Pokemon"]
    return collection


mapping_cols_name = {
    "Unnamed: 0": "pokemon",
    "最終型態": "final_evolution",
    "最終幫忙間隔(秒)": "final_help_interval",
    "樹果": "fruit",
    "類型": "type",
    "技能": "main_skill",
    "最終進化階段": "final_evolution_step",
    "格子": "carry_limit",
    "食材1": "ingredient",
    "食材1數量": "ingredient_num",
}

pokemon_gsheet_url = "https://docs.google.com/spreadsheets/d/1XXel48BKuxa8sACD7vzS7k9TZLDF8QSugymO3Em942A/edit#gid=1569801725"
new_df = load_gsheet_data(pokemon_gsheet_url)
new_df = new_df[1:]  # Remove 1st sample row
new_df = new_df.rename(columns=mapping_cols_name)
current_df = pd.read_csv("img_util/current_pokemons.csv", index_col=0)
new_update_pokemons = new_df[~new_df.isin(current_df)].dropna()

username = st.secrets["db_username"]
password = st.secrets["db_password"]
collection = conn_mongodb(username, password)

for row in new_update_pokemons.itertuples():
    payload = {
        "_id": row.pokemon,
        "final_evolution": row.final_evolution,
        "final_help_interval": row.final_help_interval,
        "fruit": row.fruit,
        "type": row.type,
        "main_skill": row.main_skill,
        "final_evolution_step": row.final_evolution_step,
        "carry_limit": row.carry_limit,
        "ingredient": row.ingredient,
        "ingredient_num": row.ingredient_num,
    }
    print(payload)
    try:
        collection.insert_one(payload)
        # collection.insert_many(ingredients)
        # x = collection.delete_many({})
        # print(x.deleted_count)
    except Exception as e:
        print(e)

os.system("mv img_util/current_pokemons.csv img_util/updated/current_pokemons.csv")
new_df.to_csv("img_util/current_pokemons.csv")

# def get_data_by_id(_id: str):
#     query = collection.find_one({'_id': _id})#.limit(int(offset))
#     print(f"{query['up']=}")
#     print(f"{query['down']=}")

# get_data_by_id('樂天')
