#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import io
import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime as dt

from .utils import ticker_map, EoXMonth
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
        self._start_per = date.strftime(start_dt, '%Y-%m')
        self._end_dt = end_dt
        self._data = self._get_inegi(tickers)
        
    def _get_inegi(self, tickers:list[str]) -> pd.DataFrame:
        _data = []
        p = {'type': 'json'}
        
        for tic in tickers:
            url = ('http://en.www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'
            + ticker_map[tic]['id'] 
            + '/en/0700/false/' 
            + ticker_map[tic]['fuente'] 
            + '/2.0/' 
            + API_KEYS['INEGI_API_KEY'])
            s = requests.get(url, p).text
            _d = pd.DataFrame(json.loads(s)['Series'][0]['OBSERVATIONS']).set_index('TIME_PERIOD')
            _d.index = _d.index.map(lambda x: EoXMonth(dt.strptime(x, '%Y/%m').date(), 0, False))
            _d = _d.loc[_d.index >= self._start_dt].sort_index()['OBS_VALUE']
            _d.name = tic
            _data.append(pd.DataFrame(_d))

        _data = _data[0].join(_data[1:], how='outer')
        return _data

    @property
    def data(self):
        return self._data