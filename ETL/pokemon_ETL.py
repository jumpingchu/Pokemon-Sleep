# from data_filepath import POKEMON_SHEET, POKEMON_TRANSFORMED
# from util import load_gsheet_data

# df = load_gsheet_data(POKEMON_SHEET)
# df = df.replace('無', '')
# df = df.fillna('')

# df['all_ingredients'] = (
#     df['食材'] + \
#     df['食材.1'] + \
#     df['食材.2']
# )
# df['fruit'] = df['樹果'] # 增加英文欄位做後續篩選用
# df['來源島嶼'] = (
#     df['萌綠之島'] + ' / ' + \
#     df['天青沙灘'] + ' / ' + \
#     df['灰褐洞窟'] + ' / ' + \
#     df['白花雪原'] + ' / ' + \
#     df['脂紅火山'] + ' / ' + \
#     df['寶藍湖畔']
# )
# df['來源島嶼'] = df['來源島嶼'].apply(lambda x: x.strip(' / ')) # 移除字尾多餘的斜線

# df['all_sleep_type'] = (
#     df['睡眠類型'] + ' / ' + \
#     df['睡眠類型.1'] + ' / ' + \
#     df['睡眠類型.2'] + ' / ' + \
#     df['睡眠類型.3'] + ' / ' + \
#     df['睡眠類型.4'] + ' / ' + \
#     df['睡眠類型.5']
# )
# df['all_sleep_type'] = df['all_sleep_type'].apply(lambda x: ' / '.join(list(set(x.split(' / ')))))
# df['all_sleep_type'] = df['all_sleep_type'].apply(lambda x: str(x).strip(' / ')) # 移除字尾多餘的斜線

# df = df.rename(
#     columns={
#         '食材': '基本食材',
#         '食材.1': 'Lv30食材',
#         '食材.2': 'Lv60食材',
#         'all_sleep_type': '睡眠類型'
#     }
# )
# df = df[[
#     '名稱',
#     # '進化條件',
#     # '糖果數量',
#     '樹果',
#     'fruit',
#     '基本食材',
#     'Lv30食材',
#     'Lv60食材',
#     'all_ingredients',
#     'all_sleep_type',
#     '來源島嶼',
#     # '萌綠之島',
#     '睡眠類型',
#     # '天青沙灘',
#     # '睡眠類型.1',
#     # '灰褐洞窟',
#     # '睡眠類型.2',
#     # '白花雪原',
#     # '睡眠類型.3',
#     # '脂紅火山',
#     # '睡眠類型.4',
#     # '寶藍湖畔',
#     # '睡眠類型.5',
# ]]
# df.to_csv(POKEMON_TRANSFORMED)
