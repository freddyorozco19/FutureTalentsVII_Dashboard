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
#import matplotlib.pyplot as plt
import matplotlib.pyplot as mplt
import matplotlib.font_manager as font_manager
import mplsoccer
from mplsoccer import Pitch, VerticalPitch, FontManager
import sklearn
from sklearn.preprocessing import StandardScaler
from scipy.spatial import ConvexHull
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
from scipy.ndimage import gaussian_filter
import seaborn as sns
from matplotlib import colors as mcolors
import requests
from PIL import Image
from matplotlib.patches import Rectangle

#####################################################################################################################################################

font_path = 'Resources/keymer-bold.otf'  # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop2 = font_manager.FontProperties(fname=font_path)

font_path2 = 'Resources/BasierCircle-Italic.ttf'  # Your font path goes here
font_manager.fontManager.addfont(font_path2)
prop3 = font_manager.FontProperties(fname=font_path2)

#####################################################################################################################################################

#Data
df = pd.read_excel("MatchesData/matches.xlsx")
df['FieldXfrom'] = (df['FieldXfrom']*105)/1
df['FieldYfrom'] = (df['FieldYfrom']*68)/1
df['FieldXto'] = (df['FieldXto']*105)/1
df['FieldYto'] = (df['FieldYto']*68)/1


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



fig, ax = mplt.subplots(figsize=(8, 8), dpi = 800)
ax.axis("off")
fig.patch.set_visible(False)
pitch = Pitch(pitch_color='None', pitch_type='custom', line_zorder=1, linewidth=0.5, goal_type='box', pitch_length=105, pitch_width=68)
pitch.draw(ax=ax)
#Adding directon arrow
ax29 = fig.add_axes([0.368,0.22,0.3,0.05])
ax29.axis("off")
ax29.set_xlim(0,10)
ax29.set_ylim(0,10)
ax29.annotate('', xy=(2, 6), xytext=(8, 6), arrowprops=dict(arrowstyle='<-', ls= '-', lw = 1, color = (1,1,1,0.5)))
#ax29.annotate(s='', xy=(2, 5), xytext=(8, 5), arrowprops=dict(arrowstyle='<-', ls= '-', lw = 1, color = (1,1,1,0.5)))
ax29.text(5, 2, 'Dirección campo de juego', fontproperties=prop3, c=(1,1,1,0.5), fontsize=10, ha='center')
#Adding winstats logo
ax53 = fig.add_axes([0.82, 0.14, 0.05, 0.05])
url53 = "https://i.postimg.cc/R0QjGByL/sZggzUM.png"
response = requests.get(url53)
img = Image.open(BytesIO(response.content))
ax53.imshow(img)
ax53.axis("off")
ax53.set_facecolor("#000")
#st.dataframe(dfDOWN)
#df = df[(df['EfectiveMinute'] >= EfectMinSel[0]) & (df['EfectiveMinute'] <= EfectMinSel[1])]
dfKK = df

ax.scatter(df['FieldXfrom'], df['FieldYfrom'], color = "#FF0046", edgecolors='w', s=30, zorder=2, alpha=0.2)
st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
