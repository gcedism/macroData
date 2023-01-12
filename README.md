# <span style='color:DarkSlateGray'> Macro Data Analyses</span>
---
#### <span style='color:blue'> AVAILABLE DATA </span>

Total of 295 data points from 14 differenct sources using API form each one of them

SOURCES :
- Yahoo Finance
- BLS - Bureau of Labour Statistics
- FRED - St Louis FED
- US Census
- BEA - Bureau of Economic Analyses
- US FED
- Philly FED
- US Treasury Department
- ONS - Office for National Statistics (UK)
- Canada Central Bank
- Eurostat Data (Europe)
- Brazilian Central Bank
- INEGI - National Institute of Statistic and Geography (Mexico)
- Manual Data - Other manual data

Example : 

![data_available](https://github.com/gcedism/macroData/blob/main/_docs/data_available.png "data_available")


---
#### <span style='color:DarkSlateGray'> Usage </span>
Colect macro data from different sources to create analyses, charts and statisical modelling

1 - Load Data_specs.json with all data available in the macro

![data_spec](https://github.com/gcedism/macroData/blob/main/_docs/data_spec.png "data_spec")

2- Load Database with selected data

![macroDataLoad](https://github.com/gcedism/macroData/blob/main/_docs/macroDataLoad.png "macroDataLoad")


---
<span styles='color:red'> - API_KEYS need to be provided in the constants_private.py file </span>

---
## <span style='color:blue'> Analyses </span>

- Some analyses run as examples of how to extract data, generate charts and save it to files

### <span style='color:red'> US MACRO ANALYSES </span>

US Inflation Expectations

![usInfExp](https://github.com/gcedism/macroData/blob/main/_docs/usInfExp.png "usInfExp")

S&P500 vs US 10Y Real Rate

![snpXreal10](https://github.com/gcedism/macroData/blob/main/_docs/snpXreal10.png "snpXreal10")

US Housing

![usHousing](https://github.com/gcedism/macroData/blob/main/_docs/usHousing.png "usHousing")

US IG Spreads x MOVE Index

![igspreadXmove](https://github.com/gcedism/macroData/blob/main/_docs/igspreadXmove.png "igspreadXmove")


### <span style='color:DarkRed'> To Do </span>

- Some data still requires manual input since it's not automated from an official source. A csv file is provided in the folder that needs to be updated
