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
    'mxn_cpi_mom': {'id': '628201',
                    'fuente': 'BIE'},
    'mxn_cons_conf': {'id': '454168',
                      'fuente': 'BIE'
                      }
}