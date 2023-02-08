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
        self._data = self._get_ec(tickers)
        
    def _get_ec(self, tickers:list[str]) -> pd.DataFrame:
        print('Retrieving data from Eurostat Data...')
        
        p = {
            'format': 'SDMX-CSV',
            'lang': 'en',
            'detail': 'dataonly',
            'startPeriod': self._start_per
        }
        url = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/'

        data = []
        for tic in tickers:
            url_f = url + ticker_map[tic]['flow'] + ticker_map[tic]['filter']

            _s = requests.get(url_f, p).content
            df = pd.read_csv(io.StringIO(_s.decode('utf-8')))

            if not df.empty :
                _data = df.pivot_table(values='OBS_VALUE', index='TIME_PERIOD', columns='geo', aggfunc=np.sum)
                _data.columns = [tic]
                _data.index = _data.index.map(lambda x: EoXMonth(dt.strptime(x, '%Y-%m').date(), 0))
            else :
                _data = pd.DataFrame()
                print(f'No data for {tic}')
                #TO DO : transfrom into Logging
            data.append(_data)

        final = data[0].join(data[1:], how='outer')
         # Correct data to last calendar day to match other time series
        final.index = final.index.map(lambda x : EoXMonth(x, 0, False))

        return final

    @property
    def data(self):
        return self._data