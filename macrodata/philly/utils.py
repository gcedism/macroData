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
    'us_cur_activity' : 'GAC',
    'us_cur_new_orders' : 'NOC',
    'us_cur_shipments' : 'SHC',
    'us_unfilled_orders' : 'UOC',
    'us_cur_delivery_time' : 'DTC',
    'us_cur_inventories' : 'IVC',
    'us_cur_prices_paid' : 'PPC',
    'us_cur_prices_received' : 'PRC',
    'us_cur_employment' : 'NEC',
    'us_cur_avg_workweek' : 'AWC',
    'us_fut_activity' : 'GAF',
    'us_fut_new_orders' : 'NOF',
    'us_fut_shipments' : 'SHF',
    'us_fut_unfilled_orders' : 'UOF',
    'us_fut_delivery_time' : 'DTF',
    'us_fut_inventories' : 'IVF',
    'us_fut_prices_paid' : 'PPF',
    'us_fut_prices_received' : 'PRF',
    'us_fut_employment' : 'NEF',
    'us_fut_avg_workweek' : 'AWF',
    'us_fut_capex' : 'CEF'
}