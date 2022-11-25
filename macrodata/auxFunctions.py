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

FOLDER = __file__[:-len('auxFunctions.py')]

endog = pd.read_csv(FOLDER + 'manual.csv', index_col=0, encoding='UTF-8')
endog.index = endog.index.map(lambda x: dt.strptime(x, '%d.%m.%y').date())


def Adjust_for_Dividends(ticker: str, prices):
  _start_date = prices.index[0]

  tic = yf.Ticker(ticker)
  dvd = tic.actions['Dividends']
  dvd.index = [first_day(x) for x in dvd.index]
  dvd.index.name = 'date'
  dvd = dvd.groupby('date').sum()
  dvd = dvd[_start_date:].cumsum()

  a = []
  i = 0
  for i, index in enumerate(prices.index):
    try:
      a.append(dvd[index])
    except:
      try:
        a.append(a[-1])
      except:
        a.append(0)

  return pd.Series(a, index=prices.index) + prices


def linInterp(value, origin, destiny):
  table = pd.DataFrame(destiny, index=origin)
  if type(origin[0]) == datetime.date:
    table_interp = table.iloc[abs(
      (table.index - value).days.values).argsort()[:2]]
    res = (value - table_interp.index[0]).days / (
      table_interp.index[1] - table_interp.index[0]).days * (
        table_interp.iloc[1] - table_interp.iloc[0]) + table_interp.iloc[0]

  return res

