import json
import pandas as pd

import numpy as np
from numpy import log
import statsmodels.api as sm

from _data.database import database

sec = json.load(open('_data/data_specs.json'))
selection = ['us_cpi', 'us_cpi_core', 'us_cpi_food']
sel_sec = {x: sec[x] for x in selection}
db = database(sel_sec, 'm').data

us_cpi_MoM = db.apply(lambda x: log(x), axis=1).diff(periods=1).dropna()

selection = ['HO=F', 'CL=F', 'RB=F', 'HG=F', 'PL=F', 'ZM=F', 'ZC=F']
sel_sec = {x: sec[x] for x in selection}

db = database(sel_sec, 'm').data

comm_MoM = db.apply(lambda x: log(x), axis=1).diff(periods=1).dropna()

# comm_MoM3M = db.rolling(window=3).mean().apply(
#   lambda x: log(x), axis=1).diff(periods=1).dropna()
# CORRELATIONS
# i = 1
# print(
#   pd.DataFrame([(col,
#                  np.corrcoef(us_cpi_MoM.loc[comm_MoM.index[i:], 'us_cpi'],
#                              comm_MoM.loc[:, col].shift(i).dropna())[0, 1])
#                 for col in comm_MoM],
#                columns=['col', 'correl']).sort_values('correl',
#                                                       ascending=False))

# MODEL
i = 1
y = us_cpi_MoM.loc[comm_MoM.index[i:], 'us_cpi']
X = comm_MoM.shift(i).dropna()
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

print(model.predict([1] + comm_MoM.iloc[-1].to_list()))
