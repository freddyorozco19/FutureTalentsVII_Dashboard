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
from streamlit_option_menu import option_menu

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

hex_list2 = ['#121214', '#D81149', '#FF0050']
#hex_list = ['#121214', '#112F66', '#004DDD']B91845
hex_list4 = ['#5A9212', '#70BD0C', '#83E604']
#hex_list1 = ['#121214', '#854600', '#C36700']
hex_list = ['#121214', '#545454', '#9F9F9F']
hex_list1 = ['#121214', '#695E00', '#C7B200']
#hex_list2 = ['#121214', '#112F66', '#004DDD']
#hex_list = ['#121214', '#11834C', '#00D570']
cmap = sns.cubehelix_palette(start=.25, rot=-.3, light=1, reverse=True, as_cmap=True)
cmap2 = sns.diverging_palette(250, 344, as_cmap=True, center="dark")
cmap3 = sns.color_palette("dark:#FF0046", as_cmap=True)


def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#") # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v/256 for v in value]


def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list. 
        
        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.
        
        Returns
        ----------
        colour map'''
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0,1,len(rgb_list)))
        
    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp

def colorlist(color1, color2, num):
    """Generate list of num colors blending from color1 to color2"""
    result = [np.array(color1), np.array(color2)]
    while len(result) < num:
        temp = [result[0]]
        for i in range(len(result)-1):
            temp.append(np.sqrt((result[i]**2+result[i+1]**2)/2))
            temp.append(result[i+1])
        result = temp
    indices = np.linspace(0, len(result)-1, num).round().astype(int)
    return [result[i] for i in indices] 
    
#####################################################################################################################################################
#####################################################################################################################################################

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

###Data
##df = pd.read_excel("MatchesData/matches.xlsx")
df = pd.read_excel("MatchesData/all_matches_prueba.xlsx")
df['Index'] = df['Index'].fillna("")
df['Event'] = df['Action'] + ' - ' + df['Index']

event_counts = df.groupby(['Players', 'Team'])['Event'].value_counts().unstack(fill_value=0)
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
        #ax.axis("off")
        fig.patch.set_visible(False)
        event_counts = event_counts.sort_values(by=[MetricSel], ascending=True)
        players_teams = [f'{player} - {team}' for player, team in event_counts[-10:].index]
        #events = event_counts[MetricSel].head(-5)
        
        ##st.write(event_counts.columns)
        ##st.write(players_teams)
        #event_counts = event_counts.head(10)
        colors = colorlist((1, 0, 0.3137254901960784, 0), (1, 0, 0.3137254901960784, 1), 10)
        #PLY = event_counts['Players'].tail(10).str.upper()
        Z = event_counts[MetricSel].tail(10)
        ax.barh(players_teams, Z, edgecolor=(1,1,1,0.5), lw = 1, color=colors)
        mplt.setp(ax.get_yticklabels(), fontproperties=prop2, fontsize=18, color='#FFF')
        mplt.setp(ax.get_xticklabels(), fontproperties=prop2, fontsize=20, color=(1,1,1,1))
        mplt.xlabel(MetricSel, color = 'w', fontproperties=prop2, fontsize=15, labelpad=20)
        #ax.set_xticks([0, 5, 10])
        #ax.set_xlim(0, 18)
        ax.tick_params(axis='y', which='major', pad=15)
        spines = ['top','bottom','left','right']
        for x in spines:
            if x in spines:
                ax.spines[x].set_visible(False)
        st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
    with p02:
        st.write(event_counts[MetricSel][-10:])
if selected == "Player Search":
    ###Data
    ##df = pd.read_excel("MatchesData/matches.xlsx")
    df = pd.read_excel("MatchesData/all_matches_16102023_215800.xlsx")
    st.title("Search Player")
    
    #df['FieldXfrom'] = (df['FieldXfrom']*105)/1
    #df['FieldYfrom'] = (df['FieldYfrom']*68)/1
    #df['FieldXto'] = (df['FieldXto']*105)/1
    #df['FieldYto'] = (df['FieldYto']*68)/1

    df['X1'] = (df['X1']*105)/1
    df['Y1'] = (df['Y1']*68)/1
    df['X2'] = (df['X2']*105)/1
    df['Y2'] = (df['Y2']*68)/1
    ###Convert for left attack-side
    for index, row in df.iterrows():
        if row['Atack side'] == 'Left':
            df.at[index, 'X1'] = 105 - row['X1']
            df.at[index, 'Y1'] = 68 - row['Y1']
            df.at[index, 'X2'] = 105 - row['X2']
            df.at[index, 'Y2'] = 68 - row['Y2']

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
    st.markdown("<style> div { text-align: left } </style>", unsafe_allow_html=True)
    st.header(PlayerSel)
    st.subheader(TeamSel)
    
    css='''
    [data-testid="metric-container"] {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] label {
        width: fit-content;
        margin: auto;
    }
    '''
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
    st.markdown("""----""")
    st.markdown("<style> div { text-align: center } </style>", unsafe_allow_html=True)
    st.title("ACTIONS")
    with st.form(key='formpltev'):
        pltev01, pltev02, pltev03 = st.columns(3)
        with pltev01:
            Eventlst = ['Actions', 'Passes', 'Shots', 'Dribbles', 'Recoveries']
            EventlstSel = st.selectbox('Choose metric:', Eventlst)
            #st.dataframe(dfDOWN)
    #with pltev02:
        #Typelst = ['Mapa de Acciones', 'Territorio de Acciones', 'Mapa de Calor Acciones - JdP', 'Mapa de Calor Acciones - Bins']
        #st.selectbox('Seleccionar tipo gráfico:', Typelst)
        with pltev02:
            LstTeam = df['Team'].drop_duplicates()
            LstTeamsel = st.selectbox('Choose team:', LstTeam)
            #df = df[df['Team'] == LstTeamsel].reset_index(drop=True)
            #st.dataframe(dfDOWN)
        with pltev03:
            LstPlayer = df['Players'].drop_duplicates()
            LstPlayer = LstPlayer.tolist()
            PlayerPltSel = st.selectbox('Choose player:', LstPlayer)
            #df = df[df['Players'] == PlayerPltSel].reset_index(drop=True)
            #st.dataframe(dfDOWN)
        submit_button_pltev = st.form_submit_button(label='OK')
    
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
    ##df = df.rename(columns={'FieldXfrom': 'X1',
    ##                                'FieldYfrom': 'Y1',
    ##                                'FieldXto': 'X2',
    ##                                'FieldYto': 'Y2'})
    if EventlstSel == 'Actions':     
        pltmnop01, pltmnop02, pltmnop03 = st.columns(3)
        with pltmnop01:
            OptionPlot = ['Territory Actions', 'Heatmap - Zones', 'Heatmap - Gaussian', 'Heatmap - Kernel']
            OptionPlotSel = st.selectbox('Choose viz:', OptionPlot)
        with pltmnop02:
            #EfectMinSel = st.slider('Seleccionar rango de partido:', 0, MaxAddMin, (0, MaxAddMin))
            EfectMinSel = st.slider('Seleccionar rango de partido:', 0, 90, (0, 90))
        with pltmnop03:
            ColorOptionSel = st.color_picker('Choose color:', '#FF0046')
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
            ax29.text(5, 2, 'Attack Direction', fontproperties=prop3, c=(1,1,1,0.5), fontsize=10, ha='center')
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
                    ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfKKcleaned)) + " TOUCHES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                    #Adding title
                    ax9 = fig.add_axes([0.17,0.16,0.20,0.07])
                    ax9.axis("off")
                    ax9.set_xlim(0,10)
                    ax9.set_ylim(0,10)
                    ax9.scatter(2, 5, s=120, color=ColorOptionSel, edgecolors='#FFFFFF', lw=1)
                    ax9.text(2, -0.5, 'TOUCHES', fontproperties=prop2, fontsize=9, ha='center', va='center', c='w')
                    ax9.scatter(8, 5, s=320, color=ColorOptionSel, edgecolors='#FFFFFF', lw=1, ls='--', marker='h')
                    ax9.text(8, -0.5, 'ACTIONS\nTERRITORY', fontproperties=prop2, fontsize=9, ha='center', va='center', c='w')
                    st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
            elif OptionPlotSel == 'Heatmap - Zones':
    
                    #df = df[df['Event'] != 'Assists'].reset_index(drop=True)
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
                    ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfKKcleaned)) + " TOUCHES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                    ax9 = fig.add_axes([0.14,0.15,0.20,0.07])
                    ax9.scatter(6.75,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=1.0)
                    ax9.scatter(5.00,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.6)
                    ax9.scatter(3.25,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.2)
                    ax9.text(5, 0, '-  TOUCHES  +', c='w', fontproperties=prop2, fontsize=9, ha='center')
                    ax9.axis("off")
                    ax9.set_xlim(0,10)
                    ax9.set_ylim(0,10)
    
                    st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
            elif OptionPlotSel == 'Heatmap - Gaussian':
                    #df = df[df['Event'] != 'Assists'].reset_index(drop=True)
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
                    ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfKKcleaned)) + " TOUCHES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                    ax9 = fig.add_axes([0.14,0.15,0.20,0.07])
                    ax9.scatter(6.75,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=1.0)
                    ax9.scatter(5.00,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.6)
                    ax9.scatter(3.25,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.2)
                    ax9.text(5, 0, '-  TOUCHES  +', c='w', fontproperties=prop2, fontsize=9, ha='center')
                    ax9.axis("off")
                    ax9.set_xlim(0,10)
                    ax9.set_ylim(0,10)
                    st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
            elif OptionPlotSel == 'Heatmap - Kernel':
                    #df = df[df['Event'] != 'Assists'].reset_index(drop=True)
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
                    ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfKKcleaned)) + " TOUCHES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                    ax9 = fig.add_axes([0.14,0.15,0.20,0.07])
                    ax9.scatter(6.75,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=1.0)
                    ax9.scatter(5.00,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.6)
                    ax9.scatter(3.25,5, c=ColorOptionSel, marker='h', s=400, edgecolors='#121214', alpha=0.2)
                    ax9.text(5, 0, '-  TOUCHES  +', c='w', fontproperties=prop2, fontsize=9, ha='center')
                    ax9.axis("off")
                    ax9.set_xlim(0,10)
                    ax9.set_ylim(0,10)
                    st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png")
        with pltmain02:
            st.dataframe(df)
    elif EventlstSel == 'Passes':
        pltmnop11, pltmnop12, pltmnop13 = st.columns(3)
        with pltmnop11:
            OptionPlot = ['Passes Map', 'Progressive Passes Map', 'Passes to Final Third Map', 'Passes to Penalty Area', 'xT Passes Map']
            OptionPlotSel = st.selectbox('Choose viz:', OptionPlot)
        with pltmnop12:
            EfectMinSel = st.slider('Seleccionar rango de partido:', 0, 90, (0, 90))
        with pltmnop13:
                MetOption = ['Pases Claves', 'Asistencias']
                MetOptionSel = st.selectbox('Choose metric:', MetOption)
        pltmain11, pltmain12 = st.columns(2)
        with pltmain11:
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
            ax29.text(5, 2, 'Attack Direction', fontproperties=prop3, c=(1,1,1,0.5), fontsize=10, ha='center')
            #Adding winstats logo
            ax53 = fig.add_axes([0.82, 0.14, 0.05, 0.05])
            url53 = "https://i.postimg.cc/R0QjGByL/sZggzUM.png"
            response = requests.get(url53)
            img = Image.open(BytesIO(response.content))
            ax53.imshow(img)
            ax53.axis("off")
            ax53.set_facecolor("#000")
            ##st.dataframe(dfDOWN)
            ##df = df[(df['EfectiveMinute'] >= EfectMinSel[0]) & (df['EfectiveMinute'] <= EfectMinSel[1])]
            df_backup = df
            colorviz="#FF0046"
            if OptionPlotSel == 'Passes Map':
                ##df = df[(df['Event'] == 'Successful passes') | (df['Event'] == 'Key Passes') | (df['Event'] == 'Assists') | (df['Event'] == 'Successful open play crosses') | (df['Event'] == 'Successful set play crosses')].reset_index()
                dfKKK = df
                df = df_backup
                df = df[(df['Action'] == 'Pass') | (df['Action'] == 'Type pass')].reset_index(drop=True)
                ##dfKKK = df.drop_duplicates(subset=['X1', 'Y1', 'X2', 'Y2'], keep='last')
                ##dfast = df[df['Event'] == 'Assists']
                ##dfkey = df[df['Event'] == 'Key Passes']
                ##dfpas = df[(df['Event'] == 'Successful passes') | (df['Event'] == 'Successful open play crosses') | (df['Event'] == 'Successful set play crosses')]
                dfpas = df[df['Action'] == 'Pass'].reset_index(drop=True)
                dfkey = df[df['Action'] == 'Type pass'].reset_index(drop=True)
                
                ###Progressive
                df['Beginning'] = np.sqrt(np.square(105-df['X1']) + np.square(34-df['Y1']))
                df['Ending']    = np.sqrt(np.square(105-df['X2']) + np.square(34-df['Y2']))
                df['Progress']  = [(df['Ending'][x]) / (df['Beginning'][x]) <= 0.8 for x in range(len(df.Beginning))]
                
                
                ###Filter by passes progressives
                dfprog = df[df['Progress'] == True].reset_index()
                dfprog = dfprog.drop(['index'], axis=1)    
                pitch = Pitch(pitch_color='None', pitch_type='custom', line_zorder=1, linewidth=1, goal_type='box', pitch_length=105, pitch_width=68)
                pitch.draw(ax=ax)
                x1 = dfpas['X1']
                y1 = dfpas['Y1']
                x2 = dfpas['X2']
                y2 = dfpas['Y2']
                
                x1a = dfprog['X1']
                y1a = dfprog['Y1']
                x2a = dfprog['X2']
                y2a = dfprog['Y2']
                
                x1k = dfkey['X1']
                y1k = dfkey['Y1']
                x2k = dfkey['X2']
                y2k = dfkey['Y2']

                pitch.lines(x1, y1, x2, y2, cmap=get_continuous_cmap(hex_list), ax=ax, lw=2, comet=True, transparent=True) 
                ax.scatter(x2, y2, color='#9F9F9F', edgecolors='#121214', zorder=3, lw=0.5)       
                    
                pitch.lines(x1a, y1a, x2a, y2a, cmap=get_continuous_cmap(hex_list2), ax=ax, lw=2, comet=True, transparent=True, zorder=3) 
                ax.scatter(x2a, y2a, color=colorviz, edgecolors='#121214', zorder=3, lw=0.5)           
                
                
                pitch.lines(x1k, y1k, x2k, y2k, cmap=get_continuous_cmap(hex_list1), ax=ax, lw=2, comet=True, transparent=True, zorder=10) 
                ax.scatter(x2k, y2k, color="#C7B200", edgecolors='#121214', zorder=5, lw=0.5)
                ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(df)) + " PASES COMPLETOS", c='w', fontsize=10, fontproperties=prop2, ha='center')
                ax9 = fig.add_axes([0.20,0.14,0.63,0.07])
                ax9.set_xlim(0,105)
                ax9.set_ylim(0,20)
                ax9.axis("off")
                ax9.scatter(26.25, 12, marker='s', color='#9F9F9F', s=300)
                ax9.text(26.25, 2, 'SUCCESSFUL PASSES', color='#9F9F9F', fontproperties=prop2, ha='center', fontsize=9)
                ax9.scatter(52.5, 12, marker='s', color=colorviz, s=300)
                ax9.text(52.5, 2, 'PROGRESSIVE PASSES', color=colorviz, fontproperties=prop2, ha='center', fontsize=9)
                ax9.scatter(78.75, 12, marker='s', color='#C7B200', s=300)
                ax9.text(78.75, 2, 'KEY PASSES', color='#C7B200', fontproperties=prop2, ha='center', fontsize=9)

                st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png") 

            if OptionPlotSel == 'Progressive Passes Map':
                ##df = df[(df['Event'] == 'Successful passes') | (df['Event'] == 'Key Passes') | (df['Event'] == 'Assists') | (df['Event'] == 'Successful open play crosses') | (df['Event'] == 'Successful set play crosses') | (df['Event'] == 'Unsuccessful passes') | (df['Event'] == 'Unsuccessful open play crosses') | (df['Event'] == 'Unsuccessful set play crosses')].reset_index()
                ##dfKKK = df.drop_duplicates(subset=['X1', 'Y1', 'X2', 'Y2'], keep='last')
                ###Progressive
                dfKKK = df
                df = df_backup
                df = df[(df['Action'] == 'Pass') | (df['Action'] == 'Type pass')].reset_index(drop=True)
                dfpas = df[df['Action'] == 'Pass'].reset_index(drop=True)
                dfkey = df[df['Action'] == 'Type pass'].reset_index(drop=True)
                df['Beginning'] = np.sqrt(np.square(105-df['X1']) + np.square(34-df['Y1']))
                df['Ending']    = np.sqrt(np.square(105-df['X2']) + np.square(34-df['Y2']))
                df['Progress']  = [(df['Ending'][x]) / (df['Beginning'][x]) <= 0.8 for x in range(len(df.Beginning))]
                                          
                ###Filter by passes progressives
                dfprog = df[df['Progress'] == True].reset_index()
                dfprog = dfprog.drop(['index'], axis=1)
                ##dfprog = dfprog.drop_duplicates(subset=['X1', 'Y1', 'X2', 'Y2'], keep='last')
                dfw = dfprog[(dfprog['Index'] == 'Complete') | (dfprog['Index'] == 'Assists') | (dfprog['Index'] == 'Key') | (dfprog['Index'] == 'Second assist')].reset_index(drop=True)
                dff = dfprog[(dfprog['Index'] == 'Miss')].reset_index(drop=True)
                ##dfw = dfprog[(dfprog['Event'] == 'Successful passes') | (dfprog['Event'] == 'Key Passes') | (dfprog['Event'] == 'Assists') | (dfprog['Event'] == 'Successful open play crosses') | (dfprog['Event'] == 'Successful set play crosses')].reset_index(drop=True)
                ##dff = dfprog[(dfprog['Event'] == 'Unsuccessful passes') | (dfprog['Event'] == 'Unsuccessful open play crosses') | (dfprog['Event'] == 'Unsuccessful set play crosses')].reset_index(drop=True)

                pitch = Pitch(pitch_color='None', pitch_type='custom', line_zorder=1, linewidth=1, goal_type='box', pitch_length=105, pitch_width=68)
                pitch.draw(ax=ax)
                
                pitch.lines(dfw['X1'], dfw['Y1'], dfw['X2'], dfw['Y2'], cmap=get_continuous_cmap(hex_list2), ax=ax, lw=2, comet=True, transparent=True, zorder=3) 
                ax.scatter(dfw['X2'], dfw['Y2'], color=colorviz, edgecolors='#121214', zorder=3, lw=0.5)  

                pitch.lines(dff['X1'], dff['Y1'], dff['X2'], dff['Y2'], cmap=get_continuous_cmap(hex_list), ax=ax, lw=2, comet=True, transparent=True, zorder=3) 
                ax.scatter(dff['X2'], dff['Y2'], color="#9F9F9F", edgecolors='#121214', zorder=3, lw=0.5)     
                ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(dfprog)) + " PROGRESSIVE PASSES", c='w', fontsize=10, fontproperties=prop2, ha='center')
                ax9 = fig.add_axes([0.20,0.14,0.63,0.07])
                ax9.set_xlim(0,105)
                ax9.set_ylim(0,20)
                ax9.axis("off")
                ax9.scatter(32.5, 15, marker='s', color=colorviz, s=300)
                ax9.text(32.5, 0, 'SUCCESSFUL\nPROGRESSIVE PASSES', color=colorviz, fontproperties=prop2, ha='center', fontsize=9)
                ax9.scatter(72.5, 15, marker='s', color='#9F9F9F', s=300)
                ax9.text(72.5, 0, 'UNSUCCESSFUL\nPROGRESSIVE PASSES', color='#9F9F9F', fontproperties=prop2, ha='center', fontsize=9)
                st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png") 
            if OptionPlotSel == 'Passes to Final Third Map':
                ##df = df[(df['Event'] == 'Successful passes') | (df['Event'] == 'Key Passes') | (df['Event'] == 'Assists') | (df['Event'] == 'Successful open play crosses') | (df['Event'] == 'Successful set play crosses') | (df['Event'] == 'Unsuccessful passes') | (df['Event'] == 'Unsuccessful open play crosses') | (df['Event'] == 'Unsuccessful set play crosses')].reset_index()
                ##df = df[(df['X1'] <= 70) & (df['X2'] >= 70)].reset_index(drop=True)
                df = df_backup
                df = df[(df['Action'] == 'Pass') | (df['Action'] == 'Type pass')].reset_index(drop=True)
                df = df[(df['X1'] <= 70) & (df['X2'] >= 70)].reset_index(drop=True)
                ##dfwin = df[(df['Event'] == 'Successful passes') | (df['Event'] == 'Key Passes') | (df['Event'] == 'Assists') | (df['Event'] == 'Successful open play crosses') | (df['Event'] == 'Successful set play crosses')].reset_index(drop=True)
                ##dffail = df[(df['Event'] == 'Unsuccessful passes') | (df['Event'] == 'Unsuccessful open play crosses') | (df['Event'] == 'Unsuccessful set play crosses')].reset_index(drop=True)
                dfKKK = df
                ##dfKKK = df.drop_duplicates(subset=['X1', 'Y1', 'X2', 'Y2'], keep='last')
                
                pitch = Pitch(pitch_color='None', pitch_type='custom', line_zorder=1, linewidth=1, goal_type='box', pitch_length=105, pitch_width=68)
                pitch.draw(ax=ax)
                pitch.lines(df['X1'], df['Y1'], df['X2'], df['Y2'], cmap=get_continuous_cmap(hex_list2), ax=ax, lw=2, comet=True, transparent=True)
                ax.scatter(df['X2'], df['Y2'], color='#FF0050', edgecolors='#121214', zorder=3, lw=0.5)
                #pitch.lines(dffail['X1'], dffail['Y1'], dffail['X2'], dffail['Y2'], cmap=get_continuous_cmap(hex_list), ax=ax, lw=2, comet=True, transparent=True)
                #ax.scatter(dffail['X2'], dffail['Y2'], color='#9F9F9F', edgecolors='#121214', zorder=3, lw=0.5)
                ax.vlines(x=70, ymin=0, ymax=68, color='w', alpha=0.3, ls='--', zorder=-1)
                ax.add_patch(Rectangle((70, 0), 35, 68, fc="#000000", fill=True, alpha=0.7, zorder=-2))

                ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(df)) + " PASES HACIA ÚLTIMO TERCIO", c='w', fontsize=10, fontproperties=prop2, ha='center')
                ax9 = fig.add_axes([0.20,0.14,0.63,0.07])
                ax9.set_xlim(0,105)
                ax9.set_ylim(0,20)
                ax9.axis("off")
                #ax9.scatter(26.25, 12, marker='s', color='#9F9F9F', s=300)
                #ax9.text(26.25, 2, 'PASES EFECTIVOS', color='#9F9F9F', fontproperties=prop2, ha='center', fontsize=9)
                ax9.scatter(32.5, 12, marker='s', color=colorviz, s=300)
                ax9.text(32.5, 2, 'PASES EXITOSOS', color=colorviz, fontproperties=prop2, ha='center', fontsize=9)
                ax9.scatter(72.5, 12, marker='s', color='#9F9F9F', s=300)
                ax9.text(72.5, 2, 'PASES FALLADOS', color='#9F9F9F', fontproperties=prop2, ha='center', fontsize=9)

                st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png") 
                #pitch.lines(x1a, y1a, x2a, y2a, cmap=get_continuous_cmap(hex_list2), ax=ax, lw=2, comet=True, transparent=True, zorder=3) 
                #ax.scatter(x2a, y2a, color=colorviz, edgecolors='#121214', zorder=3, lw=0.5)
            if OptionPlotSel == 'Passes to Penalty Area':
                #df = df[(df['Event'] == 'Successful passes') | (df['Event'] == 'Key Passes') | (df['Event'] == 'Assists') | (df['Event'] == 'Successful open play crosses') | (df['Event'] == 'Successful set play crosses') | (df['Event'] == 'Unsuccessful passes') | (df['Event'] == 'Unsuccessful open play crosses') | (df['Event'] == 'Unsuccessful set play crosses')].reset_index()
                #dfKKK = df.drop_duplicates(subset=['X1', 'Y1', 'X2', 'Y2'], keep='last')
                # Coordenadas del cuadrilátero
                x1_cuadrilatero, y1_cuadrilatero = 88.5, 13.84
                x2_cuadrilatero, y2_cuadrilatero = 105, 13.84
                x3_cuadrilatero, y3_cuadrilatero = 88.5, 54.16
                x4_cuadrilatero, y4_cuadrilatero = 105, 54.16
                
                # Primera condición: X1, Y1 deben estar por fuera del cuadrilátero
                condicion1 = (
                    (df['X1'] < x1_cuadrilatero) |    # X1 debe ser menor que x1_cuadrilatero
                    (df['Y1'] < y1_cuadrilatero) |    # Y1 debe ser menor que y1_cuadrilatero
                    (df['X1'] > x4_cuadrilatero) |    # X1 debe ser mayor que x4_cuadrilatero
                    (df['Y1'] > y3_cuadrilatero)      # Y1 debe ser mayor que y3_cuadrilatero
                )
                
                # Segunda condición: X2, Y2 deben estar por dentro del cuadrilátero
                condicion2 = (
                    (df['X2'] >= x1_cuadrilatero) &   # X2 debe ser mayor o igual que x1_cuadrilatero
                    (df['Y2'] >= y1_cuadrilatero) &   # Y2 debe ser mayor o igual que y1_cuadrilatero
                    (df['X2'] <= x4_cuadrilatero) &   # X2 debe ser menor o igual que x4_cuadrilatero
                    (df['Y2'] <= y3_cuadrilatero)     # Y2 debe ser menor o igual que y3_cuadrilatero
                )
                
                # Aplicar las condiciones para filtrar el DataFrame
                df = df[condicion1 & condicion2]
                pitch = Pitch(pitch_color='None', pitch_type='custom', line_zorder=1, linewidth=1, goal_type='box', pitch_length=105, pitch_width=68)
                pitch.draw(ax=ax)

                dfw = df[(df['Event'] == 'Successful passes') | (df['Event'] == 'Key Passes') | (df['Event'] == 'Assists') | (df['Event'] == 'Successful open play crosses') | (df['Event'] == 'Successful set play crosses')].reset_index(drop=True)
                dff = df[(df['Event'] == 'Unsuccessful passes') | (df['Event'] == 'Unsuccessful open play crosses') | (df['Event'] == 'Unsuccessful set play crosses')].reset_index(drop=True)
                
                pitch.lines(dfw['X1'], dfw['Y1'], dfw['X2'], dfw['Y2'], cmap=get_continuous_cmap(hex_list2), ax=ax, lw=2, comet=True, transparent=True, zorder=3) 
                ax.scatter(dfw['X2'], dfw['Y2'], color=colorviz, edgecolors='#121214', zorder=3, lw=0.5)  

                pitch.lines(dff['X1'], dff['Y1'], dff['X2'], dff['Y2'], cmap=get_continuous_cmap(hex_list), ax=ax, lw=2, comet=True, transparent=True, zorder=3) 
                ax.scatter(dff['X2'], dff['Y2'], color="#9F9F9F", edgecolors='#121214', zorder=3, lw=0.5)  
                ax.vlines(x=88.5, ymin=13.84, ymax=54.16, color='w', alpha=1, ls='--', lw=2, zorder=-1)
                #ax.vlines(x=105, ymin=13.84, ymax=54.16, color='w', alpha=1, ls='--', lw=2, zorder=-1)
                ax.hlines(xmin=88.5, xmax=105, y=54.16, color='w', alpha=1, ls='--', lw=2, zorder=-1)
                ax.hlines(xmin=88.5, xmax=105, y=13.84, color='w', alpha=1, ls='--', lw=2, zorder=-1)
                ax.add_patch(Rectangle((88.5, 13.84), 16.5, 40.32, fc="#000000", fill=True, alpha=0.7, zorder=-2))
                ax.text(52.5,70, "" + PlayerPltSel.upper() + " - " + str(len(df)) + " PASES HACIA ÁREA RIVAL", c='w', fontsize=10, fontproperties=prop2, ha='center')
                ax9 = fig.add_axes([0.20,0.14,0.63,0.07])
                ax9.set_xlim(0,105)
                ax9.set_ylim(0,20)
                ax9.axis("off")
                #ax9.scatter(26.25, 12, marker='s', color='#9F9F9F', s=300)
                #ax9.text(26.25, 2, 'PASES EFECTIVOS', color='#9F9F9F', fontproperties=prop2, ha='center', fontsize=9)
                ax9.scatter(32.5, 15, marker='s', color=colorviz, s=300)
                ax9.text(32.5, 0, 'PASES EXITOSOS\nHACIAÁREA RIVAL', color=colorviz, fontproperties=prop2, ha='center', fontsize=9)
                ax9.scatter(72.5, 15, marker='s', color='#9F9F9F', s=300)
                ax9.text(72.5, 0, 'PASES FALLADOS\nHACIA ÁREA RIVAL', color='#9F9F9F', fontproperties=prop2, ha='center', fontsize=9)
                st.pyplot(fig, bbox_inches="tight", pad_inches=0.05, dpi=400, format="png") 
            if OptionPlotSel == 'xT Passes Map':
                pitch = Pitch(pitch_color='None', pitch_type='custom', line_zorder=1, linewidth=1, goal_type='box', pitch_length=105, pitch_width=68)
                pitch.draw(ax=ax)
        with pltmain12:
            st.dataframe(df)

    st.markdown("""----""")
    metricplayerbox01, metricplayerbox02, metricplayerbox03 = st.columns(3)
    with metricplayerbox01:
        #Team_Lst = df['Team'].drop_duplicates().tolist()
        Metric_Lst = columnsevents
        MetricSel = st.selectbox("Choose metric:", Metric_Lst)
    st.markdown("""----""")
