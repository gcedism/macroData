#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import pandas as pd
from pandas.tseries.offsets import CDay
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine.url import URL

from .logs import logHeader
from .clients import *

logger = logging.getLogger(__name__)
logger.debug(logHeader)

FOLDER = str(Path(__file__).parent)

DATABASE = {
    'drivername': 'sqlite',
    'database': FOLDER + '/_data/macroDatabase.db'
}
engine = sa.create_engine(URL.create(**DATABASE))
Base = orm.declarative_base()
    
class History(Base) :
    __table__ = sa.Table('monthly_history', Base.metadata, autoload_with=engine)
    
    def __repr__(self) :
        return f'History({self.index})'

class Data(Base) :
    __table__ = sa.Table('data_specs', Base.metadata, autoload_with=engine)
    
    def __repr__(self) :
        return f'Data({self.id} from {self.source})'
    
session = orm.Session(engine)

logger.debug('Session connected')

class Manager :
    
    lastDate = session.scalars(sa.select(History).order_by(History.index.desc())).first().index
    
    @classmethod
    def downloadFromSource(cls, source:str, tickers:list[str],
                          start_dt:date, end_dt:date, freq:str) -> pd.DataFrame :
        
        _data = getattr(globals()[source + 'Client'](tickers, start_dt, end_dt, freq), '_data')
        
        return _data
    
    @classmethod
    def updateFromSource(cls, source:str):
        # It works, but still have to check which data from source is actually
        # Not NA !
        
        items = session.scalars(sa.select(Data.id).where(Data.source == source)).all()
        if len(items) > 0 :
            cols = [History.index] + [col for col in History.__table__.c if col.name in items]
            stmt = (sa.select(*cols)
                .filter(History.__table__.c[items[0]] != None)
                .order_by(History.index.desc())
                .limit(1))
            results = engine.execute(stmt)
            lastHistorySource = results.first().index
        
            end_dt = dt.now().date() - CDay(1)
            start_dt = end_dt - td(days=180)
            freq = 'M'
            df = cls.downloadFromSource(source, items, start_dt, end_dt, freq)
            lastFromSource = df.index[-1]
            
            if lastFromSource <= lastHistorySource :
                logger.debug(f'History for {source} already updated upt to {lastHistorySource}')
                return f'Nothing'
            else :
                dfToUpdate = df.loc[(df.index > lastHistorySource) *
                                   (df.index <= cls.lastDate)]
                if not dfToUpdate.empty :
                    cls.updateData(dfToUpdate)
                    return 'Success'
                else :
                    logger.debut(f'Nothing to update')
                
                dfToAdd = df.loc[df.index > cls.lastDate]
                if not dfToAdd.empty :
                    print('To do : add items')
                else :
                    logger.debut(f'Nothing to add')
                    
                return f'All handled'
        else :
            return f'No items four source : {source}'
        
    @classmethod
    def updateData(cls, df:pd.DataFrame) :
        #Assumes that df is not Empty :
        #Maybe Todo : assert that
        items = session.scalars(sa.select(History).where(History.index.in_(df.index))).all()
        for item in items :
            for col in df.columns :
                setattr(item, col, df.loc[item.index, col])
        
        session.commit()
        logger.debug(f'Items on {[x for x in df.columns]} for dates {[x for x in df.index]} updated')
    