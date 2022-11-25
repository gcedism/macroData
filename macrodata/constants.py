from datetime import datetime as dt

d_start = '2020-12-31'
d_start_dt = dt.strptime(d_start, '%Y-%m-%d').date()
m_start = '1970-01-01'
m_start_2 = '01/01/1993'
m_start_dt = dt.strptime(m_start, '%Y-%m-%d').date()
q_start_dt = dt.strptime('1993-03-15', '%Y-%m-%d').date()
end_dt = dt.now().date()
end = dt.strftime(end_dt, '%Y-%m-%d')
end_2 = '01/09/2022'

DATES = {
    'start' : m_start,
    'start_2' : m_start_2,
    'start_dt' : m_start_dt,
    'start_per' : '1993-01',
    'd_start' : d_start,
    'd_start_dt' : d_start_dt,
    'm_start' : m_start,
    'm_start_dt' : m_start_dt,
    'q_start_dt' : q_start_dt,
    'end' : end,
    'end_2' : end_2,
    'end_dt' : end_dt,
    'start_year': '1993',
    'end_year' : '2022'
}

SOURCES = ['yahoo', 'bls', 'fred', 'census', 'bea', 'fed', 'philly', 'ons', 'can', 'ec', 'bcb', 'inegi', 'manual']