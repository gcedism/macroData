from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date
from pandas.tseries.offsets import CDay

def EoXMonth(dat:date, x:int, calendar:bool=True) -> date :
    """ 
    Function that returns the last day of x months ahead
    :parameters:
        date : date
            Original Date to be transformed
        x : int
            Number of months ahead (0 if same month)
        calendar : bool
            Whether to return the last business day or last calendar day
    """

    _m = (dat.month + x + 1) % 12
    if _m == 0: _m = 12
    _y = dat.year + int((dat.month + x) / 12)
        
    _date = date(_y, _m, 1)
    if calendar : 
        return (_date - CDay(1)).date()
    else :
        return (_date - td(days=1))

ticker_map = {
    'eu_ind_conf': {'flow': 'ei_bsin_m_r2',
                    'filter': '/M.BS-ICI.SA.BAL.EU27_2020'},
    'eu_ind_inventories': {'flow': 'ei_bsin_m_r2',
                    'filter': '/M.BS-ISFP.SA.BAL.EU27_2020'},
    'eu_retail_sales': {'flow': 'EI_ISRR_M',
                        'filter': '/M.TOVT.RT1-SCA.G47.EU27_2020'},
    'eu_retail_sales_real': {'flow': 'EI_ISRR_M',
                             'filter': '/M.TOVV.RT1-SCA.G47.EU27_2020'},
    'eu_construction_conf' : {'flow': 'ei_bsin_m_r2',
                              'filter': '/M.BS-CCI.SA.BAL.EU27_2020'},
    'eu_services_conf' : {'flow': 'ei_bsin_m_r2',
                          'filter': '/M.BS-SCI.SA.BAL.EU27_2020'},
    'de_ind_conf': {'flow': 'ei_bsin_m_r2',
                    'filter': '/M.BS-ICI.SA.BAL.DE'},
    'fr_ind_conf': {'flow': 'ei_bsin_m_r2',
                    'filter': '/M.BS-ICI.SA.BAL.FR'},
    'uk_ind_conf': {'flow': 'ei_bsin_m_r2',
                    'filter': '/M.BS-ICI.SA.BAL.UK'},
    'eu_ca': {'flow': 'ei_bpm6ca_m',
               'filter': '/M.MIO_EUR.CA.S1.S1.BAL.EXT_EU27_2020.NSA.EU27_2020'},
    'de_ca': {'flow': 'ei_bpm6ca_m',
              'filter': '/M.MIO_EUR.CA.S1.S1.BAL.WRL_REST.NSA.DE'},
    'fr_ca': {'flow': 'ei_bpm6ca_m',
              'filter': '/M.MIO_EUR.CA.S1.S1.BAL.WRL_REST.NSA.FR'},
    'uk_ca': {'flow': 'ei_bpm6ca_m',
              'filter': '/M.MIO_EUR.CA.S1.S1.BAL.WRL_REST.NSA.UK'},
    'eu_ind_prod': {'flow': 'STS_INPR_M',
                    'filter': '/M.PROD.B-D.SCA.I15.EU27_2020'},
    'de_ind_prod': {'flow': 'STS_INPR_M',
                    'filter': '/M.PROD.B-D.SCA.I15.DE'},
    'fr_ind_prod': {'flow': 'STS_INPR_M',
                    'filter': '/M.PROD.B-D.SCA.I15.FR'},
    'uk_ind_prod': {'flow': 'STS_INPR_M',
                    'filter': '/M.PROD.B-D.SCA.I15.UK'}}