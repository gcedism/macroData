#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd
from datetime import date
from datetime import datetime as dt

from .utils import ticker_map

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
        self._start = date.strftime(start_dt, '%d/%m/%Y')
        self._end_dt = end_dt
        self._end = date.strftime(end_dt, '%d/%m/%Y')
        self._data = self._get_fed(tickers)
        
    def _get_fed(self, tickers:list[str]) -> pd.DataFrame:
        print('Retrieving data from FED...')
        url = 'https://www.federalreserve.gov/datadownload/Output.aspx'
        p = {
            'rel': 'G17',
            'series': '5d88c03b0036f0334d78f6bafefc5101',
            'lastobs': [],
            'from': self._start,
            'to': self._end,
            'filetype': 'csv',
            'label': 'include',
            'layout': 'seriescolumn'
        }

        _data = []
        for tic in tickers:
            p_csv = {'index_col': 0, 'skiprows': 5, 'usecols': ticker_map[tic]['usecols']}
            r = requests.get(url, p)
            open('temp.xls', 'wb').write(r.content)
            _df = pd.read_csv('temp.xls', **p_csv)
            _df.columns = ticker_map[tic]['colNames']
            _start = date(int(_df.index[0][:4]), int(_df.index[0][-2:]), 1)
            _df.index = pd.date_range(_start, periods=_df.shape[0], freq=self._freq)
            _data.append(_df)

        return _data[0]

    @property
    def data(self):
        return self._data