import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from numpy import log
from macrodata import listHistory, countryAssetList

def get_us_inflation_chart(start_dt, end_dt, session, History) :
    items = ['us_cpi', 'us_cpi_core']

    history = listHistory(items, start_dt, end_dt, session, History)
    history = history.apply(log).diff(12).dropna()
        
    f, ax = plt.subplots()
    f.suptitle('US Inflation', fontsize = 12, fontweight = 'bold')

    (history*100).plot(ax=ax)
        
    ax.spines[['top', 'right']].set_visible(False)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals = 1))
        
    ax.grid(alpha = 0.5, ls = '--')
    ax.legend(loc = 'lower left')
    
    void = plt.xticks(fontsize=12)
    void = plt.yticks(fontsize=12)

    void = ax.text(0, -0.1, 'Source : ',
              fontstyle = 'italic',
              transform = ax.transAxes)

    return f
    
def get_us_inflation_breakdown(start_dt, end_dt, session, History, Data) :
    items = countryAssetList(['US'], ['Inflation'], session, Data)
    db = listHistory(items, start_dt, end_dt, session, History)
    
    us_cpi = db[['us_cpi', 'us_cpi_core', 'us_cpi_food',
             'us_cpi_medicare', 'us_cpi_shelter',
             'us_cpi_rent_sa']].astype(float)
    us_cpi_high = db[['us_cpi_energy', 'us_cpi_gasoline']].astype(float)
    
    us_cpi_YoY = us_cpi.dropna().apply(lambda x : log(x), axis = 1).diff(periods = 12).dropna()
    us_cpi_high_YoY = us_cpi_high.apply(lambda x : log(x), axis = 1).diff(periods = 12).dropna()
    us_cpi_MoM = us_cpi.dropna().apply(lambda x : log(x), axis = 1).diff(periods = 1).dropna()
    us_cpi_high_MoM = us_cpi_high.apply(lambda x : log(x), axis = 1).diff(periods = 1).dropna()
    
    f, ax = plt.subplots(2,2, figsize=(18,12))
    f.suptitle('US Inflation', fontsize = 12, fontweight = 'bold')

    (us_cpi_YoY.iloc[-36:] * 100).plot(ax = ax[0, 0], lw = 3, title = 'Ex-Energy, YoY')
    (us_cpi_high_YoY.iloc[-36:] * 100).plot(ax = ax[0, 1], lw = 3, title = 'Energy, YoY')
    (us_cpi_MoM.iloc[-36:] * 100).plot(ax = ax[1, 0], lw = 3, title = 'Ex-Energy, MoM')
    (us_cpi_high_MoM.iloc[-36:] * 100).plot(ax = ax[1, 1], lw = 3, title = 'Energy, MoM')

    for a in ax.reshape(1,4)[0] :
        a.spines[['right', 'top']].set_visible(False)
        a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals = 1))
        a.grid(alpha = 0.5, ls = '--')

    void = plt.xticks(fontsize=12)
    void = plt.yticks(fontsize=12)

    void = ax[1, 0].text(0, -0.1, 'Source : US BLS - Bureau of Labour Statistics',
              fontstyle = 'italic',
              transform = ax[1, 0].transAxes)
    
    return(f)

def get_us_inflation_expectations(start_dt, end_dt, session, History) :
    items = ['us_5v5_inflation', 'us_5y_be_inflation', 'us_10y_rate']
    db = listHistory(items, start_dt, end_dt, session, History)
    
    f, ax = plt.subplots(figsize=(10,6))
    f.suptitle('US Inflation expectations\nYoY', fontsize = 16, fontweight = 'bold')

    db.plot(ax = ax, lw = 3)

    ax.spines[['right', 'top']].set_visible(False)
    ax.grid(alpha = 0.5, ls = '--')
    ax.legend(loc = 'lower left')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals = 1))

    void = plt.xticks(fontsize=12)
    void = plt.yticks(fontsize=12)

    void = ax.text(0, -0.1, 'Source : FRED, yahoo Finance',
              fontstyle = 'italic',
              fontsize = 8,
              transform = ax.transAxes)
    
    return(f)
