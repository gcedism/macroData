from datetime import datetime as dt
from datetime import timedelta as td

start = '1993-01-01'
start_2 = '01/01/1993'
start_dt = dt.strptime(start, '%Y-%m-%d').date()
q_start_dt = dt.strptime('1993-03-15', '%Y-%m-%d').date()
end_dt = dt.now().date()
end = dt.strftime(end_dt, '%Y-%m-%d')
end_2 = '01/09/2022'

DATES = {
    'start' : start,
    'start_2' : start_2,
    'start_dt' : start_dt,
    'start_per' : '1993-01',
    'q_start_dt' : q_start_dt,
    'end' : end,
    'end_2' : end_2,
    'end_dt' : end_dt,
    'start_year': '1993',
    'end_year' : '2022'
}

API_KEYS = {
    'FRED_API_KEY' : '670447b1b80828dd0122187f1d2661ae',
    'BEA_API_KEY' : '7B01FC1C-8919-4AC2-BD04-C34BA76ABCD8',
    'BLS_API_KEY' : '8494059d2e194e3d92592613a48ce565',
    'NASDAQ_API_KEY' : 'YzwzXVQ-yw77QqS8dwEA',
    'CENSUS_API_KEY' : 'f19c09f7b92debf8e9e2f2561ffadba6f3efab72',
    'EIA_API_KEY' : 'm2y6m4NRfTSGGrtZ9bJTgAkfxyScHcbPBEUSUeTP'
}

SOURCES = ['yahoo', 'bls', 'fred', 'census', 'bea', 'fed', 'philly', 'ons', 'can', 'ec', 'bcb', 'manual']