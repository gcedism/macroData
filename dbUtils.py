#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pandas as pd
from pandas.tseries.offsets import CDay
from datetime import date
from datetime import datetime as dt
import yfinance as yf

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine.url import URL

from IPython.display import display_html

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def tablesDescription(dbPathName:str) :
    DATABASE = {
       'drivername': 'sqlite',
       'database': dbPathName
    }

    engine = sa.create_engine(URL.create(**DATABASE))
    
    insp = sa.inspect(engine)
    table_names = insp.get_table_names()
    
    meta = sa.MetaData(engine)
    tables = {}
    for table_name in table_names :
        tables[table_name] = sa.Table(table_name, meta, autoload=True)
        
    tpl = f'''
    <div>Database {dbPathName} details :</div>
    '''
    
    for table in tables :
        tpl += f'''
        <div>
            <table>
                <tr>
                    <td></td>
                    <td>Name</td>
                    <td>Type</td>
                    <td>Null</td>
                    <td>prKey</td>
                </tr>
                <tr>
                    <td>{table}</td>
        '''
        for col in tables[table].c :
            tpl += f'''
                    <td>{col.name}</td>
                    <td>{col.type}</td>
                    <td>{col.nullable}</td>
                    <td>{col.primary_key}</td>
                </tr>
                <tr>
                    <td></td>
                '''
    
        tpl += '''
                </tr>
            </table>
        </div>
        '''
    
    display_html(tpl, raw=True)
    

def lastHistory(dbPathName:str, tableName:str,
                n:int, accounts:list[str]=None) -> pd.DataFrame :
    DATABASE = {
       'drivername': 'sqlite',
       'database': dbPathName
    }

    engine = sa.create_engine(URL.create(**DATABASE))
    Base = orm.declarative_base()
    table = sa.Table(tableName, Base.metadata, autoload_with=engine)
    
    conn = engine.connect()
    if not accounts == None :
        stmt = sa.select(table).order_by([col for col in table.c if col.primary_key==True][0].desc()).where(table.c.account.in_(accounts)).limit(n)
    else :
        stmt = sa.select(table).order_by([col for col in table.c if col.primary_key==True][0].desc()).limit(n)
    
    return pd.read_sql(stmt, conn, index_col = table.c.keys()[0]).sort_index()

  
def addCashTrade(currency:str, amount:float, date:date, account:str,
                 classification:str, dbPathName:str) :
    
    DATABASE = {
       'drivername': 'sqlite',
       'database': dbPathName
    }
    engine = sa.create_engine(URL.create(**DATABASE))
    
    Base = orm.declarative_base()
    class CashTrade(Base) :
        __table__ = sa.Table('cash_blotter', Base.metadata, autoload_with=engine)
    
    session = orm.Session(engine)
    newTrade = CashTrade(currency=currency, amount=amount, date=date, account=account,
                        classification=classification)
    session.add(newTrade)
    session.commit()
    
    logger.info('Cash Trade added sucessfully')
    
    session.close()
    engine.dispose()
    
    logger.info('Session closed, engine disposed')
    
#Maybe studdy asyncronous adding / or threading 
def addTrade(ticker:str, date:date, quantity:float, cost_price:float,
             account:str, currency:str, dbPathName:str):
    DATABASE = {
        'drivername': 'sqlite',
        'database': dbPathName
    }

    engine = sa.create_engine(URL.create(**DATABASE))
    Base = orm.declarative_base()
    class Trade(Base) :
        __table__ = sa.Table('blotter', Base.metadata, autoload_with=engine)

    session = orm.Session(engine)
    newTrade = Trade(ticker=ticker, date=date,
                       quantity=quantity, cost_price=cost_price, account=account)
    
    session.add(newTrade)
    session.flush()
    session.refresh(newTrade)
    session.commit()
    
    logger.info('Trade added sucessfully')
    
    class CashTrade(Base) :
        __table__ = sa.Table('cash_blotter', Base.metadata, autoload_with=engine)
        
    cash_trade = {
        'currency' : currency,
        'amount' : - newTrade.quantity * newTrade.cost_price, 
        'date' : newTrade.date, 
        'account' : newTrade.account,
        'classification' : 'trade',
        'blotter_id' : newTrade.id
    }
    newCashTrade = CashTrade(**cash_trade)
    
    session.add(newCashTrade)
    session.flush()
    session.commit()
    
    logger.info('Cash Trade replicated sucessfully')
    
    session.close()
    engine.dispose()
    
    logger.info('Session closed, engine disposed')
    
def copyPrevious() :
    DATABASE = {
       'drivername': 'sqlite',
       'database': 'portfolio/_data/Market.db'
    }
    engine = sa.create_engine(URL.create(**DATABASE))
    Base = orm.declarative_base()
    class History(Base) :
        __table__ = sa.Table('history', Base.metadata, autoload_with=engine)

    session = orm.Session(engine)
    lastHist = session.scalars(sa.select(History).order_by(History.Date.desc())).first()
    next_date = (lastHist.Date + CDay(1)).date()
    nextHist = History(Date=next_date)

    for col in lastHist.__table__.c :
        nextHist.__dict__[col.name] = lastHist.__dict__[col.name]
    
    nextHist.Date = next_date

    session.add(nextHist)
    session.flush()
    session.commit()
    
    session.close()
    engine.dispose()
    
    print('Previous Date copied')
    
yCodes = ['BMO.TO', 'CM.TO', 'ESPO', 'IGSB', 'IYF', 'JXI', 'RIGS', 'RY.TO',
          'SHY', 'SPY', 'VALE', 'BRL=X', 'CAD=X', 'CHF=X', 'EUR=X', 'GBP=X',
          'SPY230120P00370000', 'SPY230120P00380000', 'SPY230217C00410000',
          'SPY230217C00420000', 'SPY230217P00360000', 'SPY230217P00365000',
          'SPY230317C00410000', 'SPY230317C00415000', 'SPY230317C00420000',
          'SPY230317P00340000', 'SPY230317P00350000', 'SPY230317P00360000',
          'SPY230317P00370000', 'SPY230317P00380000', 'SPY230421P00350000',
          'SPY230616C00430000']

def updateYahooUpToYesterday() :
    DATABASE = {
       'drivername': 'sqlite',
       'database': 'portfolio/_data/Market.db'
    }

    engine = sa.create_engine(URL.create(**DATABASE))
    
    Base = orm.declarative_base()
    class History(Base) :
        __table__ = sa.Table('history', Base.metadata, autoload_with=engine)

    session = orm.Session(engine)
    lastHist = session.scalars(sa.select(History).order_by(History.Date.desc())).first()
    
    lastEmpty = (dt.now() - CDay(1)).date()
    if lastEmpty == lastHist.Date :
        return  'History Already updated'
    else :
        #Updating from Yahoo
        yHist = yf.download(yCodes, period='1mo', interval='1d')['Adj Close']
        yHist.index = yHist.index.map(lambda x: x.date())
        adjustYahooTickers = {
            'BMO.TO' : 'BMO',
            'CM.TO' : 'CM', 
            'RY.TO' : 'RY',
            'BRL=X' : 'BRL',
            'CAD=X' : 'CAD', 
            'EUR=X' : 'EUR',
            'GBP=X' : 'GBP',
            'CHF=X' : 'CHF'}
    
        dates = [x.date() for x in pd.date_range(lastHist.Date, lastEmpty, freq='B')][1:]
        for date_ in dates : 
            nextHist = History(Date=date_)
            prices = yHist.loc[date_].to_dict()
            prices['Date'] = date_
            for i in adjustYahooTickers :
                prices[adjustYahooTickers[i]] = prices.pop(i)
            for col in lastHist.__table__.c :
                if col.name in prices.keys() :
                    nextHist.__dict__[col.name] = prices[col.name]
                else :
                    nextHist.__dict__[col.name] = lastHist.__dict__[col.name]
            
            session.add(nextHist)
    
        session.commit()
        session.close()
        engine.dispose()
        return 'History Updated'
    
def addNewHistoryItem(tickers:list[str]) :
    DATABASE = {
       'drivername': 'sqlite',
       'database': 'portfolio/_data/Market.db'
    }
    engine = sa.create_engine(URL.create(**DATABASE))
    Base = orm.declarative_base()
    class History(Base) :
        __table__ = sa.Table('history', Base.metadata, autoload_with=engine)
    
    for ticker in new_tickers :
        engine.execute('ALTER TABLE history ADD COLUMN %s float' % (ticker))
        
    session = orm.Session(engine)
    histItems = session.scalars(sa.select(History)).all()
    start_dt = histItems[0].Date
    end_dt = histItems[-1].Date
    
    new_prices = yf.download(new_tickers, start=start_dt, end=end_dt, interval='1d')['Adj Close']
    new_prices.index = new_prices.index.map(lambda x:x.date())
    
    histItems = session.scalars(sa.select(History).where(History.Date.in_(new_prices.index))).all()
    
    if len(tickers) > 1 :
        for histItem in histItems :
            for ticker in new_tickers :
                setattr(histItem, ticker, new_prices.loc[histItem.Date, ticker])
    else :
        for histItem in histItems :
            setattr(histItem, new_tickers[0], new_prices.loc[histItem.Date])
    
    session.add_all(histItems)
    session.commit()
    session.close()
    engine.dispose()
    
    logger.info(f'Items {tickers} added to History')