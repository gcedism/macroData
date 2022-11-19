import json
import pandas as pd

import numpy as np
from numpy import log

from _data.database import database

sec = json.load(open('_data/data_specs.json'))
selection = ['us_cpi', 'us_cpi_core', 'us_cpi_food']
sel_sec = {x: sec[x] for x in selection}
db = database(sel_sec, 'm').data

us_cpi_MoM = db.apply(lambda x: log(x), axis=1).diff(periods=1).dropna()

sel_sec = {x: sec[x] for x in sec if sec[x]['asset_class'] == 'Commodities'}

db = database(sel_sec, 'm').data
db = db.loc[:, ~db.iloc[94].isnull()]

comm_MoM = db.apply(lambda x: log(x), axis=1).diff(periods=1).dropna()

comm_MoM3M = db.rolling(window=3).mean().apply(
  lambda x: log(x), axis=1).diff(periods=1).dropna()

# MoM :
for i in range(4):
  print(f'\n////////---SHIFT {i}---/////////////////\n')
  print(f'************ CPI MOM **********')
  print(
    pd.DataFrame([(col,
                   np.corrcoef(us_cpi_MoM.loc[comm_MoM.index[i:], 'us_cpi'],
                               comm_MoM.loc[:, col].shift(i).dropna())[0, 1])
                  for col in comm_MoM],
                 columns=['col', 'correl']).sort_values('correl',
                                                        ascending=False))

  print(f'************ CPI MOM3M **********')
  print(
    pd.DataFrame([(col,
                   np.corrcoef(us_cpi_MoM.loc[comm_MoM3M.index[i:], 'us_cpi'],
                               comm_MoM3M.loc[:, col].shift(i).dropna())[0, 1])
                  for col in comm_MoM3M],
                 columns=['col', 'correl']).sort_values('correl',
                                                        ascending=False))
  print(f'************ CPI CORE MOM **********')
  print(
    pd.DataFrame(
      [(col,
        np.corrcoef(us_cpi_MoM.loc[comm_MoM.index[i:], 'us_cpi_core'],
                    comm_MoM.loc[:, col].shift(i).dropna())[0, 1])
       for col in comm_MoM],
      columns=['col', 'correl']).sort_values('correl', ascending=False))

  print(f'************ CPI_CORE MOM3M **********')
  print(
    pd.DataFrame(
      [(col,
        np.corrcoef(us_cpi_MoM.loc[comm_MoM3M.index[i:], 'us_cpi_core'],
                    comm_MoM3M.loc[:, col].shift(i).dropna())[0, 1])
       for col in comm_MoM3M],
      columns=['col', 'correl']).sort_values('correl', ascending=False))

  print(f'************ CPI FOOD MOM **********')
  print(
    pd.DataFrame(
      [(col,
        np.corrcoef(us_cpi_MoM.loc[comm_MoM.index[i:], 'us_cpi_food'],
                    comm_MoM.loc[:, col].shift(i).dropna())[0, 1])
       for col in comm_MoM],
      columns=['col', 'correl']).sort_values('correl', ascending=False))

  print(f'************ CPI_FOOD MOM3M **********')
  print(
    pd.DataFrame(
      [(col,
        np.corrcoef(us_cpi_MoM.loc[comm_MoM3M.index[i:], 'us_cpi_food'],
                    comm_MoM3M.loc[:, col].shift(i).dropna())[0, 1])
       for col in comm_MoM3M],
      columns=['col', 'correl']).sort_values('correl', ascending=False))

# com_selection = ['ALI=F', 'CC=F', 'KC=F', 'SB=F', 'OJ=F', 'CT=F', 'GF=F', 'HE=F', 'LE=F', 'DC=F', 'BZ=F', 'CL=F', 'RB=F', 'HO=F', 'NG=F', 'ZW=F', 'ZR=F', 'ZC=F', 'ZM=F', 'ZL=F', 'ZS=F']
