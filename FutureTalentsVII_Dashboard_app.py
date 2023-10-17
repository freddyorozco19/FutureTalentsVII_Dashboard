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
    selected = option_menu("", ["Rankings", "Player Search", "Comparison"], 
        icons=['trophy', 'search', 'server'], default_index=1, styles={
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
        PositionsSel = st.selectbox("Choose index:", Positions_List)
    with metricsearchbox03:
      Player_Lst = df['Players'].drop_duplicates().tolist()
      PlayerSel = st.selectbox("Choose range:", Player_Lst)
      #df = df[df['Players'] == PlayerSel].reset_index(drop=True)
    p01, p02 = st.columns(2)
    with p01:
        fig, ax = mplt.subplots(figsize=(8, 8), dpi = 800)
        ax.axis("off")
        fig.patch.set_visible(False)
        players_teams = [f'{player} - {team}' for player, team in event_counts.index]
        #events = event_counts[MetricSel].head(-5)
        event_counts = event_counts.sort_values(by=MetricSel, axis=0, ascending=True)
        #event_counts = event_counts.head(10)
        ax.barh(players_teams, event_counts[MetricSel], color="#FF0050")
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
    with p02:
        st.write(event_counts[MetricSel])
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
    st.title(PlayerSel)
    st.subtitle(TeamSel)
    st.markdown("""----""")
    st.title("ACTIONS")
    with st.form(key='formpltev'):
        pltev01, pltev02, pltev03 = st.columns(3)
        with pltev01:
            Eventlst = ['Acciones', 'Pases', 'Remates', 'Regates', 'Recuperaciones']
            EventlstSel = st.selectbox('Seleccionar evento:', Eventlst)
            #st.dataframe(dfDOWN)
    #with pltev02:
        #Typelst = ['Mapa de Acciones', 'Territorio de Acciones', 'Mapa de Calor Acciones - JdP', 'Mapa de Calor Acciones - Bins']
        #st.selectbox('Seleccionar tipo gráfico:', Typelst)
        with pltev02:
            LstTeam = df['Team'].drop_duplicates()
            LstTeamsel = st.selectbox('Seleccionar equipo:', LstTeam)
            #df = df[df['Team'] == LstTeamsel].reset_index(drop=True)
            #st.dataframe(dfDOWN)
        with pltev03:
            LstPlayer = df['Players'].drop_duplicates()
            LstPlayer = LstPlayer.tolist()
            PlayerPltSel = st.selectbox('Seleccionar jugador:', LstPlayer)
            #df = df[df['Players'] == PlayerPltSel].reset_index(drop=True)
            #st.dataframe(dfDOWN)
        submit_button_pltev = st.form_submit_button(label='Aceptar')
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
    if EventlstSel == 'Acciones':     
        pltmnop01, pltmnop02, pltmnop03 = st.columns(3)
        with pltmnop01:
            OptionPlot = ['Territory Actions', 'Heatmap - Zones', 'Heatmap - Gaussian', 'Heatmap - Kernel']
            OptionPlotSel = st.selectbox('Seleccionar tipo gráfico:', OptionPlot)
        with pltmnop02:
            #EfectMinSel = st.slider('Seleccionar rango de partido:', 0, MaxAddMin, (0, MaxAddMin))
            EfectMinSel = st.slider('Seleccionar rango de partido:', 0, 90, (0, 90))
        with pltmnop03:
            ColorOptionSel = st.color_picker('Selecciona color:', '#FF0046')
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
        df = df.rename(columns={'FieldXfrom': 'X1',
                                'FieldYfrom': 'Y1',
                                'FieldXto': 'X2',
                                'FieldYto': 'Y2'})
        ##st.write(df)
        ##ax.scatter(df['FieldXfrom'], df['FieldYfrom'], color = "#FF0046", edgecolors='w', s=30, zorder=2, alpha=0.2)
        ##st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
        if OptionPlotSel == 'Territory Actions': 
                
                ##df = df.drop_duplicates(subset=['X1', 'Y1', 'X2', 'Y2'], keep='last')
                ##dfKKcleaned = df
                
                ##df = df[df['Event'] != 'Assists'].reset_index(drop=True)
                dfKKcleaned = df
                scaler  = StandardScaler()
                
                
                defpoints1 = df[['X1', 'Y1']].values
                defpoints2 = scaler.fit_transform(defpoints1)
                df2 = pd.DataFrame(defpoints2, columns = ['Xstd', 'Ystd'])
                df3 = pd.concat([df, df2], axis=1)
                df5=df3
                df3 = df3[df3['Xstd'] <= 1]
                df3 = df3[df3['Xstd'] >= -1]
                df3 = df3[df3['Ystd'] <= 1]
                df3 = df3[df3['Ystd'] >= -1].reset_index()
                df9 = df
                df = df3
                defpoints = df[['X1', 'Y1']].values
                #st.write(defpoints)

                hull = ConvexHull(df[['X1','Y1']])        
                ax.scatter(df9['X1'], df9['Y1'], color = ColorOptionSel, edgecolors='w', s=30, zorder=2, alpha=0.2)
                #Loop through each of the hull's simplices
                for simplex in hull.simplices:
                    #Draw a black line between each
                    ax.plot(defpoints[simplex, 0], defpoints[simplex, 1], '#BABABA', lw=2, zorder = 1, ls='--')
                ax.fill(defpoints[hull.vertices,0], defpoints[hull.vertices,1], ColorOptionSel, alpha=0.7)
                meanposx = df9['X1'].mean()
                meanposy = df9['Y1'].mean()
                ax.scatter(meanposx, meanposy, s=1000, color="w", edgecolors=ColorOptionSel, lw=2.5, zorder=25, alpha=0.95)
                names = PlayerPltSel.split()
                iniciales = ""
                for name in names:
                   iniciales += name[0] 
                #names_iniciales = names_iniciales.squeeze().tolist()
                ax.text(meanposx, meanposy, iniciales, color='k', fontproperties=prop2, fontsize=13, zorder=34, ha='center', va='center')
                ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfKKcleaned)) + " TOQUES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                #Adding title
                ax9 = fig.add_axes([0.17,0.16,0.20,0.07])
                ax9.axis("off")
                ax9.set_xlim(0,10)
                ax9.set_ylim(0,10)
                ax9.scatter(2, 5, s=120, color=ColorOptionSel, edgecolors='#FFFFFF', lw=1)
                ax9.text(2, -0.5, 'ACCIONES \nREALIZADAS', fontproperties=prop2, fontsize=9, ha='center', va='center', c='w')
                ax9.scatter(8, 5, s=320, color=ColorOptionSel, edgecolors='#FFFFFF', lw=1, ls='--', marker='h')
                ax9.text(8, -0.5, 'TERRITORIO\nRECURRENTE', fontproperties=prop2, fontsize=9, ha='center', va='center', c='w')
                st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
        elif OptionPlotSel == 'Heatmap - Zones':

                df = df[df['Event'] != 'Assists'].reset_index(drop=True)
                dfKKcleaned = df
                # Definir los colores base con transparencias diferentes
                red = [0.0705882352941176, 0.0705882352941176, 0.0784313725490196, 0]   # 121214
                green = [0.6, 0.1098039215686275, 0.2431372549019608, 0.6]   # 991C3E
                blue = [1, 0, 0.2745098039215686, 0.8]   # FF0046
                # Crear una lista de los colores y las posiciones en el colormap
                colors = [red, green, blue]
                positions = [0, 0.5, 1]
                # Crear el colormap continuo con transparencias
                cmaps = LinearSegmentedColormap.from_list('my_colormap', colors, N=256)
                path_eff = [path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()]
                bin_statistic = pitch.bin_statistic_positional(df.X1, df.Y1, statistic='count', positional='full', normalize=True)
                pitch.heatmap_positional(bin_statistic, ax=ax, cmap=cmaps, edgecolors='#524F50', linewidth=1)
                pitch.scatter(df.X1, df.Y1, c='w', s=15, alpha=0.02, ax=ax)
                labels = pitch.label_heatmap(bin_statistic, color='#f4edf0', fontsize=14, fontproperties=prop2, ax=ax, ha='center', va='center', str_format='{:.0%}', path_effects=path_eff)
                ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfKKcleaned)) + " TOQUES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                ax9 = fig.add_axes([0.14,0.15,0.20,0.07])
                ax9.scatter(6.75,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=1.0)
                ax9.scatter(5.00,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.6)
                ax9.scatter(3.25,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.2)
                ax9.text(5, 0, '-  ACCIONES REALIZADAS  +', c='w', fontproperties=prop2, fontsize=9, ha='center')
                ax9.axis("off")
                ax9.set_xlim(0,10)
                ax9.set_ylim(0,10)

                st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
        elif OptionPlotSel == 'Heatmap - Gaussian':
                df = df[df['Event'] != 'Assists'].reset_index(drop=True)
                dfKKcleaned = df
                # Definir los colores base con transparencias diferentes
                red = [0.0705882352941176, 0.0705882352941176, 0.0784313725490196, 0.3]   # Rojo opaco
                green = [1, 0, 0.2745098039215686, 1]   # Verde semitransparente
                blue = [1, 0.5490196078431373, 0.6745098039215686, 1]   # Azul semitransparente    
                # Crear una lista de los colores y las posiciones en el colormap
                colors = [red, green, blue]
                positions = [0, 0.5, 1]
                # Crear el colormap continuo con transparencias
                cmaps = LinearSegmentedColormap.from_list('my_colormap', colors, N=256)
                bin_statistic = pitch.bin_statistic(df['X1'], df['Y1'], statistic='count', bins=(120, 80))
                bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 4)
                pcm = pitch.heatmap(bin_statistic, ax=ax, cmap=cmaps, edgecolors=(0,0,0,0), zorder=-2)    
                ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfKKcleaned)) + " TOQUES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                ax9 = fig.add_axes([0.14,0.15,0.20,0.07])
                ax9.scatter(6.75,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=1.0)
                ax9.scatter(5.00,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.6)
                ax9.scatter(3.25,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.2)
                ax9.text(5, 0, '-  ACCIONES REALIZADAS  +', c='w', fontproperties=prop2, fontsize=9, ha='center')
                ax9.axis("off")
                ax9.set_xlim(0,10)
                ax9.set_ylim(0,10)
                st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
        elif OptionPlotSel == 'Heatmap - Kernel':
                df = df[df['Event'] != 'Assists'].reset_index(drop=True)
                dfKKcleaned = df
                # Definir los colores base con transparencias diferentes
                red = [0.0705882352941176, 0.0705882352941176, 0.0784313725490196, 0.3]   # Rojo opaco
                green = [1, 0, 0.2745098039215686, 1]   # Verde semitransparente
                blue = [1, 0.5490196078431373, 0.6745098039215686, 1]   # Azul semitransparente    
                # Crear una lista de los colores y las posiciones en el colormap
                colors = [red, green, blue]
                positions = [0, 0.5, 1]
                # Crear el colormap continuo con transparencias
                cmaps = LinearSegmentedColormap.from_list('my_colormap', colors, N=256)
                #bin_statistic = pitch.bin_statistic(df['X1'], df['Y1'], statistic='count', bins=(120, 80))
                #bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 4)
                kde = pitch.kdeplot(dfKKcleaned.X1, dfKKcleaned.Y1, ax=ax,
                    # fill using 100 levels so it looks smooth
                    fill=True, levels=500,
                    # shade the lowest area so it looks smooth
                    # so even if there are no events it gets some color
                    thresh=0,
                    cut=1, alpha=0.7, zorder=-2,  # extended the cut so it reaches the bottom edge
                    cmap=cmaps)

                
                #pcm = pitch.heatmap(bin_statistic, ax=ax, cmap=cmaps, edgecolors=(0,0,0,0), zorder=-2)    
                ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfKKcleaned)) + " TOQUES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                ax9 = fig.add_axes([0.14,0.15,0.20,0.07])
                ax9.scatter(6.75,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=1.0)
                ax9.scatter(5.00,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.6)
                ax9.scatter(3.25,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.2)
                ax9.text(5, 0, '-  ACCIONES REALIZADAS  +', c='w', fontproperties=prop2, fontsize=9, ha='center')
                ax9.axis("off")
                ax9.set_xlim(0,10)
                ax9.set_ylim(0,10)
                st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
    with pltmain02:
        st.dataframe(df)
    st.markdown("""----""")
    metricplayerbox01, metricplayerbox02, metricplayerbox03 = st.columns(3)
    with metricplayerbox01:
        #Team_Lst = df['Team'].drop_duplicates().tolist()
        Metric_Lst = columnsevents
        MetricSel = st.selectbox("Choose metric:", Metric_Lst)
    st.markdown("""----""")
