import sys
import os
import io
import json
import requests
import zeep

import pandas as pd
import numpy as np
import yfinance as yf

from pandas.tseries.offsets import CDay
from datetime import datetime as dt
from datetime import timedelta as td


sys.path.append(os.getcwd() + '/..')
from _aux.constants import DATES, API_KEYS, SOURCES
from _aux.dateFunctions import isMonthEnd, EoMonth, eDate, quarterDate
from _aux.auxFunctions import endog

class database() :
    
    def __init__(self, i_var:dict, freq:int) :
        self.freq = freq
        self.var:dict = {}
        
        _start_dt = DATES['start_dt'] if freq == 1 else DATES['q_start_dt']
        
        self.index = [EoMonth(eDate(_start_dt, x)) for x in range(0, 360, freq)]
        self.data = pd.DataFrame(index = self.index)
        self.add_items(i_var)
            
    def add_items(self, new_var: dict) :
        self.var.update(new_var)
        
        for source in SOURCES : 
            _items = [self.var[x]['source']['kwargs'] for x in self.var if self.var[x]['source']['name'] == source]
            if _items != [] :
                new_data = getattr(self, '_get_'+ source)(_items)
                self.data = self.data.join(new_data, how = 'outer')
    
    def _get_yahoo(self, kwargs:dict) :
        print('Retrieving data from Yahoo Finance...')
        tickers = [x['code'] for x in kwargs]     
        y_params = {
            'tickers' : tickers,
            'start' : DATES['start'],
            'end' : DATES['end'],
            'interval' : '1d'
        }
        _data = yf.download(**y_params)
        _data = _data['Adj Close']
        _data.index = [x.date() for x in _data.index]
        if self.freq == 1 :
            _data = _data.loc[_data.index.map(isMonthEnd)]
        else :
            _data = _data.fillna(method = 'bfill')
            
        # If only one ticker is provided, yf returns a Series with no adjustment on names
        if len(tickers) == 1 :
            _data.name = kwargs['name']
        else : 
            mapping = {x['code'] : x['name'] for x in kwargs}
            _data.columns = _data.columns.map(mapping)
            
        return _data
    
    def _get_bls(self, kwargs:dict) :
        print('Retrieving data from BLS - Bureau of Labour Statistics...')
        tickers = [x['code'] for x in kwargs]
        p = {
            "registrationkey" : API_KEYS['BLS_API_KEY'],
            "seriesid" : tickers,
            "startyear" : DATES['start_year'],
            "endyear" :  DATES['end_year']
        }
        url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
        h = {'Content-type': 'application/json'}
    
        _data = self._aux_blsData(url, p, h, kwargs)
    
        #Max data is only 20 years, we have to extract in two tranches
        p["startyear"] = "2013"
        _data2 = self._aux_blsData(url, p, h, kwargs)
    
        _data = pd.concat((_data, _data2))
    
        _index = self.index[:_data.shape[0]]
        _data.index = _index
    
        return _data

    def _aux_blsData(self, url, p, h, kwargs:dict) :
        mapping = {x['code']:x['name'] for x in kwargs}
        s = requests.post(url, data=json.dumps(p), headers=h).text
        a = {x['seriesID'] : x['data'] for x in json.loads(s)['Results']['series']}
        b = {k:pd.DataFrame(v, columns = ['value']).rename(columns = {'value' : mapping[k]})
                                                   .sort_index(ascending = False)
                                                   .set_index(pd.Index(range(len(v)))) for k, v in a.items()}
        _data = b[list(mapping.keys())[0]].join([b[x] for x in b][1:], how = 'outer')
    
        return _data
    
    def _get_fred(self, kwargs:dict) :
        print('Retrieving data from FRED - FED St Louis Economic Data...')
        tickers = {x['code']: x['name'] for x in kwargs}
        p = {
            'api_key' : API_KEYS['FRED_API_KEY'],
            'file_type': 'json',
            'observation_start' : DATES['start'],
            'observation_end' : DATES['end'],
            'frequency' : 'm',
            'aggregation_method' : 'eop'
        }
        url = 'https://api.stlouisfed.org/fred/series/observations'
    
        _data = {}
        for tic in tickers :
            p['series_id'] = tic
            f_data = json.loads(requests.get(url, p).text)
            f_df = pd.DataFrame(f_data['observations'])[['date', 'value']]
            f_df.index = f_df['date']
            f_Series = f_df['value']
            f_Series = f_Series.replace(['.'],0).astype(float)
        
            _data[tickers[tic]] = f_Series
        
        _data = pd.DataFrame.from_dict(_data)
        _data.index = _data.index.map(lambda x : (eDate(dt.strptime(x, '%Y-%m-%d').date(), 1) - CDay(1)).date())
    
        return _data
    
    def _get_census(self, kwargs:dict) :
        print('Retrieving data from Census...')
        p = {
            'timeSlotType': '12',
            'startYear': DATES['start_year'],
            'endYear': DATES['end_year'],
            'geoLevelCode': 'US',
            'adjusted': 'yes',
            'errorData': 'no',
            'internal': 'false'
        }
        url = 'https://www.census.gov/econ/currentdata/export/csv'
        p_csv = {
            'skiprows': [0, 1, 2, 3, 4, 5, 6],
            'index_col': 0
        }
    
        _data = {}
        for tic in kwargs :
            p['programCode'] = tic['programCode']
            p['categoryCode'] = tic['categoryCode']
            p['dataTypeCode'] = tic['dataTypeCode']
            _s = requests.get(url, p).content
            _data[tic['name']] = pd.read_csv(io.StringIO(_s.decode('utf-8')), **p_csv).iloc[:-2].loc[:, 'Value'].values
    
        _df = pd.DataFrame.from_dict(_data)
    
        _index = self.index[:_df.shape[0]]
        _df.index = _index

        return _df  
    
    def _get_bea(self, kwargs:dict) :
        print('Retrieving data from BEA - Bureau of Economic Analyses...')
        p = {
            'UserID' : API_KEYS['BEA_API_KEY'],
            'method' : 'GetData',
            'Frequency' : 'Q',
            'Year' : [str(x) for x in range(1993, 2023)],
            'ResultFormat' : 'json'
        }
        url = 'https://apps.bea.gov/api/data/'    
    
        _data = []
        for tic in kwargs :
            p['DataSetName'] = tic['DataSetName']
            p['TableName'] = tic['TableName']
            s = requests.get(url, p).text
            _df = pd.DataFrame(json.loads(s)['BEAAPI']['Results']['Data'])
            _df.set_index('TimePeriod', inplace = True)
            ser = _df[_df['LineNumber'] == '1']['DataValue']
            
            ser.index = ser.index.map(quarterDate)
            ser.name = tic['name']
            _data.append(ser)
        
        return pd.DataFrame(index = self.index).join(_data, how = 'outer')
    
    def _get_fed(self, kwargs) :
        print('Retrieving data from FED...')
        url = 'https://www.federalreserve.gov/datadownload/Output.aspx'
        p = {
            'rel' : 'G17',
            'series' : '5d88c03b0036f0334d78f6bafefc5101',
            'lastobs' : [],
            'from' : '01/01/1993',
            'to' : '12/31/2022',
            'filetype' : 'csv',
            'label' : 'include',
            'layout' : 'seriescolumn'
        }
        
        _data = {}
        for tic in kwargs : 
            p_csv = {
                'index_col' : 0,
                'skiprows' : 5,
                'usecols' : tic['usecols']
            }
            r = requests.get(url, p)
            open('temp.xls', 'wb').write(r.content)
            _df = pd.read_csv('temp.xls', **p_csv)
            _df.columns = tic['colNames']
            _df.index = self.index[:_df.shape[0]]
            _data[tic['name']] = _df
        
        return _data[tic['name']]
    
    def _get_philly(self, kwargs) :
        print('Retrieving data from Philly Fed...')
        url = 'https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/mbos/historical-data/diffusion-indexes/bos_dif.csv?la=en&hash=433F3C508D5269FD08053D9CCB63FBD7'
        s = requests.get(url).content
        open('temp.csv', 'wb').write(s)
        _df = pd.read_csv('temp.csv', index_col = 0)
        _df.columns = _df.columns.map(kwargs[0]['mapping'])
        _df.index = _df.index.map(lambda x: EoMonth(dt.strptime(x, '%b-%y').date()))
        
        return _df.loc[[x for x in _df.index if x in self.index]]
    
    def _get_ons(self, kwargs) :
        print('Retrieving data from ONS - Office for National Statistics...')
        _data = []
        for tic in kwargs :
            url = 'https://www.ons.gov.uk/file?' + tic['url']
            p = {
                'sheet_name' : tic['sheet_name'],
                'skiprows' : tic['skiprows'],
                'index_col' : 0,
                'usecols' : tic['usecols'],
                'engine' : 'openpyxl'
            }
            r = requests.get(url)
            open('temp.xls', 'wb').write(r.content)
            df = pd.read_excel('temp.xls', **p)
            df.columns = tic['colNames']
            try :
                firstRow = [x for x in range(df.shape[0]) if str(df.index[x]).lower() == '1993 jan'][0]
            except :
                firstRow = 0
            lastRow = [x for x in range(df.shape[0]) if pd.isna(df.index[x])][0] if len([x for x in range(df.shape[0]) if pd.isna(df.index[x])]) > 0 else df.shape[0]
            df = df.iloc[firstRow:lastRow]
            df.index = [EoMonth(dt.strptime(x, '%Y %b').date()) for x in df.index]
            df.loc[df.index >= DATES['start_dt']]
            _data.append(df)
        
        _df = _data[0].join(_data[1:], how = 'outer')
    
        return _df
    
    def _get_ec(self, kwargs:dict) :
        print('Retrieving data from Eurostat Data...')
        p = {
            'format' : 'SDMX-CSV',
            'lang' : 'en',
            'detail' : 'dataonly',
            'startPeriod' : DATES['start_per'] 
        }
        url = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/'
        p_csv = {
            'index_col' : []
        }
    
        data = []
        for tic in kwargs :
            url_f = url + tic['flow'] + tic['filter']
        
            s = requests.get(url_f, p).content
            open('temp.csv', 'wb').write(s)
            df = pd.read_csv('temp.csv', **p_csv)
        
            _data = df.pivot_table(values = 'OBS_VALUE', index = 'TIME_PERIOD', columns = 'geo', aggfunc = np.sum)
            _data.columns = [tic['name']]
            data.append(_data)
        
        final = data[0].join(data[1:], how = 'outer')
        final.index = self.index[:final.shape[0]]
    
        return final 
    
    def _get_can(self, kwargs) :
        print('Retrieving data from Canada Central Bank...')
        url = 'https://www.bankofcanada.ca/valet/observations/group/bond_yields_benchmark/csv'
        p_csv = {
            'skiprows': 23,
            'usecols' : [0, 1, 3, 5],
            'index_col': 0
        }
        _s = requests.get(url).content
        _data = pd.read_csv(io.StringIO(_s.decode('utf-8')), **p_csv)
        _data.index = _data.index.map(lambda x : dt.strptime(x, '%Y-%m-%d').date())
        _alt_index = [x for x in _data.index if x in self.index]
        _data.columns = kwargs[0]['cols']
    
        return _data.loc[_alt_index]
    
    def _get_bcb(self, kwargs) : 
        print('Retrieving data from BCB...')
        series = [x for x in kwargs[0]['mapping']]
        wsdl = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
        client = zeep.Client(wsdl=wsdl)
        a = client.service.getValoresSeriesVO(in0 = series, in1 = DATES['start_2'], in2 = DATES['end_2'])
        dates = [EoMonth(dt(a[0]['valores'][j]['ano'], a[0]['valores'][j]['mes'], a[0]['valores'][j]['dia']).date()) for j in range(len(a[0]['valores']))]
        
        _data = pd.DataFrame([[a[i]['valores'][j]['svalor']['_value_1'] for j in range(len(dates))] for i in range(len(a))]).T
        _data.index = dates
        _data.columns = [kwargs[0]['mapping'][x] for x in series]
        
        return _data
    
    def _get_manual(self, kwargs) :
        print('Retrieving data from Manual csv File...')
        cols = [x['code'] for x in kwargs]
        
        return endog[cols]