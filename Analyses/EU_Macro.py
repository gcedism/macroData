import json
import pandas as pd
import matplotlib.pyplot as plt
from _data.database import database

sec = json.load(open('_data/data_specs.json'))

sel_sec = {
  x: sec[x]
  for x in sec
  if (sec[x]['sub_asset_class'] == 'Sentiment') and (sec[x]['region'] == 'EU')
}

m_db = database(sel_sec, 'm').data

f, ax = plt.subplots(figsize=(10, 12))
f.suptitle('EU Sentiment', fontsize=16, fontweight='bold')

m_db.dropna().plot(ax=ax)

ax.spines[['right', 'top']].set_visible(False)
ax.grid(alpha=0.5, ls='--')

void = plt.xticks(fontsize=12)
void = plt.yticks(fontsize=12)

void = ax.text(0,
               -0.1,
               'Source : Eurostat',
               fontstyle='italic',
               transform=ax.transAxes)

plt.show()
# plt.savefig('_data/figs/EUSentiment.jpg')
