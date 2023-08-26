import re
import warnings; warnings.filterwarnings('ignore')
import pandas as pd
import pytesseract
import streamlit as st


class TransformImage:
    def __init__(self, img):
        self.img = img
        self.config = r'--psm 12 --dpi 300' # 6, 11 and 12 are more accurate
        self.output_type = 'dict'
        self.lang = 'chi_tra'
    
    def img_to_dataframe(self):
        data = pytesseract.image_to_data(self.img, output_type=self.output_type, lang=self.lang, config=self.config)
        df = pd.DataFrame(data)
        return df
    
    def pre_filter(self, df):
        mask = (
            (df['level'] == 5) & 
            (df['conf'] > 0)
        )

        df_text = df[mask]
        df_text = df_text.drop(['page_num', 'par_num', 'word_num'], axis=1)
        return df_text

    def create_full_text(self, df_text):
        df_full_text = df_text[['block_num', 'line_num', 'text']].copy()
        df_full_text = df_full_text.groupby(['block_num', 'line_num'], as_index=False).transform(lambda x: ''.join(x))
        df_text['full_text'] = df_full_text['text']
        return df_text

    def post_filter(self, df_text):

        def find_zh(x):
            if re.search(u'[\u4e00-\u9fff]', x):
                return True
            return False
            
        df_text = df_text.drop_duplicates(['block_num', 'line_num', 'full_text'])
        df_text = df_text.drop(['level', 'block_num', 'line_num'], axis=1)
        mask = (
            (df_text['full_text'].str.len() > 3)
            & (df_text['full_text'].str.len() < 10)
            & (df_text['text'] != '一')
            & (df_text['left'] > 190)
            & (df_text['top'] > 200)
        )
        df_text = df_text[mask]
        df_text = df_text.drop('text', axis=1)
        df_text = df_text[df_text['full_text'].apply(find_zh)]
        return df_text
    
    @st.cache_data
    def run(_self):
        df = _self.img_to_dataframe()
        df_text = _self.pre_filter(df)
        df_text = _self.create_full_text(df_text)
        df_text = _self.post_filter(df_text)
        return df_text