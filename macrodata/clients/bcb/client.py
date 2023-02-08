#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import zeep
import requests
import pandas as pd
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
        self._start = date.strftime(start_dt, '%d/%m/%Y')
        self._end_dt = end_dt
        self._end = date.strftime(end_dt, '%d/%m/%Y')
        self._data = self._get_bcb(tickers)
        
    def _get_bcb(self, tickers):
        print('Retrieving data from BCB...')
        
        _temp = {}
        final_data = []
        for tic in tickers :
            if 'bcb_data' not in _temp.keys() :
                series = [ticker_map[x]['code'] for x in ticker_map]
                wsdl = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
                client = zeep.Client(wsdl=wsdl)
                a = client.service.getValoresSeriesVO(in0=series, in1=self._start, in2=self._end)
                dates = [
                    EoXMonth(dt(a[0]['valores'][j]['ano'], a[0]['valores'][j]['mes'],
                        a[0]['valores'][j]['dia']).date(), 0) for j in range(len(a[0]['valores']))]

                _data = pd.DataFrame([[a[i]['valores'][j]['svalor']['_value_1'] 
                                   for j in range(len(dates))] for i in range(len(a))]).T
                _data.index = dates
                _data.columns = ticker_map.keys()
                _temp['bcb_data'] = _data
                
            _df = pd.DataFrame(_temp['bcb_data'].loc[:, tic])
            final_data.append(_df)
        
        final = final_data[0].join(final_data[1:], how='outer')
        # Correct data to last calendar day to match other time series
        final.index = final.index.map(lambda x : EoXMonth(x, 0, False))
        
        return final

    @property
    def data(self):
        return self._data