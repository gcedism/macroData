import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from numpy import log
import macrodata as md
from macrodata import create_connection, countryList, listHistory
from appComponents import get_us_inflation_chart, get_us_inflation_breakdown, get_us_inflation_expectations

from datetime import date

start_dt = date(2015, 1, 1)
end_dt = date(2023, 4, 1)

History, Data, session = create_connection()

tab1, tab2, tab3 = st.tabs(['Chart', 'Fixed Analyses', 'Others'])
with tab1 :
    with st.container() :
        cols1 = st.columns(2)
        with cols1[0] :
            countries_list = md.Explorer.countries
            countries = st.multiselect('Countries :', countries_list, default='US', key='m1')

            items_list = countryList(countries, session, Data)
            items = st.multiselect('Items :', items_list, default=items_list[0], key='m2')

            history = listHistory(items, start_dt, end_dt, session, History)
            
            trans = st.radio('Transformation : ', ('None', 'MoM', 'YoY'), index=0, key='r1')
            if trans == 'MoM' :
                history = history.apply(log).diff().dropna()
                perc = True
            elif trans == 'YoY' :
                history = history.apply(log).diff(12).dropna()
                perc = True
            else : 
                perc = False
                
        with cols1[1] :
            countries_list = md.Explorer.countries
            countries = st.multiselect('Countries :', countries_list, default='US', key='m3')

            items_list = countryList(countries, session, Data)
            items = st.multiselect('Items :', items_list, default=items_list[0], key='m4')

            history2 = listHistory(items, start_dt, end_dt, session, History)
         
            with st.container() :
                cols2 = st.columns(2)
                with cols2[0] :
                    trans = st.radio('Transformation : ', ('None', 'MoM', 'YoY'), index=0, key='r2')
                    if trans == 'MoM' :
                        history = history.apply(log).diff().dropna()
                        perc = True
                    elif trans == 'YoY' :
                        history = history.apply(log).diff(12).dropna()
                        perc = True
                    else : 
                        perc = False
                with cols2[1] :
                    axis = st.radio('Axis 2 : ', ('Yes', 'No'))
                    
    
    f, ax = plt.subplots()

    ax.spines[['top', 'right']].set_visible(False)
    if perc :
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals = 1))
        (history*100).plot(ax=ax)
    else :
        history.plot(ax=ax)
    ax.grid(alpha = 0.5, ls = '--')
    ax.legend(loc = 'lower left')
    
    void = plt.xticks(fontsize=12)
    void = plt.yticks(fontsize=12)

    void = ax.text(0, -0.1, 'Source : ',
              fontstyle = 'italic',
              transform = ax.transAxes)

    st.pyplot(f)
    
    
with tab2 :
    tab21, tab22, tab23 = st.tabs(['US Macro', 'UK Macro', 'Others'])
    
    with tab21 : 
        st.pyplot(get_us_inflation_chart(start_dt, end_dt, session, History))
        st.pyplot(get_us_inflation_breakdown(start_dt, end_dt, session, History, Data))
        st.pyplot(get_us_inflation_expectations(start_dt, end_dt, session, History))