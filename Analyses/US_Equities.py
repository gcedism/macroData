import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from datetime import datetime as dt

from numpy import log

from _data.database import database

sec = json.load(open('_data/data_specs.json'))
selection = ['SPY', 'us_10y_real_rate']
sel_sec = {
  x: sec[x]
  for x in selection
}

m_db = database(sel_sec, 'm').data
start_dt = dt(2012, 1, 31).date()


f, ax = plt.subplots(figsize = (10, 6))
ax.plot(m_db.loc[start_dt:].index, m_db['SPY'].loc[start_dt:], lw = 3, color = 'red', label = 'S&P')
ax2 = ax.twinx()
ax2.plot(m_db.loc[start_dt:].index, m_db['us_10y_real_rate'].loc[start_dt:], lw = 3, color = 'blue', label = 'US 10Y Rate, inverted, RHS')
ax2.invert_yaxis()

ax.spines[['right', 'top']].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.grid(alpha=0.5, ls='--')

void = plt.xticks(fontsize=12)
void = plt.yticks(fontsize=12)

void = ax.text(0,
               -0.1,
               'Source : Yahoo, St Louis FED',
               fontstyle='italic',
               transform=ax.transAxes)

plt.show()

