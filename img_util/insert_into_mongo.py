from pymongo.mongo_client import MongoClient
import pandas as pd
import streamlit as st

username = st.secrets["db_username"]
password = st.secrets["db_password"]
uri = f"mongodb+srv://{username}:{password}@cluster0.dhzzdc6.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)
db = client['PokemonSleep']
# collection = db['Nature']
collection = db['Pokemon']

df = pd.read_csv('img_util/pokemon.csv')

for row in df.itertuples():
    payload = {
        '_id': row.pokemon,
        'final_evolution': row.final_evolution,
        'final_help_interval': row.final_help_interval,
        'fruit': row.fruit,
        'type': row.type,
        'main_skill': row.main_skill,
        'final_evolution_step': row.final_evolution_step,
        'carry_limit': row.carry_limit,
        'ingredient': row.ingredient,
        'ingredient_num': row.ingredient_num
    }
    try:
        collection.insert_one(payload)
        # collection.insert_many(ingredients)
        # x = collection.delete_many({})
        # print(x.deleted_count)
    except Exception as e:
        print(e)

# def get_data_by_id(_id: str):
#     query = collection.find_one({'_id': _id})#.limit(int(offset))
#     print(f"{query['up']=}")
#     print(f"{query['down']=}")

# get_data_by_id('樂天')
