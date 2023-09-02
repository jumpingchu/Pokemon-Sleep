# Pokemon-Sleep Helper

![pokemon_sleep](img/pokemon_sleep.png)

## Try it (Streamlit Cloud)
https://pokemon-sleep.streamlit.app/

## 目前功能
- 利用自己現有的食材篩選能做出哪些食譜料理
- 寶可夢的樹果、食材、來源島嶼

## 使用技術
- Streamlit
- Python:
  - Data process: `numpy`, `pandas`
  - Crawler: `requests`, `BeautifulSoup`, `fake_useragent`
- Scikit-learn (`DecisionTreeRegressor`, `LinearRegression`)
- SHAP (Feature explanation by visualization)
- CSS
- Text Detection (OCR 光學字元辨識): `OpenCV`, `PyTesseract`, `EasyOCR`, `PaddleOCR`

## 可能新增功能優先度
- [x] 寶可夢的產出食材頁面 (Multipage apps)
- [x] 食材圖片 (`st.column_config.ImageColumn`)
- [x] 機器學習預測樹果提供的能量（目前特徵: 寶可夢等級, 寶可夢SP）
- [x] 自動文字辨識：寶可夢截圖資訊
- [ ] 藉由圖片辨識的文字來計算寶可夢能力
- [ ] 查詢缺乏的食材由哪隻寶可夢產出 (`st.column_config.LinkColumn`)
- [ ] 所選食材在各食譜的完成度 (`st.column_config.ProgressColumn`)
- [ ] 完成度由高到低排序

## 圖片辨識文字

- [PyTesseract](https://github.com/madmaze/pytesseract) 辨識速度快但較不準確
  - 部署需要 `packages.txt` 裡面放
    -  `tesseract-ocr`
    -  `tesseract-ocr-chi-tra`
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) 辨識速度慢但感覺較準確
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 辨識速度快又準確（目前採用此套件）
### 輸出結果範例

- PaddleOCR

![paddleOCR result](img/result_paddleOCR/result.jpg)
![paddleOCR result1](img/result_paddleOCR/result1.jpg)

- EasyOCR

![out_box](img/out_box.png)

## 資料來源

- [《野兔小幫手》v1.3.0 (Google Sheet)](https://docs.google.com/spreadsheets/d/18aAHjg762T29F74yo8axDVFO09swCa7nUp_eTZ51ZAc/edit#gid=439534137)
- [寶可夢全食譜彙整一覽表](https://pinogamer.com/16427)
- [寶可夢Sleep潛力計算機v3.32](https://forum.gamer.com.tw/C.php?bsn=36685&snA=913&tnum=185)


## Note
- Streamlit Dataframe 同一個欄位的資料不能混合圖片和文字
- 使用 SHAP 要注意其他套件的版本（參考 `requirements.txt` 檔案）

