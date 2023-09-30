# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 20:46:32 2023

@author: Freddy J. Orozco R.
"""

import streamlit as st
import hydralit_components as hc
import datetime
import base64
import pandas as pd
from io import BytesIO
import pandas as pd
import numpy as np


#Data
df = pd.read_excel("MatchesData/matches.xlsx")

#make it look nice from the start
st.set_page_config(layout='wide')

selbox01, selbox02, selbox03 = st.columns(3)

with selbox01:
  Lista_Partidos = ['Fecha 1', 'Fecha 2']
  st.selectbox("Choose matchday:", Lista_Partidos) 
with selbox02:
  Player_Lst = df['Players'].drop_duplicates()
  #Player_Lst = ['Player 1', 'Player 2', '9-Ben Youssouf Kamate']
  st.selectbox("Choose player:", Player_Lst)
