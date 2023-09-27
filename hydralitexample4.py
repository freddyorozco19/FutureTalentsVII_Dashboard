# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 09:43:57 2023

@author: ACER
"""
import streamlit as st
import hydralit_components as hc
import datetime
import base64
import pandas as pd
from io import BytesIO
import pandas as pd
import numpy as np

############################################################################################################################################################################################################################

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################

#make it look nice from the start
st.set_page_config(layout='wide')
    
# specify the primary menu definition
menu_data = [
    {'id': "EventingData", 'label':"Match EventingData"},
    {'id': "JoinEventingData", 'label':"Join EventingData"},
    {'id': "PNData", 'label':"PassNetworkData"},
    {'id': "ProMatchStats", 'label':"ProMatchStats"},
    {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"} #can add a tooltip message]
]
over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Logout',
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

if menu_id == "ProMatchStats":
    with st.sidebar:
        with open("C:/Users/ACER/Documents/WinStats/Resources/win.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
            st.sidebar.markdown(
                f"""
                <div style="display:table;margin-top:-20%">
                    <img src="data:image/png;base64,{data}" width="300">
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown("""---""")    
        
        with st.form(key='form3'):
            
            teamstatus = st.text_input("Ingrese Equipo Local:")
            tablecode = st.text_area('Paste your source code (Home)') 
            teamstatus2 = st.text_input("Ingrese Equipo Visitante:")
            tablecode2 = st.text_area('Paste your source code (Away)')
            seloption = st.selectbox("Seleccione Modo Consulta", ["Home", "Away", "All"])
            submit_button3 = st.form_submit_button(label='Aceptar')
        
        
        
        
    def aplicar_transformaciones_dfgeneral(df, teamstatus):
        df1 = df['two'].str.split("</tbody>", expand = True)
        df1.columns = ['Table', 'Code']
        df1 = df1.drop(['Code'], axis = 1)
        df11 = df1['Table'].str.split("<tr>", expand = True).T
        df11.columns = ['Events']
        df11.drop(df11.head(1).index,inplace=True)
        df11 = df11.reset_index()
        df11['Events'] = df11['Events'].str[24:]
        df1tit = df11['Events'].iloc[:1]
        df11.drop(df1.head(1).index,inplace=True)
        df11 = df11.drop(['index'], axis=1)        
        df111 = df11['Events'].str.split("<td", expand = True)
        df111.columns = ['Player', 'Minutos jugados', 'Toques', 'Duelos totales', '% Duelos ganados', 'Duelos aéreos totales', '% Duelos aéreos ganados', 'Rivales eludidos', 'Faltas recibidas', 'Posiciones adelantadas', 'Tiros de esquina']
        df111a = df111[df111['Minutos jugados'].str.contains('class="highest">')].reset_index()
        df111b = df111[~df111['Minutos jugados'].str.contains('class="highest">')].reset_index()
        df111a['Minutos jugados'] = df111a['Minutos jugados'].str[17:-5]
        df111b['Minutos jugados'] = df111b['Minutos jugados'].str[1:-5]
        df111 = pd.concat([df111a, df111b], axis=0)
        df111c = df111[df111['Toques'].str.contains('class="highest">')]
        df111d = df111[~df111['Toques'].str.contains('class="highest">')]
        df111c['Toques'] = df111c['Toques'].str[17:-5]
        df111d['Toques'] = df111d['Toques'].str[1:-5]
        df111 = pd.concat([df111c, df111d], axis=0)
        df111 = df111.sort_values(by="index")
        df111e = df111[df111['Duelos totales'].str.contains('class="highest">')]
        df111f = df111[~df111['Duelos totales'].str.contains('class="highest">')]
        df111e['Duelos totales'] = df111e['Duelos totales'].str[17:-5]
        df111f['Duelos totales'] = df111f['Duelos totales'].str[1:-5]
        df111 = pd.concat([df111e, df111f], axis=0)
        df111 = df111.sort_values(by="index")
        #df111 = df111.replace()
        df111g = df111[df111['% Duelos ganados'].str.contains('class="highest">')]
        df111h = df111[~df111['% Duelos ganados'].str.contains('class="highest">')]
        df111g['% Duelos ganados'] = df111g['% Duelos ganados'].str[17:-5]
        df111h['% Duelos ganados'] = df111h['% Duelos ganados'].str[1:-5]
        df111 = pd.concat([df111g, df111h], axis=0)
        df111 = df111.sort_values(by="index")
        df111i = df111[df111['Duelos aéreos totales'].str.contains('class="highest">')]
        df111j = df111[~df111['Duelos aéreos totales'].str.contains('class="highest">')]
        df111i['Duelos aéreos totales'] = df111i['Duelos aéreos totales'].str[17:-5]
        df111j['Duelos aéreos totales'] = df111j['Duelos aéreos totales'].str[1:-5]
        df111 = pd.concat([df111i, df111j], axis=0)
        df111 = df111.sort_values(by="index")
        df111k = df111[df111['% Duelos aéreos ganados'].str.contains('class="highest">')]
        df111l = df111[~df111['% Duelos aéreos ganados'].str.contains('class="highest">')]
        df111k['% Duelos aéreos ganados'] = df111k['% Duelos aéreos ganados'].str[17:-5]
        df111l['% Duelos aéreos ganados'] = df111l['% Duelos aéreos ganados'].str[1:-5]
        df111 = pd.concat([df111k, df111l], axis=0)
        df111 = df111.sort_values(by="index")
        df111m = df111[df111['Rivales eludidos'].str.contains('class="highest">')]
        df111n = df111[~df111['Rivales eludidos'].str.contains('class="highest">')]
        df111m['Rivales eludidos'] = df111m['Rivales eludidos'].str[17:-5]
        df111n['Rivales eludidos'] = df111n['Rivales eludidos'].str[1:-5]
        df111 = pd.concat([df111m, df111n], axis=0)
        df111 = df111.sort_values(by="index")
        df111o = df111[df111['Faltas recibidas'].str.contains('class="highest">')]
        df111p = df111[~df111['Faltas recibidas'].str.contains('class="highest">')]
        df111o['Faltas recibidas'] = df111o['Faltas recibidas'].str[17:-5]
        df111p['Faltas recibidas'] = df111p['Faltas recibidas'].str[1:-5]
        df111 = pd.concat([df111o, df111p], axis=0)
        df111 = df111.sort_values(by="index")
        df111q = df111[df111['Posiciones adelantadas'].str.contains('class="highest">')]
        df111r = df111[~df111['Posiciones adelantadas'].str.contains('class="highest">')]
        df111q['Posiciones adelantadas'] = df111q['Posiciones adelantadas'].str[17:-5]
        df111r['Posiciones adelantadas'] = df111r['Posiciones adelantadas'].str[1:-5]
        df111 = pd.concat([df111q, df111r], axis=0)
        df111 = df111.sort_values(by="index")
        df111s = df111[df111['Tiros de esquina'].str.contains('class="highest">')]
        df111t = df111[~df111['Tiros de esquina'].str.contains('class="highest">')]
        df111s['Tiros de esquina'] = df111s['Tiros de esquina'].str[17:-10]
        df111t['Tiros de esquina'] = df111t['Tiros de esquina'].str[1:-10]
        df111 = pd.concat([df111s, df111t], axis=0)
        df111 = df111.sort_values(by="index")
        df111 = df111.reset_index()
        df111 = df111.drop(['level_0'], axis=1)
        df111z = df111['Player'].str.split('>', expand = True)
        df111z.columns = ['Uno', 'Player', 'Tres', 'Cuatro']
        df111z = df111z.drop(['Uno', 'Tres', 'Cuatro'], axis=1)
        df111z['Player'] = df111z['Player'].str[:-6]
        df111 = df111.drop(['Player'], axis=1)
        df111 = pd.concat([df111z, df111], axis=1)
        df111 = df111[['index', 'Player', 'Minutos jugados', 'Toques', 'Duelos totales', '% Duelos ganados', 'Duelos aéreos totales', '% Duelos aéreos ganados', 'Rivales eludidos', 'Faltas recibidas', 'Posiciones adelantadas', 'Tiros de esquina']]
        df111 = df111.replace("-", 0)
        df111['Minutos jugados'] = df111['Minutos jugados'].astype(int) 
        df111['Toques'] = df111['Toques'].astype(int) 
        df111['Duelos totales'] = df111['Duelos totales'].astype(int)
        df111['% Duelos ganados'] = df111['% Duelos ganados'].str.replace("%", "")
        df111['% Duelos ganados'] = df111['% Duelos ganados'].str.replace(",", ".")
        df111['% Duelos ganados'] = df111['% Duelos ganados'].astype(float) 
        df111['Duelos ganados'] = round((df111['Duelos totales']*df111['% Duelos ganados'])/100)
        df111['Duelos aéreos totales'] = df111['Duelos aéreos totales'].astype(int) 
        df111['% Duelos aéreos ganados'] = df111['% Duelos aéreos ganados'].str.replace("%", "")
        df111['% Duelos aéreos ganados'] = df111['% Duelos aéreos ganados'].str.replace(",", ".")
        df111['% Duelos aéreos ganados'] = df111['% Duelos aéreos ganados'].astype(float) 
        df111['Duelos aéreos ganados'] = round((df111['Duelos aéreos totales']*df111['% Duelos aéreos ganados'])/100)
        df111['Rivales eludidos'] = df111['Rivales eludidos'].astype(int) 
        df111['Faltas recibidas'] = df111['Faltas recibidas'].astype(int)
        df111['Posiciones adelantadas'] = df111['Posiciones adelantadas'].astype(int)
        df111['Tiros de esquina'] = df111['Tiros de esquina'].astype(int)
        df111 = df111.fillna(0)
        lst = []
        aux = teamstatus
        for i in range(len(df111)):
            lst.append(aux)
        dfpss = pd.DataFrame([lst]).T
        dfpss.columns = ['Team']
        df111 = pd.concat([df111, dfpss], axis = 1)
        df111 = df111[['index', 'Team', 'Player', 'Minutos jugados', 'Toques', 'Duelos totales', 'Duelos ganados', '% Duelos ganados', 'Duelos aéreos totales', 'Duelos aéreos ganados', '% Duelos aéreos ganados', 'Rivales eludidos', 'Faltas recibidas', 'Posiciones adelantadas', 'Tiros de esquina']]
        #st.dataframe(df111, use_container_width=True)
        return df111
    
    def aplicar_transformaciones_dfataque(df, teamstatus):
        df3 = df['fou'].str.split("</tbody>", expand = True)
        df3.columns = ['Table', 'Code']
        df3 = df3.drop(['Code'], axis = 1)
        df33 = df3['Table'].str.split("<tr>", expand = True).T
        df33.columns = ['Events']
        df33.drop(df33.head(1).index,inplace=True)
        df33 = df33.reset_index()
        df33['Events'] = df33['Events'].str[24:]
        df3tit = df33['Events'].iloc[:1]
        df33.drop(df3.head(1).index,inplace=True)
        df33 = df33.drop(['index'], axis=1)
        df333 = df33['Events'].str.split("<td", expand = True)
        df333.columns = ['Player', 'Goles', 'Remates intentados', 'Remates al arco', 'Remates bloqueados', 'Remates de cabeza', 'Remates desde fuera del área', 'Remates desde dentro del área', 'Shot accuracy (%)', 'Asistencia', 'Chances creadas']
        df333 = df333.reset_index()
        df333a = df333[df333['Goles'].str.contains('class="highest">')]
        df333b = df333[~df333['Goles'].str.contains('class="highest">')]
        df333a['Goles'] = df333a['Goles'].str[17:-5]
        df333b['Goles'] = df333b['Goles'].str[1:-5]
        df333 = pd.concat([df333a, df333b], axis=0)
        df333 = df333.sort_values(by="index")
        df333c = df333[df333['Remates intentados'].str.contains('class="highest">')]
        df333d = df333[~df333['Remates intentados'].str.contains('class="highest">')]
        df333c['Remates intentados'] = df333c['Remates intentados'].str[17:-5]
        df333d['Remates intentados'] = df333d['Remates intentados'].str[1:-5]
        df333 = pd.concat([df333c, df333d], axis=0)
        df333 = df333.sort_values(by="index")
        df333e = df333[df333['Remates al arco'].str.contains('class="highest">')]
        df333f = df333[~df333['Remates al arco'].str.contains('class="highest">')]
        df333e['Remates al arco'] = df333e['Remates al arco'].str[17:-5]
        df333f['Remates al arco'] = df333f['Remates al arco'].str[1:-5]
        df333 = pd.concat([df333e, df333f], axis=0)
        df333 = df333.sort_values(by="index")
        df333g = df333[df333['Remates bloqueados'].str.contains('class="highest">')]
        df333h = df333[~df333['Remates bloqueados'].str.contains('class="highest">')]
        df333g['Remates bloqueados'] = df333g['Remates bloqueados'].str[17:-5]
        df333h['Remates bloqueados'] = df333h['Remates bloqueados'].str[1:-5]
        df333 = pd.concat([df333g, df333h], axis=0)
        df333 = df333.sort_values(by="index")
        df333i = df333[df333['Remates de cabeza'].str.contains('class="highest">')]
        df333j = df333[~df333['Remates de cabeza'].str.contains('class="highest">')]
        df333i['Remates de cabeza'] = df333i['Remates de cabeza'].str[17:-5]
        df333j['Remates de cabeza'] = df333j['Remates de cabeza'].str[1:-5]
        df333 = pd.concat([df333i, df333j], axis=0)
        df333 = df333.sort_values(by="index")
        df333k = df333[df333['Remates desde fuera del área'].str.contains('class="highest">')]
        df333l = df333[~df333['Remates desde fuera del área'].str.contains('class="highest">')]
        df333k['Remates desde fuera del área'] = df333k['Remates desde fuera del área'].str[17:-5]
        df333l['Remates desde fuera del área'] = df333l['Remates desde fuera del área'].str[1:-5]
        df333 = pd.concat([df333k, df333l], axis=0)
        df333 = df333.sort_values(by="index")
        df333m = df333[df333['Remates desde dentro del área'].str.contains('class="highest">')]
        df333n = df333[~df333['Remates desde dentro del área'].str.contains('class="highest">')]
        df333m['Remates desde dentro del área'] = df333m['Remates desde dentro del área'].str[17:-5]
        df333n['Remates desde dentro del área'] = df333n['Remates desde dentro del área'].str[1:-5]
        df333 = pd.concat([df333m, df333n], axis=0)
        df333 = df333.sort_values(by="index")
        df333o = df333[df333['Shot accuracy (%)'].str.contains('class="highest">')]
        df333p = df333[~df333['Shot accuracy (%)'].str.contains('class="highest">')]
        df333o['Shot accuracy (%)'] = df333o['Shot accuracy (%)'].str[17:-5]
        df333p['Shot accuracy (%)'] = df333p['Shot accuracy (%)'].str[1:-5]
        df333 = pd.concat([df333o, df333p], axis=0)
        df333 = df333.sort_values(by="index")
        df333q = df333[df333['Asistencia'].str.contains('class="highest">')]
        df333r = df333[~df333['Asistencia'].str.contains('class="highest">')]
        df333q['Asistencia'] = df333q['Asistencia'].str[17:-5]
        df333r['Asistencia'] = df333r['Asistencia'].str[1:-5]
        df333 = pd.concat([df333q, df333r], axis=0)
        df333 = df333.sort_values(by="index")
        df333s = df333[df333['Chances creadas'].str.contains('class="highest">')]
        df333t = df333[~df333['Chances creadas'].str.contains('class="highest">')]
        df333s['Chances creadas'] = df333s['Chances creadas'].str[17:-10]
        df333t['Chances creadas'] = df333t['Chances creadas'].str[1:-10]
        df333 = pd.concat([df333s, df333t], axis=0)
        df333 = df333.sort_values(by="index")
        df333z = df333['Player'].str.split('>', expand = True)
        df333z.columns = ['Uno', 'Player', 'Tres', 'Cuatro']
        df333z = df333z.drop(['Uno', 'Tres', 'Cuatro'], axis=1)
        df333z['Player'] = df333z['Player'].str[:-6]
        df333 = df333.drop(['Player'], axis=1)
        df333 = pd.concat([df333z, df333], axis=1)
        df333 = df333[['index', 'Player', 'Goles', 'Remates intentados', 'Remates al arco', 'Remates bloqueados', 'Remates de cabeza', 'Remates desde fuera del área', 'Remates desde dentro del área', 'Shot accuracy (%)', 'Asistencia', 'Chances creadas']]
        df333 = df333.replace("-", 0)
        df333['Goles'] = df333['Goles'].astype(int)
        df333['Remates intentados'] = df333['Remates intentados'].astype(int)
        df333['Remates al arco'] = df333['Remates al arco'].astype(int)
        df333['Remates bloqueados'] = df333['Remates bloqueados'].astype(int)
        df333['Remates de cabeza'] = df333['Remates de cabeza'].astype(int)
        df333['Remates desde fuera del área'] = df333['Remates desde fuera del área'].astype(int)
        df333['Remates desde dentro del área'] = df333['Remates desde dentro del área'].astype(int)
        df333['Shot accuracy (%)'] = df333['Shot accuracy (%)'].str.replace("%", "")
        df333['Shot accuracy (%)'] = df333['Shot accuracy (%)'].str.replace(",", ".")
        df333['Shot accuracy (%)'] = df333['Shot accuracy (%)'].astype(float)
        df333['Asistencia'] = df333['Asistencia'].astype(int)
        df333['Chances creadas'] = df333['Chances creadas'].astype(int)
        df333 = df333.fillna(0)
        lst = []
        aux = teamstatus
        for i in range(len(df333)):
            lst.append(aux)
        dfpss = pd.DataFrame([lst]).T
        dfpss.columns = ['Team']
        df333 = pd.concat([df333, dfpss], axis = 1)
        df333 = df333[['index', 'Team', 'Player', 'Goles', 'Remates intentados', 'Remates al arco', 'Remates bloqueados', 'Remates de cabeza', 'Remates desde fuera del área', 'Remates desde dentro del área', 'Shot accuracy (%)', 'Asistencia', 'Chances creadas']]

        #st.dataframe(df333, use_container_width=True)
        return df333
        
    def aplicar_transformaciones_dfdistribucion(df, teamstatus):
        #st.title("DISTRIBUCIÓN")
        df4 = df['fiv'].str.split("</tbody>", expand = True)
        df4.columns = ['Table', 'Code']
        df4 = df4.drop(['Code'], axis = 1)
        df44 = df4['Table'].str.split("<tr>", expand = True).T
        df44.columns = ['Events']
        df44.drop(df44.head(1).index,inplace=True)
        df44 = df44.reset_index()
        df44['Events'] = df44['Events'].str[24:]
        df4tit = df44['Events'].iloc[:1]
        df44.drop(df4.head(1).index,inplace=True)
        df44 = df44.drop(['index'], axis=1)
        df444 = df44['Events'].str.split("<td", expand = True)
        df444.columns = ['Player', 'Pases intentados', 'Pases completos', 'Pases largos (%)', 'Precisión de pases (%)', 'Pases en campo rival', '% Pases completos en campo rival', '% Precisión de los pases en el último tercio de campo', 'Through Balls', 'Pases al último tercio', 'Pases al área contraria', 'Centros con pelota en movimiento', 'Good passes and crosses']
        df444 = df444.reset_index()
        df444a = df444[df444['Pases intentados'].str.contains('class="highest">')]
        df444b = df444[~df444['Pases intentados'].str.contains('class="highest">')]
        df444a['Pases intentados'] = df444a['Pases intentados'].str[17:-5]
        df444b['Pases intentados'] = df444b['Pases intentados'].str[1:-5]
        df444 = pd.concat([df444a, df444b], axis=0)
        df444 = df444.sort_values(by="index")
        df444c = df444[df444['Pases completos'].str.contains('class="highest">')]
        df444d = df444[~df444['Pases completos'].str.contains('class="highest">')]
        df444c['Pases completos'] = df444c['Pases completos'].str[17:-5]
        df444d['Pases completos'] = df444d['Pases completos'].str[1:-5]
        df444 = pd.concat([df444c, df444d], axis=0)
        df444 = df444.sort_values(by="index")
        df444e = df444[df444['Pases largos (%)'].str.contains('class="highest">')]
        df444f = df444[~df444['Pases largos (%)'].str.contains('class="highest">')]
        df444e['Pases largos (%)'] = df444e['Pases largos (%)'].str[17:-5]
        df444f['Pases largos (%)'] = df444f['Pases largos (%)'].str[1:-5]
        df444 = pd.concat([df444e, df444f], axis=0)
        df444 = df444.sort_values(by="index")
        df444g = df444[df444['Precisión de pases (%)'].str.contains('class="highest">')]
        df444h = df444[~df444['Precisión de pases (%)'].str.contains('class="highest">')]
        df444g['Precisión de pases (%)'] = df444g['Precisión de pases (%)'].str[17:-5]
        df444h['Precisión de pases (%)'] = df444h['Precisión de pases (%)'].str[1:-5]
        df444 = pd.concat([df444g, df444h], axis=0)
        df444 = df444.sort_values(by="index")
        df444i = df444[df444['Pases en campo rival'].str.contains('class="highest">')]
        df444j = df444[~df444['Pases en campo rival'].str.contains('class="highest">')]
        df444i['Pases en campo rival'] = df444i['Pases en campo rival'].str[17:-5]
        df444j['Pases en campo rival'] = df444j['Pases en campo rival'].str[1:-5]
        df444 = pd.concat([df444i, df444j], axis=0)
        df444 = df444.sort_values(by="index")
        df444k = df444[df444['% Pases completos en campo rival'].str.contains('class="highest">')]
        df444l = df444[~df444['% Pases completos en campo rival'].str.contains('class="highest">')]
        df444k['% Pases completos en campo rival'] = df444k['% Pases completos en campo rival'].str[17:-5]
        df444l['% Pases completos en campo rival'] = df444l['% Pases completos en campo rival'].str[1:-5]
        df444 = pd.concat([df444k, df444l], axis=0)
        df444 = df444.sort_values(by="index")
        df444m = df444[df444['% Precisión de los pases en el último tercio de campo'].str.contains('class="highest">')]
        df444n = df444[~df444['% Precisión de los pases en el último tercio de campo'].str.contains('class="highest">')]
        df444m['% Precisión de los pases en el último tercio de campo'] = df444m['% Precisión de los pases en el último tercio de campo'].str[17:-5]
        df444n['% Precisión de los pases en el último tercio de campo'] = df444n['% Precisión de los pases en el último tercio de campo'].str[1:-5]
        df444 = pd.concat([df444m, df444n], axis=0)
        df444 = df444.sort_values(by="index")
        df444o = df444[df444['Through Balls'].str.contains('class="highest">')]
        df444p = df444[~df444['Through Balls'].str.contains('class="highest">')]
        df444o['Through Balls'] = df444o['Through Balls'].str[17:-5]
        df444p['Through Balls'] = df444p['Through Balls'].str[1:-5]
        df444 = pd.concat([df444o, df444p], axis=0)
        df444 = df444.sort_values(by="index")
        df444q = df444[df444['Pases al último tercio'].str.contains('class="highest">')]
        df444r = df444[~df444['Pases al último tercio'].str.contains('class="highest">')]
        df444q['Pases al último tercio'] = df444q['Pases al último tercio'].str[17:-5]
        df444r['Pases al último tercio'] = df444r['Pases al último tercio'].str[1:-5]
        df444 = pd.concat([df444q, df444r], axis=0)
        df444 = df444.sort_values(by="index")
        df444s = df444[df444['Pases al área contraria'].str.contains('class="highest">')]
        df444t = df444[~df444['Pases al área contraria'].str.contains('class="highest">')]
        df444s['Pases al área contraria'] = df444s['Pases al área contraria'].str[17:-5]
        df444t['Pases al área contraria'] = df444t['Pases al área contraria'].str[1:-5]
        df444 = pd.concat([df444s, df444t], axis=0)
        df444 = df444.sort_values(by="index")
        df444u = df444[df444['Centros con pelota en movimiento'].str.contains('class="highest">')]
        df444v = df444[~df444['Centros con pelota en movimiento'].str.contains('class="highest">')]
        df444u['Centros con pelota en movimiento'] = df444u['Centros con pelota en movimiento'].str[17:-5]
        df444v['Centros con pelota en movimiento'] = df444v['Centros con pelota en movimiento'].str[1:-5]
        df444 = pd.concat([df444u, df444v], axis=0)
        df444 = df444.sort_values(by="index")
        df444w = df444[df444['Good passes and crosses'].str.contains('class="highest">')]
        df444x = df444[~df444['Good passes and crosses'].str.contains('class="highest">')]
        df444w['Good passes and crosses'] = df444w['Good passes and crosses'].str[17:-10]
        df444x['Good passes and crosses'] = df444x['Good passes and crosses'].str[1:-10]
        df444 = pd.concat([df444w, df444x], axis=0)
        df444 = df444.sort_values(by="index")
        df444z = df444['Player'].str.split('>', expand = True)
        df444z.columns = ['Uno', 'Player', 'Tres', 'Cuatro']
        df444z = df444z.drop(['Uno', 'Tres', 'Cuatro'], axis=1)
        df444z['Player'] = df444z['Player'].str[:-6]
        df444 = df444.drop(['Player'], axis=1)
        df444 = pd.concat([df444z, df444], axis=1)
        df444 = df444.replace("-", 0)
        df444['Pases intentados'] = df444['Pases intentados'].astype(int)
        df444['Pases completos'] = df444['Pases completos'].astype(int)
        df444['Pases largos (%)'] = df444['Pases largos (%)'].str.replace("%", "")
        df444['Pases largos (%)'] = df444['Pases largos (%)'].str.replace(",", ".")
        df444['Pases largos (%)'] = df444['Pases largos (%)'].astype(float)
        df444['Precisión de pases (%)'] = df444['Precisión de pases (%)'].str.replace("%", "")
        df444['Precisión de pases (%)'] = df444['Precisión de pases (%)'].str.replace(",", ".")
        df444['Precisión de pases (%)'] = df444['Precisión de pases (%)'].astype(float)
        df444['Pases en campo rival'] = df444['Pases en campo rival'].astype(int)
        df444['% Pases completos en campo rival'] = df444['% Pases completos en campo rival'].str.replace("%", "")
        df444['% Pases completos en campo rival'] = df444['% Pases completos en campo rival'].str.replace(",", ".")
        df444['% Pases completos en campo rival'] = df444['% Pases completos en campo rival'].astype(float)
        df444['Pases completos en campo rival'] = round((df444['% Pases completos en campo rival']*df444['Pases en campo rival'])/100)
        df444['% Precisión de los pases en el último tercio de campo'] = df444['% Precisión de los pases en el último tercio de campo'].str.replace("%", "")
        df444['% Precisión de los pases en el último tercio de campo'] = df444['% Precisión de los pases en el último tercio de campo'].str.replace(",", ".")
        df444['% Precisión de los pases en el último tercio de campo'] = df444['% Precisión de los pases en el último tercio de campo'].astype(float)        
        df444['Through Balls'] = df444['Through Balls'].astype(int)
        df444['Pases al último tercio'] = df444['Pases al último tercio'].astype(int)
        df444['Pases al área contraria'] = df444['Pases al área contraria'].astype(int)
        df444['Centros con pelota en movimiento'] = df444['Centros con pelota en movimiento'].astype(int)
        df444['Good passes and crosses'] = df444['Good passes and crosses'].astype(int)
        lst = []
        aux = teamstatus
        for i in range(len(df444)):
            lst.append(aux)
        dfpss = pd.DataFrame([lst]).T
        dfpss.columns = ['Team']
        df444 = pd.concat([df444, dfpss], axis = 1)
        df444 = df444[['index', 'Team', 'Player', 'Pases intentados', 'Pases completos', 'Pases largos (%)', 'Precisión de pases (%)', 'Pases en campo rival', '% Pases completos en campo rival', '% Precisión de los pases en el último tercio de campo', 'Through Balls', 'Pases al último tercio', 'Pases al área contraria', 'Centros con pelota en movimiento', 'Good passes and crosses']]
        #st.dataframe(df444, use_container_width=True)
        return df444
    
    def aplicar_transformaciones_dfdefensa(df, teamstatus):
        df5 = df['six'].str.split("</tbody>", expand = True)
        df5.columns = ['Table', 'Code']
        df5 = df5.drop(['Code'], axis = 1)
        df55 = df5['Table'].str.split("<tr>", expand = True).T
        df55.columns = ['Events']
        df55.drop(df55.head(1).index,inplace=True)
        df55 = df55.reset_index()
        df55['Events'] = df55['Events'].str[24:]
        df5tit = df55['Events'].iloc[:1]
        df55.drop(df5.head(1).index,inplace=True)
        df55 = df55.drop(['index'], axis=1)
        df555 = df55['Events'].str.split("<td", expand = True)
        df555.columns = ['Player', 'Quites', '% Quites con recuperación', 'Despejes', 'Intercepciones', 'Pérdidas', 'Pelotas recuperadas', 'Faltas cometidas', 'Tarjetas amarillas', 'Tarjetas rojas']
        df555 = df555.reset_index()
        df555a = df555[df555['Quites'].str.contains('class="highest">')]
        df555b = df555[~df555['Quites'].str.contains('class="highest">')]
        df555a['Quites'] = df555a['Quites'].str[17:-5]
        df555b['Quites'] = df555b['Quites'].str[1:-5]
        df555 = pd.concat([df555a, df555b], axis=0)
        df555 = df555.sort_values(by="index")
        df555c = df555[df555['% Quites con recuperación'].str.contains('class="highest">')]
        df555d = df555[~df555['% Quites con recuperación'].str.contains('class="highest">')]
        df555c['% Quites con recuperación'] = df555c['% Quites con recuperación'].str[17:-5]
        df555d['% Quites con recuperación'] = df555d['% Quites con recuperación'].str[1:-5]
        df555 = pd.concat([df555c, df555d], axis=0)
        df555 = df555.sort_values(by="index")
        df555e = df555[df555['Despejes'].str.contains('class="highest">')]
        df555f = df555[~df555['Despejes'].str.contains('class="highest">')]
        df555e['Despejes'] = df555e['Despejes'].str[17:-5]
        df555f['Despejes'] = df555f['Despejes'].str[1:-5]
        df555 = pd.concat([df555e, df555f], axis=0)
        df555 = df555.sort_values(by="index")
        df555g = df555[df555['Intercepciones'].str.contains('class="highest">')]
        df555h = df555[~df555['Intercepciones'].str.contains('class="highest">')]
        df555g['Intercepciones'] = df555g['Intercepciones'].str[17:-5]
        df555h['Intercepciones'] = df555h['Intercepciones'].str[1:-5]
        df555 = pd.concat([df555g, df555h], axis=0)
        df555 = df555.sort_values(by="index")
        df555i = df555[df555['Pérdidas'].str.contains('class="highest">')]
        df555j = df555[~df555['Pérdidas'].str.contains('class="highest">')]
        df555i['Pérdidas'] = df555i['Pérdidas'].str[17:-5]
        df555j['Pérdidas'] = df555j['Pérdidas'].str[1:-5]
        df555 = pd.concat([df555i, df555j], axis=0)
        df555 = df555.sort_values(by="index")
        df555k = df555[df555['Pelotas recuperadas'].str.contains('class="highest">')]
        df555l = df555[~df555['Pelotas recuperadas'].str.contains('class="highest">')]
        df555k['Pelotas recuperadas'] = df555k['Pelotas recuperadas'].str[17:-5]
        df555l['Pelotas recuperadas'] = df555l['Pelotas recuperadas'].str[1:-5]
        df555 = pd.concat([df555k, df555l], axis=0)
        df555 = df555.sort_values(by="index")
        df555m = df555[df555['Faltas cometidas'].str.contains('class="highest">')]
        df555n = df555[~df555['Faltas cometidas'].str.contains('class="highest">')]
        df555m['Faltas cometidas'] = df555m['Faltas cometidas'].str[17:-5]
        df555n['Faltas cometidas'] = df555n['Faltas cometidas'].str[1:-5]
        df555 = pd.concat([df555m, df555n], axis=0)
        df555 = df555.sort_values(by="index")
        df555o = df555[df555['Tarjetas amarillas'].str.contains('class="highest">')]
        df555p = df555[~df555['Tarjetas amarillas'].str.contains('class="highest">')]
        df555o['Tarjetas amarillas'] = df555o['Tarjetas amarillas'].str[17:-5]
        df555p['Tarjetas amarillas'] = df555p['Tarjetas amarillas'].str[1:-5]
        df555 = df555.sort_values(by="index")
        df555 = pd.concat([df555o, df555p], axis=0)
        df555q = df555[df555['Tarjetas rojas'].str.contains('class="highest">')]
        df555r = df555[~df555['Tarjetas rojas'].str.contains('class="highest">')]
        df555q['Tarjetas rojas'] = df555q['Tarjetas rojas'].str[17:-10]
        df555r['Tarjetas rojas'] = df555r['Tarjetas rojas'].str[1:-10]
        df555 = pd.concat([df555q, df555r], axis=0)
        df555 = df555.sort_values(by="index")
        df555z = df555['Player'].str.split('>', expand = True)
        df555z.columns = ['Uno', 'Player', 'Tres', 'Cuatro']
        df555z = df555z.drop(['Uno', 'Tres', 'Cuatro'], axis=1)
        df555z['Player'] = df555z['Player'].str[:-6]
        df555 = df555.drop(['Player'], axis=1)
        df555 = pd.concat([df555z, df555], axis=1)
        df555 = df555.replace("-", 0)
        df555['Quites'] = df555['Quites'].astype(int)
        df555['% Quites con recuperación'] = df555['% Quites con recuperación'].str.replace("%", "")
        df555['% Quites con recuperación'] = df555['% Quites con recuperación'].str.replace(",", ".")
        df555['% Quites con recuperación'] = df555['% Quites con recuperación'].astype(float)
        df555['Quites con recuperación'] = round((df555['% Quites con recuperación']*df555['Quites'])/100)
        df555['Despejes'] = df555['Despejes'].astype(int)
        df555['Intercepciones'] = df555['Intercepciones'].astype(int)
        df555['Pérdidas'] = df555['Pérdidas'].astype(int)
        df555['Pelotas recuperadas'] = df555['Pelotas recuperadas'].astype(int)
        df555['Faltas cometidas'] = df555['Faltas cometidas'].astype(int)
        df555['Tarjetas amarillas'] = df555['Tarjetas amarillas'].astype(int)
        df555['Tarjetas rojas'] = df555['Tarjetas rojas'].astype(int)
        lst = []
        aux = teamstatus
        for i in range(len(df555)):
            lst.append(aux)
        dfpss = pd.DataFrame([lst]).T
        dfpss.columns = ['Team']
        df555 = pd.concat([df555, dfpss], axis = 1)
        df555 = df555[['index', 'Team', 'Player', 'Quites', '% Quites con recuperación', 'Despejes', 'Intercepciones', 'Pérdidas', 'Pelotas recuperadas', 'Faltas cometidas', 'Tarjetas amarillas', 'Tarjetas rojas']]
        #st.dataframe(df555, use_container_width=True)
        #st.markdown("""---""")
        return df555
    
    def aplicar_transformaciones_dfatajadas(df, teamstatus):
        df2 = df['thr'].str.split("</tbody>", expand = True)
        df2.columns = ['Table', 'Code']
        df2 = df2.drop(['Code'], axis = 1)
        df22 = df2['Table'].str.split("<tr>", expand = True).T
        df22.columns = ['Events']
        df22.drop(df22.head(1).index,inplace=True)
        df22 = df22.reset_index()
        df22['Events'] = df22['Events'].str[24:]
        df2tit = df22['Events'].iloc[:1]
        df22.drop(df2.head(1).index,inplace=True)
        df22 = df22.drop(['index'], axis=1)
        df222 = df22['Events'].str.split("<td", expand = True)
        df222.columns = ['Player', 'Atajadas totales', 'Remates recibidos', '% de atajadas', 'Sweeper Keeper Total', 'Sweeper Keeper Success', 'Crosses Claimed', 'Crosses Not Claimed', 'Despejes de puño']
        df222a = df222[df222['Atajadas totales'].str.contains('class="highest">')]
        df222b = df222[~df222['Atajadas totales'].str.contains('class="highest">')]
        df222a['Atajadas totales'] = df222a['Atajadas totales'].str[17:-5]
        df222b['Atajadas totales'] = df222b['Atajadas totales'].str[1:-5]
        df222 = pd.concat([df222a, df222b], axis=0)
        df222c = df222[df222['Remates recibidos'].str.contains('class="highest">')]
        df222d = df222[~df222['Remates recibidos'].str.contains('class="highest">')]
        df222c['Remates recibidos'] = df222c['Remates recibidos'].str[17:-5]
        df222d['Remates recibidos'] = df222d['Remates recibidos'].str[1:-5]
        df222 = pd.concat([df222c, df222d], axis=0)
        df222e = df222[df222['% de atajadas'].str.contains('class="highest">')]
        df222f = df222[~df222['% de atajadas'].str.contains('class="highest">')]
        df222e['% de atajadas'] = df222e['% de atajadas'].str[17:-5]
        df222f['% de atajadas'] = df222f['% de atajadas'].str[1:-5]
        df222 = pd.concat([df222e, df222f], axis=0)
        
        
        lst = []
        aux = teamstatus
        for i in range(len(df222)):
            lst.append(aux)
        dfpss = pd.DataFrame([lst]).T
        dfpss.columns = ['Team']
        df222 = pd.concat([df222, dfpss], axis = 1)
        #st.dataframe(df222, use_container_width=True)
        #st.markdown("""---""")
        return df222
    
    if seloption == "Home":
        datos = tablecode.split("<thead>")
        df = pd.DataFrame([datos])
        df.columns = ['one', 'two', 'thr', 'fou', 'fiv', 'six']
        df = df.drop(['one'], axis=1)
        dfc = df
        st.markdown("""---""")
        dfgeneral = aplicar_transformaciones_dfgeneral(df, teamstatus)
        st.title("GENERAL")
        st.dataframe(dfgeneral, use_container_width=True)
        st.markdown("""---""")
        dfataque = aplicar_transformaciones_dfataque(df, teamstatus)
        st.title("ATAQUE")
        st.dataframe(dfataque, use_container_width=True)
        st.markdown("""---""")
        dfdistribucion = aplicar_transformaciones_dfataque(df, teamstatus)
        st.title("DISTRIBUCIÓN")
        st.dataframe(dfdistribucion, use_container_width=True)
        st.markdown("""---""")
        dfdefensa = aplicar_transformaciones_dfdefensa(df, teamstatus)
        st.title("DEFENSA")
        st.dataframe(dfdefensa, use_container_width=True)
        st.markdown("""---""")
        dfatajadas = aplicar_transformaciones_dfatajadas(df, teamstatus)
        st.title("ATAJADAS")
        st.dataframe(dfatajadas, use_container_width=True)
        st.markdown("""---""")
        
    if seloption == "Away":
        datos = tablecode2.split("<thead>")
        df = pd.DataFrame([datos])
        df.columns = ['one', 'two', 'thr', 'fou', 'fiv', 'six']
        df = df.drop(['one'], axis=1)
        dfc = df
        st.markdown("""---""")
        dfgeneral = aplicar_transformaciones_dfgeneral(df, teamstatus2)
        st.title("GENERAL")
        st.dataframe(dfgeneral, use_container_width=True)
        st.markdown("""---""")
        dfataque = aplicar_transformaciones_dfataque(df, teamstatus2)
        st.title("ATAQUE")
        st.dataframe(dfataque, use_container_width=True)
        st.markdown("""---""")
        dfdistribucion = aplicar_transformaciones_dfataque(df, teamstatus2)
        st.title("DISTRIBUCIÓN")
        st.dataframe(dfdistribucion, use_container_width=True)
        st.markdown("""---""")
        dfdefensa = aplicar_transformaciones_dfdefensa(df, teamstatus2)
        st.title("DEFENSA")
        st.dataframe(dfdefensa, use_container_width=True)
        st.markdown("""---""")
        dfatajadas = aplicar_transformaciones_dfatajadas(df, teamstatus2)
        st.title("ATAJADAS")
        st.dataframe(dfatajadas, use_container_width=True)
        st.markdown("""---""")
        
    if seloption == "All":
        datos_home = tablecode.split("<thead>")
        df_home = pd.DataFrame([datos_home])
        df_home.columns = ['one', 'two', 'thr', 'fou', 'fiv', 'six']
        df_home = df_home.drop(['one'], axis=1)
        dfc_home = df_home
        datos_away = tablecode2.split("<thead>")
        df_away = pd.DataFrame([datos_away])
        df_away.columns = ['one', 'two', 'thr', 'fou', 'fiv', 'six']
        df_away = df_away.drop(['one'], axis=1)
        dfc_away = df_away
        st.markdown("""---""")
        
        dfgeneral_home = aplicar_transformaciones_dfgeneral(df_home, teamstatus)
        dfgeneral_away = aplicar_transformaciones_dfgeneral(df_away, teamstatus2)
        dfgeneral_all = pd.concat([dfgeneral_home, dfgeneral_away], axis=0)
        st.title("GENERAL")
        
        st.dataframe(dfgeneral_all, use_container_width=True)
        st.markdown("""---""")
        
        dfataque_home = aplicar_transformaciones_dfataque(df_home, teamstatus)
        dfataque_away = aplicar_transformaciones_dfataque(df_away, teamstatus2)
        dfataque_all = pd.concat([dfataque_home, dfataque_away], axis=0)
        st.title("ATAQUE")
        st.write(dfataque_all)
        st.markdown("""---""")
        
        dfdistribucion_home = aplicar_transformaciones_dfdistribucion(df_home, teamstatus)
        dfdistribucion_away = aplicar_transformaciones_dfdistribucion(df_away, teamstatus2)
        dfdistribucion_all = pd.concat([dfdistribucion_home, dfdistribucion_away], axis=0)
        st.title("DISTRIBUCIÓN")
        st.write(dfdistribucion_all)
        st.markdown("""---""")
        
        dfdefensa_home = aplicar_transformaciones_dfdefensa(df_home, teamstatus)
        dfdefensa_away = aplicar_transformaciones_dfdefensa(df_away, teamstatus2)
        dfdefensa_all = pd.concat([dfdefensa_home, dfdefensa_away], axis=0)
        st.title("DEFENSA")
        st.write(dfdefensa_all)
        st.markdown("""---""")
        
        dfatajadas_home = aplicar_transformaciones_dfatajadas(df_home, teamstatus)
        dfatajadas_away = aplicar_transformaciones_dfatajadas(df_away, teamstatus2)
        dfatajadas_all = pd.concat([dfatajadas_home, dfatajadas_away], axis=0)
        st.title("ATAJADAS")
        st.write(dfatajadas_all)
        st.markdown("""---""")
        
