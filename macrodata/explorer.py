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
    sources = session.scalars(sa.select(Data.source.distinct())).all()
    
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
    def countrySubAssetList(cls, countries:list[str], sub_asset_classes:list[str]) -> dict[str] :
        items = (session.scalars(sa.select(Data)
                                 .where(Data.country.in_(countries))
                                 .where(Data.sub_asset_class.in_(sub_asset_classes)))
                 .all())
        result = {country: {asset: [item.id for item in items
                                     if (item.country==country) & (item.sub_asset_class==asset)]
                           for asset in sub_asset_classes} for country in countries}
        
        logger.debug(f'Retrieved data for {sub_asset_classes} in {countries}')
        
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
    
    @classmethod
    def separateSources(cls, tickers:list[str]) -> dict[str] :
        items = (session.scalars(sa.select(Data)
                                 .where(Data.id.in_(tickers)))
               .all())
        
        results = {source:[item.id for item in items if item.source == source]
                   for source in cls.sources}
        
        logger.debug(f'Separated {tickers} in respective sources')
        
        return results
    
    @classmethod
    def desc(cls, tickers:list[str], start_dt:date, end_dt:date) -> pd.DataFrame :
        """
        Gives a quick summary of the data collected 
        """
        df_items = cls.listHistory(tickers, start_dt, end_dt)
        
        real_data = df_items.dropna()
        print(f'Total non NA data : {real_data.shape[0]}')
        real_start = real_data.index[0]
        real_end = real_data.index[-1]
        print(f"From {format(real_start, '%Y-%m-%d')} to {format(real_end, '%Y-%m-%d')}")
        nMonths = (real_end.month - real_start.month) + (real_end.year - real_start.year) * 12 + 1
        print(f'Theorical number of months : {nMonths}')                                                
        
        items = cls.separateSources(tickers)
        items_dict = {}
        for k, v in items.items() :
            if len(v) > 0:
                for i in v :
                    last_date = df_items.loc[:, i].dropna().index[-1]
                    last_value = df_items.loc[:, i].dropna().iloc[-1]
                    last_nvalue = df_items.loc[:, i].notna().sum()
                    items_dict[(k, i)] = [last_date, last_value, last_nvalue]
        
        return pd.DataFrame(items_dict, index=['last Date', 'last value', 'n of values']).T
        
    
    
    
        
    