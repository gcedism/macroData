#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import pandas as pd
from datetime import date as dt


from .utils import ticker_map
from .utils_private import API_KEYS

class Client :
    
    def __init__(self, tickers, start_dt:dt, end_dt:dt, freq:str) :
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
        
        self.freq = freq
        self.start = start_dt.year
        self.end = end_dt.year
        self._data = self._get_bls(tickers)
        
    def _get_bls(self, tickers):
        print('Retrieving data from BLS - Bureau of Labour Statistics...')
        _tickers = [ticker_map[x]['code'] for x in tickers]
        p = {
            "registrationkey": API_KEYS['BLS_API_KEY'],
            "seriesid": _tickers,
            "startyear": self.start,
            "endyear": self.end
        }
        url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
        h = {'Content-type': 'application/json'}
        
        _start = self.start
        _data = pd.DataFrame([])
        while self.end - _start > 0 :
            p['startyear'] = _start
            new_data = self._aux_blsData(url, p, h)
            _data = pd.concat((_data, new_data))
            _start += 20

        return _data
    
    def _aux_blsData(self, url, p, h):
        mapping = {ticker_map[x]['code']: x for x in ticker_map}
        s = requests.post(url, data=json.dumps(p), headers=h).text
        a = {x['seriesID']: x['data'] for x in json.loads(s)['Results']['series']}
        b = [pd.DataFrame(v, columns=['value']).rename(columns={'value': mapping[k]})
            .sort_index(ascending=False)
            .set_index(pd.Index(range(len(v)))) for k, v in a.items()
            ]
        _data = b[0].join(b[1:], how='outer')
        
        _start = dt(p['startyear'], 1, 1)
        _data.index = pd.date_range(_start, periods=_data.shape[0], freq=self.freq)
            
        return _data
    
    @property
    def data(self):
        return self._data