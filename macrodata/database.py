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
from .can import Client as can_Client
from .modules import Yahoo, Manual, Philly

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
            securities:
                List of securities with its specificities to build up reports
        """
        
        self._freq = freq              
        self._start_dt = start_dt
        self._end_dt = end_dt

        self._var: dict = {}
        self._index = [x.date() for x in pd.date_range(start_dt, end_dt, freq=freq)]
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

    def desc(self) :
        """
        Gives a quick summary of the data collected 
        """
        real_data = self._data.dropna()
        print(f'Total non NA data : {real_data.shape[0]}')
        real_start = real_data.index[0]
        real_end = real_data.index[-1]
        print(f"From {format(real_start, '%Y-%m-%d')} to {format(real_end, '%Y-%m-%d')}")
        nMonths = (real_end.month - real_start.month) + (real_end.year - real_start.year) * 12 + 1
        print(f'Theorical number of months : {nMonths}')                                                
                                                                           
        index = pd.MultiIndex.from_tuples([(self._var[x]['source']['name'], x) for x in self._var])
        last_dates = [self._data.loc[:, x].dropna().index[-1] for x in self._data]
        last_values = [self._data.loc[:, x].dropna().iloc[-1] for x in self._data]
        last_nvalues = [self._data.loc[:, x].isna().sum() for x in self._data]
        return pd.DataFrame([last_dates, last_values, last_nvalues], columns=index, index=['last_date', 'last_value', 'n of obs']).T

    """ ****************** EMBEDDED CLIENTS ************************************* """
    
    def _get_yahoo(self, kwargs: dict):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'yahoo']
        _data = Yahoo(tickers, self._start_dt, self._end_dt, self._freq).update()
    
        return _data
    
    def _get_philly(self, kwargs:dict):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'philly']
        _data = Philly(tickers, self._start_dt, self._end_dt, self._freq).update()
        
        return _data
    
    def _get_manual(self, kwargs):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'manual']
        _data = Manual(tickers, self._start_dt, self._end_dt, self._freq).update()
    
        return _data
       
    
    """ ****************** STAND ALONE API CLIENTS ************************************* """
    
    def _get_bls(self, kwargs: dict) -> pd.DataFrame:
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'bls']
        _data = bls_Client(tickers, self._start_dt, self._end_dt, self._freq).data
    
        return _data

    def _get_fred(self, kwargs: dict):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'fred']
        _data = fred_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_census(self, kwargs: dict):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'census']
        _data = census_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_bea(self, kwargs: dict):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'bea']
        _data = bea_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_fed(self, kwargs):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'fed']
        _data = fed_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_ons(self, kwargs:dict):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'ons']
        _data = ons_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    def _get_ec(self, kwargs: dict):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'ec']
        _data = es_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data
        
    def _get_can(self, kwargs):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'can']
        _data = can_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    # BRAZILIAN CENTRAL BANK
    def _get_bcb(self, kwargs):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'bcb']
        _data = bcb_Client(tickers, self._start_dt, self._end_dt, self._freq).data
        
        return _data

    #MEXICO NATIONAL INSTITUTE DE ESTATISTICA
    def _get_inegi(self, kwargs):
        
        tickers = [x for x in self._var.keys() if self._var[x]['source']['name'] == 'inegi']
        _data = inegi_Client(tickers, self._start_dt, self._end_dt, self._freq).data
    
        return _data

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
