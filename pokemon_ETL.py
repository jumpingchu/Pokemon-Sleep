import pandas as pd
from data.data_filepath import POKEMON_SHEET
from util import load_gsheet_data
df = load_gsheet_data(POKEMON_SHEET)
df