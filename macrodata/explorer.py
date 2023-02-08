#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path
import pandas as pd
from datetime import date

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine.url import URL

from .logs import logHeader

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

class Explorer :
    
    countries = session.scalars(sa.select(Data.country.distinct())).all()
    asset_classes = session.scalars(sa.select(Data.asset_class.distinct())).all()
    tickers = session.scalars(sa.select(Data.id)).all()
    
    logger.debug('Class Initiated with countries, asset_classes and tickers')
    
    @classmethod
    def countryList(cls, countries:list[str]) -> dict[str] :
        items = session.scalars(sa.select(Data).where(Data.country.in_(countries))).all()
        result = {country: [item.id for item in items if item.country==country]
                  for country in countries}
        logger.debug(f'Retrieved data for {countries}')
        
        return result
    
    @classmethod
    def countryAssetList(cls, countries:list[str], asset_classes:list[str]) -> dict[str] :
        items = (session.scalars(sa.select(Data)
                                 .where(Data.country.in_(countries))
                                 .where(Data.asset_class.in_(asset_classes)))
                 .all())
        result = {country: {asset: [item.id for item in items
                                     if (item.country==country) & (item.asset_class==asset)]
                           for asset in asset_classes} for country in countries}
        
        logger.debug(f'Retrieved data for {asset_classes} in {countries}')
        
        return result
    
    @classmethod
    def sourceList(cls, sources:list[str]) -> dict[str] :
        items = (session.scalars(sa.select(Data)
                                 .where(Data.source.in_(sources)))
                 .all())
        result = {source: [item.id for item in items
                           if (item.source==source)]
                  for source in sources}
        
        logger.debug(f'Retrieved data for {sources}')
        
        return result
    
    @classmethod
    def listHistory(cls, tickers:list[str], start_dt:date, end_dt:date) -> pd.DataFrame :
        
        _tickers = ['index'] + tickers
        cols = [History.__dict__[x] for x in _tickers]
        items = (session.query(*cols)
                 .where(History.index >= start_dt)
                 .where(History.index <= end_dt)
                 .all())
        
        logger.debug(f''''
            Data for {tickers} between dates of {start_dt} and {end_dt}
            was retrieved
            ''')
        
        return pd.DataFrame([x for x in items]).set_index('index')
                
    
    
    
    
    
        
    