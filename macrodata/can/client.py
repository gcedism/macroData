#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import io
import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime as dt

from .utils import ticker_map

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
        self._data = self._get_can(tickers)
        
    def _get_can(self, ticker:list[str]) -> pd.DataFrame:
        print('Retrieving data from Canada Central Bank...')
        
        _temp = {}
        _data = []
        for tic in ticker :
            if 'canada' not in _temp.keys() :
                url = 'https://www.bankofcanada.ca/valet/observations/group/bond_yields_benchmark/csv'
                usecols = [0] + [ticker_map[t]['col'] for t in ticker_map]
                p_csv = {
                    'skiprows': 23,
                    'usecols': usecols,
                }                
                _s = requests.get(url).content
                _aux = pd.read_csv(io.StringIO(_s.decode('utf-8')), **p_csv)
                if self._freq == 'B' :
                    _aux.loc[:, 'date'] = _aux.loc[:, 'date'].map(lambda x: dt.strptime(x, '%Y-%m-%d').date())
                    _aux.set_index('date', inplace=True)
                elif self._freq == 'M' :
                    _start = dt.strptime(_aux.iloc[0, 0], '%Y-%m-%d').date()
                    _aux.loc[:, 'date'] = _aux.loc[:, 'date'].map(lambda x: x[:7])
                    _aux = (_aux.drop_duplicates('date', keep='last')
                                .set_index('date'))
                    _aux.index = pd.date_range(_start, periods = _aux.shape[0], freq=self._freq)
                
                     
                _aux.columns = ticker_map.keys()
                _temp['canada'] = _aux
            
            _df = pd.DataFrame(_temp['canada'].loc[:, tic])
            _data.append(_df)

        return _data[0].join(_data[1:], how='outer')

    @property
    def data(self):
        return self._data