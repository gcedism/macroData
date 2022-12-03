#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import io
import pandas as pd
from datetime import date 

from .utils import ticker_map, quarterDate
from .utils_private import API_KEYS

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
                Frequency of the data, available values are : Q
        '''
        
        self._freq = freq
        self._start_dt = start_dt
        self._end_dt = end_dt
        self._start_year = start_dt.year
        self._end_year = end_dt.year
        self._data = self._get_bea(tickers)
        
    def _get_bea(self, tickers:list[str]) -> pd.DataFrame:
        print('Retrieving data from BEA - Bureau of Economic Analyses...')
        p = {
            'UserID': API_KEYS['BEA_API_KEY'],
            'method': 'GetData',
            'Frequency': 'Q',
            'Year': [str(x) for x in range(self._start_year, self._end_year)],
            'ResultFormat': 'json'
        }
        url = 'https://apps.bea.gov/api/data/'

        _data = []
        for tic in tickers:
            p['DataSetName'] = ticker_map[tic]['DataSetName']
            p['TableName'] = ticker_map[tic]['TableName']
            s = requests.get(url, p).text
            _df = pd.DataFrame(json.loads(s)['BEAAPI']['Results']['Data'])
            _df.set_index('TimePeriod', inplace=True)
            ser = _df[_df['LineNumber'] == '1']['DataValue']

            ser.index = ser.index.map(quarterDate)
            ser.name = tic
            _data.append(pd.DataFrame(ser))

        return _data[0].join(_data[1:], how='outer').sort_index()

    @property
    def data(self):
        return self._data