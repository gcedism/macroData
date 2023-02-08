#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yfinance as yf
import numpy as np
import datetime
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date
from pathlib import Path

import pandas as pd
from pandas.tseries.offsets import CDay

FOLDER = str(Path(__file__).parent.parent)

endog = pd.read_csv(FOLDER + '/_data/manual.csv', index_col=0, encoding='UTF-8')
endog.index = endog.index.map(lambda x: dt.strptime(x, '%d.%m.%y').date())

def EoXMonth(dat:date, x:int, calendar:bool=True) -> date :
    """ 
    Function that returns the last day of x months ahead
    :parameters:
        date : date
            Original Date to be transformed
        x : int
            Number of months ahead (0 if same month)
        calendar : bool
            Whether to return the last business day or last calendar day
    """

    _m = (dat.month + x + 1) % 12
    if _m == 0: _m = 12
    _y = dat.year + int((dat.month + x) / 12)
        
    _date = date(_y, _m, 1)
    if calendar : 
        return (_date - CDay(1)).date()
    else :
        return (_date - td(days=1))
    
def nMonths(date1:date, date2:date) -> int :
    if date1 > date2 :
        # Raise an error
        pass
    else :
        n = (date2.month - date1.month) + (n.year - n.year) * 12
    
    return int(n)
        
def isEndOfMonth(_date:date) -> bool:
    next_date = _date + CDay(1)
    if next_date.month != _date.month :
        return True
    else :
        return False
    
yahoo_mapping = {
    'corp': 'CORP',
    'LQD': 'LQD',
    'HYG': 'HYG',
    'GOVT': 'GOVT',
    'IGOV': 'IGOV',
    'EMB': 'EMB',
    'CEMB': 'CEMB',
    'EMLC': 'EMLC',
    'DX-Y.NYB': 'DX-Y.NYB',
    'SPY': 'SPY',
    'IYM': 'IYM',
    'IXP': 'IXP',
    'IYC': 'IYC',
    'IYK': 'IYK',
    'IYE': 'IYE',
    'IYF': 'IYF',
    'IYH': 'IYH',
    'IYJ': 'IYJ',
    'IYR': 'IYR',
    'IDU': 'IDU',
    'JXI': 'JXI',
    'BBEU': 'BBEU',
    'EZU': 'EZU',
    'VGK': 'VGK',
    'EEM': 'EEM',
    'SPTI': 'SPTI',
    'GSG': 'GSG',
    '^GSPC': '^GSPC',
    'us_3m_rate': '^IRX',
    'us_5y_rate': '^FVX',
    'us_10y_rate': '^TNX',
    'us_30y_rate': '^TYX',
    '^MOVE': '^MOVE',
    'dxy' : 'DX-Y.NYB',
    'EURUSD=X': 'EURUSD=X',
    'GBPUSD=X': 'GBPUSD=X',
    'CAD=X': 'CAD=X',
    'AUDUSD=X': 'AUDUSD=X',
    'NZDUSD=X': 'NZDUSD=X',
    'JPY=X': 'JPY=X',
    'SEK=X': 'SEK=X',
    'NOK=X': 'NOK=X',
    'PLN=X': 'PLN=X',
    'HUF=X': 'HUF=X',
    'CZK=X': 'CZK=X',
    'MXN=X': 'MXN=X',
    'BRL=X': 'BRL=X',
    'ZAR=X': 'ZAR=X',
    'TRY=X': 'TRY=X',
    'gold_fut': 'GC=F',
    'silver_fut': 'SI=F',
    'copper_fut': 'HG=F',
    'platinum_fut': 'PL=F',
    'palladiium_fut': 'PA=F',
    'aluminum_fut': 'ALI=F',
    'coccoa_fut': 'CC=F',
    'coffee_fut': 'KC=F',
    'sugar_fut': 'SB=F',
    'orangeJ_fut': 'OJ=F',
    'cotton_fut': 'CT=F',
    'feeder_cattle_fut': 'GF=F',
    'lean_hogs_fut': 'HE=F',
    'live_cattle_fut': 'LE=F',
    'milk_classIII_fut': 'DC=F',
    'brent_oil_fut': 'BZ=F',
    'wti_oil_fut': 'CL=F',
    'gasoline_oil_fut': 'RB=F',
    'heating_oil_fut': 'HO=F',
    'natural_gas_fut': 'NG=F',
    'wheat_fut': 'ZW=F',
    'rice_fut': 'ZR=F',
    'corn_fut': 'ZC=F',
    'soybean_meal_fut': 'ZM=F',
    'soybean_oil_fut': 'ZL=F',
    'soybean_fut': 'ZS=F'
}

philly_mapping = {
    'us_cur_activity' : 'GAC',
    'us_cur_new_orders' : 'NOC',
    'us_cur_shipments' : 'SHC',
    'us_unfilled_orders' : 'UOC',
    'us_cur_delivery_time' : 'DTC',
    'us_cur_inventories' : 'IVC',
    'us_cur_prices_paid' : 'PPC',
    'us_cur_prices_received' : 'PRC',
    'us_cur_employment' : 'NEC',
    'us_cur_avg_workweek' : 'AWC',
    'us_fut_activity' : 'GAF',
    'us_fut_new_orders' : 'NOF',
    'us_fut_shipments' : 'SHF',
    'us_fut_unfilled_orders' : 'UOF',
    'us_fut_delivery_time' : 'DTF',
    'us_fut_inventories' : 'IVF',
    'us_fut_prices_paid' : 'PPF',
    'us_fut_prices_received' : 'PRF',
    'us_fut_employment' : 'NEF',
    'us_fut_avg_workweek' : 'AWF',
    'us_fut_capex' : 'CEF'
}