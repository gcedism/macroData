from datetime import date 
from datetime import timedelta as td
from pandas.tseries.offsets import CDay

ticker_map = {
    'bra_ipca_MoM': {'code': '433'},
    'bra_reserves' : {'code' : '3546'},
    'bra_net_debt_to_gdp' : {'code' : '4513'},
    'bra_deliquency' : {'code' : '21082'},
    'bra_trade_balance' : {'code' : '22704'},
    'bra_fdi' : {'code' : '22865'},
    'bra_fdi2' : {'code' : '22885'},
    'bra_unemployment_rate' : {'code' : '24369'},
    'bra_m1' : {'code' : '27840'},
    'bra_employment' : {'code' : '28763'}
}

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
   