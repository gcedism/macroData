import yfinance as yf
import numpy as np

import datetime
from datetime import datetime as dt
from datetime import timedelta as td

import pandas as pd
from pandas.tseries.offsets import CDay

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from .dateFunctions import first_day

endog = pd.read_csv('_data/manual.csv', index_col = 0, encoding = 'UTF-8')
endog.index = endog.index.map(lambda x : dt.strptime(x, '%d.%m.%y').date())

params = {
    'FRED_API_KEY' : '670447b1b80828dd0122187f1d2661ae',
    'BEA_API_KEY' : '7B01FC1C-8919-4AC2-BD04-C34BA76ABCD8',
    'BLS_API_KEY' : '8494059d2e194e3d92592613a48ce565',
    'NASDAQ_API_KEY' : 'YzwzXVQ-yw77QqS8dwEA'
}

def Adjust_for_Dividends(ticker: str, prices) :
    _start_date = prices.index[0]
    
    tic = yf.Ticker(ticker)
    dvd = tic.actions['Dividends']
    dvd.index = [first_day(x) for x in dvd.index]
    dvd.index.name = 'date'
    dvd = dvd.groupby('date').sum()
    dvd = dvd[_start_date:].cumsum() 

    a = []
    i = 0
    for i, index in enumerate(prices.index) :
        try :
            a.append(dvd[index])
        except :
            try :
                a.append(a[-1])
            except : 
                a.append(0)
            
    return pd.Series(a, index = prices.index) + prices
    
def linInterp(value, origin, destiny) :
    table = pd.DataFrame(destiny, index = origin)
    if type(origin[0]) == datetime.date :
        table_interp = table.iloc[abs((table.index-value).days.values).argsort()[:2]]
        res = (value - table_interp.index[0]).days / (table_interp.index[1] - table_interp.index[0]).days * (table_interp.iloc[1] - table_interp.iloc[0]) + table_interp.iloc[0]
    
    return res

def plot_class_regions_for_classifier(clf, X, y, X_test=None, y_test=None, title=None, target_names = None, plot_decision_regions = True):

    numClasses = np.amax(y) + 1
    color_list_light = ['#FFFFAA', '#EFEFEF', '#AAFFAA', '#AAAAFF']
    color_list_bold = ['#EEEE00', '#000000', '#00CC00', '#0000CC']
    cmap_light = ListedColormap(color_list_light[0:numClasses])
    cmap_bold  = ListedColormap(color_list_bold[0:numClasses])

    h = 0.03
    k = 0.5
    x_plot_adjust = 0.1
    y_plot_adjust = 0.1
    plot_symbol_size = 50

    x_min = X[:, 0].min()
    x_max = X[:, 0].max()
    y_min = X[:, 1].min()
    y_max = X[:, 1].max()
    x2, y2 = np.meshgrid(np.arange(x_min-k, x_max+k, h), np.arange(y_min-k, y_max+k, h))

    P = clf.predict(np.c_[x2.ravel(), y2.ravel()])
    P = P.reshape(x2.shape)
    plt.figure(figsize = (12,8))
    if plot_decision_regions:
        plt.contourf(x2, y2, P, cmap=cmap_light, alpha = 0.8)

    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, s=plot_symbol_size, edgecolor = 'black')
    plt.xlim(x_min - x_plot_adjust, x_max + x_plot_adjust)
    plt.ylim(y_min - y_plot_adjust, y_max + y_plot_adjust)

    if (X_test is not None):
        plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cmap_bold, s=plot_symbol_size, marker='^', edgecolor = 'black')
        train_score = clf.score(X, y)
        test_score  = clf.score(X_test, y_test)
        title = title + "\nTrain score = {:.2f}, Test score = {:.2f}".format(train_score, test_score)

    if (target_names is not None):
        legend_handles = []
        for i in range(0, len(target_names)):
            patch = mpatches.Patch(color=color_list_bold[i], label=target_names[i])
            legend_handles.append(patch)
        plt.legend(loc=0, handles=legend_handles)

    if (title is not None):
        plt.title(title)
    plt.show()
    
