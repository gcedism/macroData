import yfinance as yf
import numpy as np

import datetime
from datetime import datetime as dt
from datetime import timedelta as td

import pandas as pd
from pandas.tseries.offsets import CDay

FOLDER = __file__[:-len('utils.py')]

endog = pd.read_csv(FOLDER + 'manual.csv', index_col=0, encoding='UTF-8')
endog.index = endog.index.map(lambda x: dt.strptime(x, '%d.%m.%y').date())

