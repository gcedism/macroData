from datetime import date 
from datetime import timedelta as td
from pandas.tseries.offsets import CDay

ticker_map = {
    'uk_cpi_health': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 17,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_furn': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 18,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_housing': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 19,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_clothing': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 21,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_alcohol': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 23,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_misc': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 24,
        'dataGroup' : 'inflation'
    },    
    'uk_cpi_food': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 25,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_hotels': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 26,
        'dataGroup' : 'inflation'
    },
    'uk_cpi': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 27,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_education': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 28,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_recreation': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 29,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_communication': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 31,
        'header': [],
        'col' : 30,
        'dataGroup' : 'inflation'
    },
    'uk_cpi_transport': {
        'url': 'uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.xlsx',
        'sheet_name': 'data',
        'skiprows': 7,
        'header': [],
        'col' : 31,
        'dataGroup' : 'inflation'
    },
    'uk_retail_sales_sa': {
        'url': 'uri=/businessindustryandtrade/retailindustry/datasets/retailsalesindexreferencetables/current/mainreferencetables.xlsx',
        'sheet_name': 'KPSA',
        'skiprows': 8,
        'header': [],
        'col' : 1,
        'dataGroup' : 'retail_sales'
    },
    'uk_retail_sales_exfuel_sa': {
        'url': 'uri=/businessindustryandtrade/retailindustry/datasets/retailsalesindexreferencetables/current/mainreferencetables.xlsx',
        'sheet_name': 'KPSA',
        'skiprows': 8,
        'header': [],
        'col' : 2,
        'dataGroup' : 'retail_sales'
    },
    'uk_retail_sales_food_sa': {
        'url': 'uri=/businessindustryandtrade/retailindustry/datasets/retailsalesindexreferencetables/current/mainreferencetables.xlsx',
        'sheet_name': 'KPSA',
        'skiprows': 8,
        'header': [],
        'col' : 3,
        'dataGroup' : 'retail_sales'
    },
    'uk_retail_sales_exfood_sa': {
        'url': 'uri=/businessindustryandtrade/retailindustry/datasets/retailsalesindexreferencetables/current/mainreferencetables.xlsx',
        'sheet_name': 'KPSA',
        'skiprows': 8,
        'header': [],
        'col' : 4,
        'usecols': [0, 1, 2, 3, 4],
        'dataGroup' : 'retail_sales'
    },
    'uk_industrial_prod': {
        'url': 'uri=/economy/grossdomesticproductgdp/datasets/gdpmonthlyestimateuktimeseriesdataset/current/mgdp.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 22,
        'dataGroup' : 'production'
    },
    'uk_gdp': {
        'url': 'uri=/economy/grossdomesticproductgdp/datasets/gdpmonthlyestimateuktimeseriesdataset/current/mgdp.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 52,
        'dataGroup' : 'production'
    },
    'uk_manuf_prod': {
        'url': 'uri=/economy/grossdomesticproductgdp/datasets/gdpmonthlyestimateuktimeseriesdataset/current/mgdp.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 69,
        'dataGroup' : 'production'
    },
    'uk_imports_fuel': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 103,
        'dataGroup' : 'trade'
    },
    'uk_exports_food': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 224,
        'dataGroup' : 'trade'
    },
    'uk_exports_beverages_tobacco': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 248,
        'dataGroup' : 'trade'
    },
    'uk_exports_materials': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 300,
        'dataGroup' : 'trade'
    },
    'uk_trade_balance': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 314,
        'dataGroup' : 'trade'
    },
    'uk_exports_animal_vegetable_oil': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 348,
        'dataGroup' : 'trade'
    },
    'uk_imports_beverages_tobacco': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 369,
        'dataGroup' : 'trade'
    },
    'uk_imports_food': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 379,
        'dataGroup' : 'trade'
    },
    'uk_exports_machines': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 393,
        'dataGroup' : 'trade'
    },
    'uk_exports_manufactures': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 406,
        'dataGroup' : 'trade'
    },
    'uk_exports_chemicals': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 419,
        'dataGroup' : 'trade'
    },
    'uk_exports_fuel': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 522,
        'dataGroup' : 'trade'
    },
    'uk_imports_chemicals': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 612,
        'dataGroup' : 'trade'
    },
    'uk_imports_animal_vegetable_oil': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 755,
        'dataGroup' : 'trade'
    },
    'uk_imports_manufactures': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 760,
        'dataGroup' : 'trade'
    },
    'uk_imports_machines': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 769,
        'dataGroup' : 'trade'
    },
    'uk_imports_materials': {
        'url': 'uri=/economy/nationalaccounts/balanceofpayments/datasets/tradeingoodsmretsallbopeu2013timeseriesspreadsheet/current/mret.xlsx',
        'sheet_name': 'data',
        'header': [0],
        'skiprows': 7,
        'col' : 988,
        'dataGroup' : 'trade'
    }
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
