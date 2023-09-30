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

#make it look nice from the start
st.set_page_config(layout='wide')

Lista_Partidos = ['Fecha 1', 'Fecha 2']
st.selectbox("Seleccione partido:", Lista_Partidos) 
