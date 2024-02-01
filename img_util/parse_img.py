import re
from datetime import datetime
import streamlit as st
from pymongo.mongo_client import MongoClient
import warnings; warnings.filterwarnings('ignore')
from paddleocr import PaddleOCR

# Connect MongoDB to get possible item lists
def connect_mongodb():
    username = st.secrets["db_username"]
    password = st.secrets["db_password"]
    uri = f"mongodb+srv://{username}:{password}@cluster0.dhzzdc6.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db_conn = client['PokemonSleep']
    return db_conn

def get_db_item_list(db_conn, target_collection):
    collection = db_conn[target_collection]
    item_all = collection.find({})
    item_list = list(set([i['_airbyte_data']['_id'] for i in item_all]))
    item_list.insert(0, '---')
    return item_list

db_conn = connect_mongodb()
pokemons_list = get_db_item_list(db_conn, 'airbyte_raw_Pokemon')
main_skills_list = get_db_item_list(db_conn, 'airbyte_raw_MainSkill')
sub_skills_list = get_db_item_list(db_conn, 'airbyte_raw_SubSkill')
natures_list = get_db_item_list(db_conn, 'airbyte_raw_Nature')
ingredient_list = get_db_item_list(db_conn, 'airbyte_raw_Ingredient')

class TransformImage:
    def __init__(self, img):
        self.img = img
        self.lang = "chinese_cht"
    
    def extract_text_from_img(self):
        # 設定辨識語言、不顯示 log
        ocr = PaddleOCR(lang=self.lang, show_log=False)  
        
        # If no text is rotated by 180 degrees, use cls=False to get better performance.
        # 關閉 angle classifier 的辨識，提高效能
        result = ocr.ocr(self.img, cls=False)  
        
        return result[0]
            
    
    def filter_text(self, result):
        
        def sub_eng(text):
            # 移除英文字
            return re.sub(u'[A-Za-z]', '', text)
        
        info = {}
        sub_skill_idx = 1
        for _, line in enumerate(result):
            text = line[1][0].strip()
            text = text.upper()
            if sub_eng(text) in pokemons_list:
                info['pokemon'] = sub_eng(text)
            elif text in main_skills_list or text.replace('瘋', '癒') in main_skills_list or text.replace('癥', '癒') in main_skills_list:
                info['main_skill'] = text.replace('瘋', '癒').replace('癥', '癒')
            elif text in natures_list or text.replace('青', '害') in natures_list:
                info['nature'] = text.replace('青', '害')
            elif text in sub_skills_list or text.replace('盜', '持') in sub_skills_list or text.replace('複', '復') in sub_skills_list:
                info[f'sub_skill_{sub_skill_idx}'] = text.replace('盜', '持').replace('複', '復')
                sub_skill_idx += 1
            elif f'持有{text}' in sub_skills_list or f"持有{text.replace('盜', '持')}" in sub_skills_list:
                info[f'sub_skill_{sub_skill_idx}'] = f'持有{text}'
                sub_skill_idx += 1 
            else:
                pass

        return info
    
    def run(_self):
        result = _self.extract_text_from_img()
        info = _self.filter_text(result)
        print(f"{datetime.now()}")
        print(f"{info}")
        print("=========")
        return info
