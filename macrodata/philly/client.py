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
        self._end_dt = end_dt
        self._data = self._get_philly(tickers)
        
    def _get_philly(self, tickers:list[str]) -> pd.DataFrame:
        print('Retrieving data from Philly Fed...')
        
        _temp = {}
        _data = []
        for tic in tickers:
            
            if 'philly_fed' not in _temp.keys() :
                url = 'https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/mbos/historical-data/diffusion-indexes/bos_dif.csv?la=en&hash=433F3C508D5269FD08053D9CCB63FBD7'
                _s = requests.get(url).content
                _df = pd.read_csv(io.StringIO(_s.decode('utf-8')), index_col=0)
                reverse_map = {ticker_map[x]:x for x in ticker_map}
                _df.columns = _df.columns.map(reverse_map)
                _df.index = _df.index.map(lambda x: EoXMonth(dt.strptime(x, '%b-%y').date(), 0))
                _temp['philly_fed'] = _df
            
            final_df = pd.DataFrame(_temp['philly_fed'].loc[:, tic])
            _data.append(final_df)

        return _data[0].join(_data[1:], how='outer')

    @property
    def data(self):
        return self._data