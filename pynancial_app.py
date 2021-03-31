import SessionState
import streamlit as st
import streamlit.components.v1 as components

import numpy as np
import pandas as pd
import datetime

import plotly.express as px

from data_gathering import get_tickers
from data_gathering import get_companies
from data_gathering import get_actives
from data_gathering import get_history
from datetime import date

st.title('Pynancial APP')

# Get all tickers
df = get_actives()[['name', 'ticker']]

# Select start date
start_date = st.sidebar.date_input("Start date", date.today())
st.write('Começando do dia', start_date)


# Select companies by name
comp_names_options = st.sidebar.multiselect('Select tickers', df['name'].unique())
# st.write('You selected', tickers_options)

if comp_names_options:

    # Get tickers codes as list
    tickers_options = df[df['name'].isin(comp_names_options)]['ticker'].to_list()
    # Concat suffix for yahoo API
    tickers_options = [x + '.SA' for x in tickers_options]
    # st.write('Tickers', tickers_options)

    # Show selected companies data
    st.write('Selected companies', df[df['name'].isin(comp_names_options)].reset_index(drop=True))

    df = get_history(start_date, tickers_options)
    # st.write(df)
    # Grafico de linhas com o historico das acoes normalizado
    fig = px.line(title='Histórico do preco das ações')
    for col in df.columns:
        fig.add_scatter(x=df.index, y=df[col], name=col)
    # fig.show()
    st.plotly_chart(fig)
