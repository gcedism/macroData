#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import io
import logging
import pandas as pd
from datetime import datetime as dt
from datetime import date
import yfinance as yf

from .utils import yahoo_mapping, philly_mapping, EoXMonth, endog, isEndOfMonth

logger = logging.getLogger(__name__)

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
        self.update()
    
    @property
    def data(self) :
        return self._data

class Yahoo(Client) :
    
    def update(self):
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
        
        if self._freq != 'B' :
            # Correct data to last calendar day to match other time series
            _data.index = _data.index.map(lambda x : EoXMonth(x, -1, False))
        
        logger.info(f'Yahoo data downloaded for {self._tickers}')
        self._data = _data
    
class Manual(Client) :
    
    def update(self) :
        print('Retrieving data from Manual csv File...')
        
        self._data = endog.loc[(endog.index >= self._start_dt) * (endog.index <= self._end_dt), self._tickers]
    
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

        self._data = _data[0].join(_data[1:], how='outer')
    
class Treasury(Client) :
    
    def update(self):
        print('Retrieving data from Treasury data...')
        _data = []
        _temp = {}
        for tic in self._tickers :
            
            if 'treasury' not in _temp.keys() :
                dfs = []
                for year in range(self._start_dt.year, self._end_dt.year+1) :
                    params = {
                        'type' : 'daily_treasury_real_yield_curve',
                        'field_tdr_date_value' : str(year),
                        '_format' : 'csv'
                    }
                    p_csv = {
                        'index_col': 0,
                    }
                    
                    url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/' + str(year) + '/all?'
        
                    r = requests.get(url, params=params).content
                    if len(r) > 0 :
                        _df = pd.read_csv(io.StringIO(r.decode('utf-8')), **p_csv)
                        dfs.append(_df)
                
                df = pd.concat(dfs)
                df.index = df.index.map(lambda x : dt.strptime(x, '%m/%d/%Y').date())
                df.columns = ['us_5y_real_rate', 'us_7y_real_rate',
                             'us_10y_real_rate2', 'us_20y_real_rate',
                             'us_30y_real_rate']
                _temp['treasury'] = df.sort_index()
                
            final_df = pd.DataFrame(_temp['treasury'].loc[:, tic])
            _data.append(final_df)
            
        final_data = _data[0].join(_data[1:], how='outer')
        if self._freq == 'M' :
            final = final_data.loc[[isEndOfMonth(x) for x in final_data.index]]
            # Correct data to last calendar day to match other time series
            final.index = final.index.map(lambda x : EoXMonth(x, 0, False))
            self._data = final
        else :
            self._data = final_data