#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import json
import requests
import zeep

import pandas as pd
import numpy as np
import yfinance as yf

from pandas.tseries.offsets import CDay
from datetime import datetime as dt
from datetime import date

from .constants import DATES, SOURCES #DATES TO BE ELIMINATED
from .constants_private import API_KEYS
from .dateFunctions import isMonthEnd, EoXMonth, eDate, quarterDate
from .utils import endog

#To be resolved more independetly :
from .bls import Client as bls_Client
from .fred import Client as fred_Client
from .census import Client as census_Client
from .bea import Client as bea_Client
from .fed import Client as fed_Client
from .ons import Client as ons_Client
from .bcb import Client as bcb_Client
from .eurostat import Client as es_Client
from .inegi import Client as inegi_Client
from .philly import Client as philly_Client
from .can import Client as can_Client

class Database():
    def __init__(self, i_var: dict, start_dt: date, end_dt: date, freq: str):
        """ Data base initializing 
        :parameters:
            i_var: dict
                Dictionary with list of variables with parameteres in the structure :
                    description :
                    asset_class :
                    sub_asset_class
                    region :
                    source :
                        name :
                        kwargs :
                    frequency : Frequency available
                    transform : If possible or not to transform
            start_dt : datetime.Date
                Start date to start extraction
            end_dt : datetime.Date
                End date to end extraction
            freq: str
                Frequency of the data, available values are : B, M, Q, A
        """
        
        self._freq = freq              
        self._start_dt = start_dt
        self._end_dt = end_dt

        self._var: dict = {}
        self._index = pd.date_range(start_dt, end_dt, freq=freq)
        self._data = pd.DataFrame(index=self._index)
        self.add_items(i_var)
   
    def add_items(self, new_var: dict):
        self._var.update(new_var)
        
        for source in SOURCES:
            _items = [self._var[x]['source']['kwargs'] for x in self._var
                      if self._var[x]['source']['name'] == source]
            if _items != []:
                new_data = getattr(self, '_get_' + source)(_items)
                self._data = self._data.join(new_data, how='outer')
                # self.debug = new_data
        
        # self.data = (self.data.replace(',', '', regex=True)
        #              .replace(' - ', np.nan, regex=True)
        #              .astype(float)
        #              .interpolate(limit_area='inside'))

    def _get_yahoo(self, kwargs: dict):
        print('Retrieving data from Yahoo Finance...')
        tickers = [x['code'] for x in kwargs]
        y_params = {
            'tickers': tickers,
            'start': dt.strftime(self._start_dt, '%Y-%m-%d'),
            'end': dt.strftime(self._end_dt, '%Y-%m-%d'),
            'interval': '1d'
        }
        _data = yf.download(**y_params)
        _data = _data['Adj Close']
        _data.index = [x.date() for x in _data.index]
        if self.freq != 'd':
            _data = _data.loc[_data.index.map(isMonthEnd)]

        # If only one ticker is provided, yf returns a Series with no adjustment on names
        if len(tickers) == 1:
            _data.name = kwargs[0]['name']
        else:
            mapping = {x['code']: x['name'] for x in kwargs}
            _data.columns = _data.columns.map(mapping)
        
        # Correct data to last calendar day to match other time series
        _data.index = _data.index.map(lambda x : EoXMonth(x, 0, False))

        return _data
    
    def _get_bls(self, kwargs: dict) -> pd.DataFrame:
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = bls_Client(tickers, self._start_dt, self._end_dt, self._freq).data
    
        return _data

    def _get_fred(self, kwargs: dict):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = fred_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_census(self, kwargs: dict):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = census_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_bea(self, kwargs: dict):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = bea_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_fed(self, kwargs):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = fed_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_philly(self, kwargs:dict):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = philly_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_ons(self, kwargs:dict):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = ons_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_ec(self, kwargs: dict):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = es_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data
        
    def _get_can(self, kwargs):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = can_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    # BRAZILIAN CENTRAL BANK
    def _get_bcb(self, kwargs):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = bcb_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    #MEXICO NATIONAL INSTITUTE DE ESTATISTICA
    def _get_inegi(self, kwargs):
        
        tickers = [x['name'] for x in kwargs] # Will change when all functions will be called with ticker list
        _data = inegi_Client(tickers, self._start_dt, self._end_dt, self._freq).data
    
        return _data

    def _get_manual(self, kwargs):
        print('Retrieving data from Manual csv File...')
        cols = [x['code'] for x in kwargs]

        return endog[cols]
    
    @property
    def data(self):
        return self._data
    
    @property
    def freq(self):
        return self._freq
    
    @property
    def start_dt(self):
        return self._start_dt
    
    @property
    def end_dt(self):
        return self._end_dt
