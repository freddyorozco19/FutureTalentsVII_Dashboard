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

#make it look nice from the start
st.set_page_config(layout='wide')

#####################################################################################################################################################

font_path = 'Resources/keymer-bold.otf'  # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop2 = font_manager.FontProperties(fname=font_path)

font_path2 = 'Resources/BasierCircle-Italic.ttf'  # Your font path goes here
font_manager.fontManager.addfont(font_path2)
prop3 = font_manager.FontProperties(fname=font_path2)

#####################################################################################################################################################

from streamlit_option_menu import option_menu

# 1. as sidebar menu
with st.sidebar:
    with open("Resources/logobk.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
            st.sidebar.markdown(
                f"""
                <div style="display:table;margin-top:-20%">
                    <img src="data:image/png;base64,{data}" width="200">
                </div>
                """,
                unsafe_allow_html=True,
            )
    selected = option_menu("", ["Rankings", 'Player Search'], 
        icons=['trophy', 'search'], default_index=1, styles={
            "nav-link": {"font-size": "15px"}})
    

# 2. horizontal menu
#selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#    icons=['house', 'cloud-upload', "list-task", 'gear'], 
#    menu_icon="cast", default_index=0, orientation="horizontal")
#selected2

# 3. CSS style definitions
#selected3 = option_menu(None, ["Home", "Upload",  "Tasks", 'Settings'], 
#    icons=['house', 'cloud-upload', "list-task", 'gear'], 
#    menu_icon="cast", default_index=0, orientation="horizontal",
#    styles={
#        "container": {"padding": "0!important", "background-color": "#fafafa"},
#        "icon": {"color": "orange", "font-size": "25px"}, 
#        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#        "nav-link-selected": {"background-color": "green"},
#    }
#)

# 4. Manual Item Selection
#if st.session_state.get('switch_button', False):
#    st.session_state['menu_option'] = (st.session_state.get('menu_option',0) + 1) % 4
#    manual_select = st.session_state['menu_option']
#else:
#    manual_select = None
    
#selected4 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#    icons=['house', 'cloud-upload', "list-task", 'gear'], 
#    orientation="horizontal", manual_select=manual_select, key='menu_4')
#st.button(f"Move to Next {st.session_state.get('menu_option',1)}", key='switch_button')
#selected4

# 5. Add on_change callback
#def on_change(key):
#    selection = st.session_state[key]
#    st.write(f"Selection changed to {selection}")
    
#selected5 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                        icons=['house', 'cloud-upload', "list-task", 'gear'],
#                        on_change=on_change, key='menu_5', orientation="horizontal")
#selected5
#Data
    df = pd.read_excel("MatchesData/matches.xlsx")
    event_counts = df.groupby(['Players', 'Team'])['Action'].value_counts().unstack(fill_value=0)
    columnsevents = event_counts.columns.tolist()
if selected == "Rankings":
    st.title("RANKINGS")
    st.markdown("""----""")
    st.write(event_counts)
    st.markdown("""----""")
    metricsearchbox01, metricsearchbox02, metricsearchbox03 = st.columns(3)
    with metricsearchbox01:
        #Team_Lst = df['Team'].drop_duplicates().tolist()
        Metric_Lst = columnsevents
        MetricSel = st.selectbox("Choose metric:", Metric_Lst)
        #event_counts = event_counts[event_counts[MetricSel]].reset_index(drop=True)
    with metricsearchbox02:
      Positions_List = ['DEF', 'MED' 'DEL']
      PositionsSel = st.selectbox("Choose position:", Positions_List)
    with metricsearchbox03:
      Player_Lst = df['Players'].drop_duplicates().tolist()
      PlayerSel = st.selectbox("Choose player:", Player_Lst)
      #df = df[df['Players'] == PlayerSel].reset_index(drop=True)
    fig, ax = mplt.subplots(figsize=(8, 8), dpi = 800)
    ax.axis("off")
    fig.patch.set_visible(False)
    players_teams = [f'{player} - {team}' for player, team in event_counts.index]
    ax.barh(players_teams, event_counts[MetricSel], color='blue', label='Pass')
    st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
if selected == "Player Search":
    
    #Data
    df = pd.read_excel("MatchesData/matches.xlsx")
    st.title("Search Player")

    df['FieldXfrom'] = (df['FieldXfrom']*105)/1
    df['FieldYfrom'] = (df['FieldYfrom']*68)/1
    df['FieldXto'] = (df['FieldXto']*105)/1
    df['FieldYto'] = (df['FieldYto']*68)/1

    teamsearchbox01, teamsearchbox02, teamsearchbox03 = st.columns(3)
    with teamsearchbox01:
      Team_Lst = df['Team'].drop_duplicates().tolist()
      TeamSel = st.selectbox("Choose team:", Team_Lst)
      df = df[df['Team'] == TeamSel].reset_index(drop=True)
    with teamsearchbox02:
      Positions_List = ['DEF', 'MED' 'DEL']
      PositionsSel = st.selectbox("Choose position:", Positions_List)
    with teamsearchbox03:
      Player_Lst = df['Players'].drop_duplicates().tolist()
      PlayerSel = st.selectbox("Choose player:", Player_Lst)
      df = df[df['Players'] == PlayerSel].reset_index(drop=True)
    st.markdown("""----""")
   
    #selbox01, selbox02, selbox03 = st.columns(3)
    #with selbox01:
    #  Lista_Partidos = ['Fecha 1', 'Fecha 2']
    #  st.selectbox("Choose matchday:", Lista_Partidos) 
    #with selbox02:
    #  Team_Lst = df['Team'].drop_duplicates().tolist()
    #  TeamSel = st.selectbox("Choose team:", Team_Lst)
    #  #df = df[df['Team'] == TeamSel].reset_index(drop=True)
    #with selbox03:
    #  Player_Lst = df['Players'].drop_duplicates().tolist()
    #  PlayerSel = st.selectbox("Choose player:", Player_Lst)
    #  #df = df[df['Players'] == PlayerSel].reset_index(drop=True)
    
    pltmain01, pltmain02 = st.columns(2)
    with pltmain01:
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
        ##ax29.annotate(s='', xy=(2, 5), xytext=(8, 5), arrowprops=dict(arrowstyle='<-', ls= '-', lw = 1, color = (1,1,1,0.5)))
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
        ###df = df[(df['EfectiveMinute'] >= EfectMinSel[0]) & (df['EfectiveMinute'] <= EfectMinSel[1])]
        dfKK = df
        ax.scatter(df['FieldXfrom'], df['FieldYfrom'], color = "#FF0046", edgecolors='w', s=30, zorder=2, alpha=0.2)
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
    with pltmain02:
        st.dataframe(df)
    st.markdown("""----""")
