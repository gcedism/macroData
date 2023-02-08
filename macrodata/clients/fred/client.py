#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd
from datetime import date
from datetime import datetime as dt

from .utils import ticker_map
from .utils_private import API_KEYS

class Client :
    
    def __init__(self, tickers, start_dt:date, end_dt:date, freq:str) :
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
        self._data = self._get_fred(tickers)
        
    def _get_fred(self, tickers):
        print('Retrieving data from FRED - FED St Louis Economic Data...')
        # _tickers = [ticker_map[x]['code'] for x in tickers]
        p = {
            'api_key': API_KEYS['FRED_API_KEY'],
            'file_type': 'json',
            'observation_start': dt.strftime(self._start_dt, '%Y-%m-%d'),
            'observation_end': dt.strftime(self._end_dt, '%Y-%m-%d'),
            'frequency': 'm',
            'aggregation_method': 'eop'
        }
        url = 'https://api.stlouisfed.org/fred/series/observations'

        _data = {}
        for tic in tickers:
            p['series_id'] = ticker_map[tic]['code']
            f_data = json.loads(requests.get(url, p).text)
            f_df = pd.DataFrame(f_data['observations'])[['date', 'value']]
            f_df.index = f_df['date']
            f_Series = f_df['value']
            f_Series = f_Series.replace(['.'], 0).astype(float)

            _data[tic] = f_Series

        _data = pd.DataFrame.from_dict(_data)
        _start = dt.strptime(_data.index[0], '%Y-%m-%d').date()
        _data.index = pd.date_range(_start, periods=_data.shape[0], freq=self._freq)
        _data.index = _data.index.map(lambda x: x.date())
        
        return _data

    @property
    def data(self):
        return self._data