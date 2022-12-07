#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import io
import pandas as pd
from datetime import datetime as dt
from datetime import date
import yfinance as yf

from .utils import yahoo_mapping, philly_mapping, EoXMonth, endog

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
        self._tickers = tickers

class Yahoo(Client) :
    
    def update(self) -> pd.DataFrame:
        print('Retrieving data from Yahoo Finance...')
        codes = [yahoo_mapping[x] for x in self._tickers]
        per_map = {
            'B': '1d',
            'M' : '1mo',
            'Q' : '1mo',
            'A' : '1mo'
        }
        
        y_params = {
            'tickers': codes,
            'start': self._start_dt,
            'end': self._end_dt,
            'interval': per_map[self._freq]
        }
        _data = yf.download(**y_params)
        _data = _data['Adj Close']
        _data.index = [x.date() for x in _data.index]
        

        # If only one ticker is provided, yf returns a Series with no adjustment on names
        if len(self._tickers) == 1:
            _data.name = self._tickers[0]
        else:
            reverse_mapping = {yahoo_mapping[x]:x for x in self._tickers}
            _data.columns = _data.columns.map(reverse_mapping)
        
        # Correct data to last calendar day to match other time series
        _data.index = _data.index.map(lambda x : EoXMonth(x, 0, False))

        return _data
    
class Manual(Client) :
    
    def update(self) :
        print('Retrieving data from Manual csv File...')
        
        return endog.loc[(endog.index >= self._start_dt) * (endog.index <= self._end_dt), self._tickers]
    
class Philly(Client):
    
    def update(self) -> pd.DataFrame:
        print('Retrieving data from Philly Fed...')
        
        _temp = {}
        _data = []
        for tic in self._tickers:
            
            if 'philly_fed' not in _temp.keys() :
                url = 'https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/mbos/historical-data/diffusion-indexes/bos_dif.csv?la=en&hash=433F3C508D5269FD08053D9CCB63FBD7'
                _s = requests.get(url).content
                _df = pd.read_csv(io.StringIO(_s.decode('utf-8')), index_col=0)
                reverse_map = {philly_mapping[x]:x for x in philly_mapping}
                _df.columns = _df.columns.map(reverse_map)
                _df.index = _df.index.map(lambda x: EoXMonth(dt.strptime(x, '%b-%y').date(), 0, False))
                real_start = max(self._start_dt, min(_df.index[0], self._start_dt))
                real_end = min(self._end_dt, _df.index[-1])
                _temp['philly_fed'] = _df.loc[(_df.index >= real_start) * (_df.index <= real_end)]
            
            final_df = pd.DataFrame(_temp['philly_fed'].loc[:, tic])
            _data.append(final_df)

        return _data[0].join(_data[1:], how='outer')