from datetime import datetime as dt
from pandas.tseries.offsets import CDay

def first_day(i_date) :
    # Returns the first day of the next month given an initial_date
    i_month = i_date.month
    if i_month < 12 :
        f_month = i_date.month + 1
        f_year = i_date.year
    else :
        f_month = 1
        f_year = i_date.year + 1
    
    f_date_str = '01/' + str(f_month) + '/' + str(f_year)
    return dt.strptime(f_date_str, '%d/%m/%Y').date()


def eDate(i_date, x) :
    # Returns the same date one x months ahead
    f_month = (i_date.month + x) % 12
    if f_month == 0 : f_month = 12
    f_year = i_date.year + int((i_date.month + x - 1) / 12)
    f_day = i_date.day
    
    return dt(f_year, f_month, f_day).date()

def isMonthEnd(date) :
    #Check if data in month end
    _date1 = date + CDay(1)
    if _date1.month == date.month :
        return False
    else : 
        return True

#Returns the end of month (business day)
def EoMonth(date) :
    if date.month == 12 :
        _m = 1
        _y = date.year + 1
    else :
        _m = date.month + 1
        _y = date.year
    
    next_month_date = dt(_y, _m, 1).date()
    return (next_month_date - CDay(1)).date()

def EoXMonth(date, x) :
    _m = (date.month + x + 1) % 12
    if _m == 0: _m = 12
    _y = date.year + int((date.month + x) / 12)
        
    _date = dt(_y, _m, 1).date()
    return (_date - CDay(1)).date()

def quarterDate(quarter:str) :
    year = int(quarter[:4])
    month = int(quarter[-1]) * 3
    day = 15
    return EoMonth(dt(year, month, day).date())