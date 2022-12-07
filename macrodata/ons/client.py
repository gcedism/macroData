#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import zeep
import warnings
import pandas as pd
from datetime import date
from datetime import datetime as dt

from .utils import ticker_map, EoXMonth

class Client :
    
    def __init__(self, tickers:list[str], start_dt:date, end_dt:date, freq:str) :
        '''
        Received an indicator and search for the parameters
        :Parameters:
            tickers : str, list
                Coded list of indicators from a list of available items
            start_dt : datetime.Date
                Start date to start extraction
            end_dt : datetime.Date
                End date to end extraction
            freq: str
                Frequency of the data, available values are : B, M, Q, A
        '''
        
        self._freq = freq
        self._start_dt = start_dt
        self._end_dt = end_dt
        self._data = self._get_ons(tickers)
        
    def _get_ons(self, tickers):
        print('Retrieving data from ONS - Office for National Statistics...')
        _data = []
        _temp = {}
        for tic in tickers:
            if ticker_map[tic]['dataGroup'] not in _temp.keys() :
                url = 'https://www.ons.gov.uk/file?' + ticker_map[tic]['url']
                _usecols = [0] + [ticker_map[t]['col'] 
                                  for t in ticker_map 
                                  if ticker_map[t]['dataGroup'] == ticker_map[tic]['dataGroup']]
                p = {
                    'sheet_name': ticker_map[tic]['sheet_name'],
                    'skiprows': ticker_map[tic]['skiprows'],
                    'index_col': 0,
                    'usecols': _usecols,
                    'engine': 'openpyxl'
                  }
                r = requests.get(url)
                open('temp.xls', 'wb').write(r.content)
                with warnings.catch_warnings(record=True):
                    warnings.simplefilter("always")
                    df = pd.read_excel('temp.xls', **p)
                
                colNames = [t for t in ticker_map 
                              if ticker_map[t]['dataGroup'] == ticker_map[tic]['dataGroup']]
                df.columns = colNames
            
                try:
                    firstRow = [x for x in range(df.shape[0]) if str(df.index[x]).lower() == '1993 jan'][0]
                except:
                    firstRow = 0
                lastRow = [x for x in range(df.shape[0]) if pd.isna(df.index[x])][0] if len([x for x in range(df.shape[0])
                   if pd.isna(df.index[x])]) > 0 else df.shape[0]
                df = df.iloc[firstRow:lastRow]
                df.index = [EoXMonth(dt.strptime(x, '%Y %b').date(), 0, False) for x in df.index]
                df.loc[df.index >= self._start_dt]
                _temp[ticker_map[tic]['dataGroup']] = df
                
            _data.append(pd.DataFrame(_temp[ticker_map[tic]['dataGroup']].loc[:, tic]))

        _df = _data[0].join(_data[1:], how='outer')

        return _df

    @property
    def data(self):
        return self._data