#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import io
import pandas as pd
from datetime import date 

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
        self._start_year = start_dt.year
        self._end_year = end_dt.year
        self._data = self._get_census(tickers)
        
    def _get_census(self, tickers):
        print('Retrieving data from Census...')
        p = {
            'format' : 'csv',
            'adjusted' : 'true',
            'notAdjusted' : 'false',
            'errorData' : 'false',
            'mode' : 'report',
            'errormode' : 'Ind',
            'timeSlotType': '12',
            'submit' : 'GET+DATA',
            'startYear': self._start_year,
            'endYear': self._end_year,
            'geoLevel': 'US',
            'vert' : '1',
        }
        # url = 'https://www.census.gov/econ/currentdata/export/csv' Old one
        url = 'https://www.census.gov/econ_export/'
        
        p_csv = {'skiprows': 6, 'index_col': 0}

        _data = []
        for tic in tickers:
            p['program'] = ticker_map[tic]['program']
            p['categories[0]'] = ticker_map[tic]['categories']
            p['dataType'] = ticker_map[tic]['dataType']
            _s = requests.get(url, p).content
            _data.append(pd.read_csv(io.StringIO(_s.decode('utf-8')), **p_csv).rename({'Value': tic}, axis=1))
        
        _start = date(self._start_year, 1, 1)
        _end = date(self._end_year+1, 1, 1)
        _index = pd.date_range(_start, _end, freq=self._freq)
                
        final_data = _data[0].join(_data[1:], how='outer')
        final_data.index = _index
        final_data.index = final_data.index.map(lambda x: x.date())
        
        return final_data


    @property
    def data(self):
        return self._data