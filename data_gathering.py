import logging
import fundamentus

import streamlit as st
import numpy as np
import pandas as pd
from pandas_datareader import data
from dmapi import DMAPI


@st.cache
def get_tickers():
    dm = DMAPI(token='9b6792598ede5d72caf26d497b1940c5')
    dm_json = dm.tickers()
    df = pd.DataFrame.from_dict(dm_json)
    return df


@st.cache
def get_companies():
    dm = DMAPI(token='9b6792598ede5d72caf26d497b1940c5')
    dm_json = dm.companies()
    df = pd.DataFrame.from_dict(dm_json)
    return df


@st.cache
def get_actives():
    logging.info('Get Actives')
    comps = get_companies()
    tickers = get_tickers()
    merged_inner = pd.merge(
        left=comps,
        right=tickers,
        left_on='slug',
        right_on='company_slug'
    )
    return merged_inner


@st.cache
def get_history(start_date, ticker_list):
    df = pd.DataFrame()
    for ticker in ticker_list:
        df[ticker] = data.DataReader(ticker, data_source='yahoo', start=start_date)['Close']
    df.dropna(inplace=True)
    return df

