from datetime import date 
from datetime import timedelta as td
from pandas.tseries.offsets import CDay

ticker_map = {
    'us_pers_spending': {'DataSetName': 'NIUnderlyingDetail',
                         'TableName': 'U20306'},
    'us_gdp': {'DataSetName': 'NIPA',
               'TableName': 'T10101'},
    'us_pce': {'DataSetName': 'NIUnderlyingDetail',
               'TableName': 'U20304'}
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

def quarterDate(quarter:str) -> date :
    """
    :parameters:
        quarter : str
            Quarter as a string in the format of YYYYQ
    :returns: 
        A date by the end of the quarter
    """

    year = int(quarter[:4])
    month = int(quarter[-1]) * 3
    day = 15
    return EoXMonth(date(year, month, day), 0, False)