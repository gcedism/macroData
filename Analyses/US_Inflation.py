import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from numpy import log

import macrodata as md

sec = json.load(open('macrodata/data_specs.json'))

sel_sec = {
  x: sec[x]
  for x in sec
  if (sec[x]['region'] == 'US') and (sec[x]['asset_class'] == 'Inflation')
}

m_db = md.database(sel_sec, 'm').data

us_cpi = m_db[[
  'us_cpi', 'us_cpi_core', 'us_cpi_food', 'us_cpi_medicare', 'us_cpi_shelter',
  'us_cpi_rent_sa'
]].astype(float)
us_cpi_high = m_db[['us_cpi_energy', 'us_cpi_gasoline']].astype(float)

us_cpi_YoY = us_cpi.dropna().apply(lambda x: log(x),
                                   axis=1).diff(periods=12).dropna()
us_cpi_high_YoY = us_cpi_high.apply(lambda x: log(x),
                                    axis=1).diff(periods=12).dropna()
us_cpi_MoM = us_cpi.dropna().apply(lambda x: log(x),
                                   axis=1).diff(periods=1).dropna()
us_cpi_high_MoM = us_cpi_high.apply(lambda x: log(x),
                                    axis=1).diff(periods=1).dropna()

f, ax = plt.subplots(2, 2, figsize=(18, 12))
f.suptitle('US Inflation', fontsize=16, fontweight='bold')

(us_cpi_YoY.iloc[-36:] * 100).plot(ax=ax[0, 0], lw=3, title='Ex-Energy, YoY')
(us_cpi_high_YoY.iloc[-36:] * 100).plot(ax=ax[0, 1], lw=3, title='Energy, YoY')
(us_cpi_MoM.iloc[-36:] * 100).plot(ax=ax[1, 0], lw=3, title='Ex-Energy, MoM')
(us_cpi_high_MoM.iloc[-36:] * 100).plot(ax=ax[1, 1], lw=3, title='Energy, MoM')

for a in ax.reshape(1, 4)[0]:
  a.spines['top'].set_visible(False)
  a.spines['right'].set_visible(False)
  a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
  a.grid(alpha=0.5, ls='--')

void = plt.xticks(fontsize=12)
void = plt.yticks(fontsize=12)

void = ax[1, 0].text(0,
                     -0.1,
                     'Source : US BLS - Bureau of Labour Statistics',
                     fontstyle='italic',
                     transform=ax[1, 0].transAxes)

plt.savefig('Analyses/figs/USInflation.jpg')
