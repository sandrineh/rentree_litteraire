# 1.Importation des librairies nécessaires pour le script
from urllib.request import Request, urlopen
#from bs4 import BeautifulSoup
#import scrapy
import re
import requests

import json
#from pandas.io.json import json_normalize

import pandas as pd
import numpy as np
import datetime as dt  #pour l'ajout de la date de l'extraction de données
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import os

import time

#from plotly.subplots import make_subplots
#import plotly.graph_objects as go
#import plotly.express as px

import streamlit as st
from streamlit_option_menu import option_menu



#import folium 
#from streamlit_folium import folium_static


# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(page_title="Rentree Litteraire", page_icon="books", layout="wide")

st.write("RL_2023 GO")

st.sidebar.success("Select and add method.")

#### Import pickel pour test

df_rl_total_test = pd.read_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/


st.dataframe(df_rl_total_test.tail(2))


st.write(len(df_rl_total_test.loc[df_rl_total_test.RL == 'RL']))

df_rl_total_gp = df_rl_total_test[['PAYS','latitude','longitude','CONTINENT','EAN']].loc[df_rl_total_test.RL == 'RL'].groupby(['PAYS','latitude','longitude','CONTINENT']).count().reset_index()

continent_color = {'EUROPE' : '#00b6cb',
'NORTH AMERICA': '#124559',
'ASIA' : '#5e35b1',
'AFRICA' : '#7cb342',
'SOUTH AMERICA' : '#598392',
'CENTRAL AMERICA' : '#aec3b0',
'OCEANIA' : '#ff7043',
'CARIBBEAN' : '#f2bedb'}

df_rl_total_gp.insert(4, 'continent_color', df_rl_total_gp.CONTINENT.apply(lambda c :continent_color[c]))

st.dataframe(df_rl_total_gp.sort_values('EAN', ascending = False))

st.map(df_rl_total_gp,
    latitude='latitude',
    longitude='longitude',
	size=150,
	color='continent_color')
    #
#CONTINENT
#### EUROPE #00b6cb
#### NORTH AMERICA #124559
#### ASIA #5e35b1
#### AFRICA #7cb342
#### SOUTH AMERICA #598392
#### MIDDLE EAST
#### CENTRAL AMERICA #aec3b0
#### OCEANIA   #ff7043

### A. GET latitude and longitude for each country + save as a pickle file
#geoloc_df = pd.DataFrame(df_rl_total_test['PAYS'].unique(), columns=['PAYS'])
#
##st.dataframe(geoloc_df)
#
## Initialize Nominatim API
#geolocator = Nominatim(user_agent="MyApp")
#
#geoloc_df.insert(1, 'latitude', geoloc_df.PAYS.apply(lambda p : geolocator.geocode(p).latitude))
#geoloc_df.insert(2, 'longitude', geoloc_df.PAYS.apply(lambda p : geolocator.geocode(p).longitude))
#
#st.dataframe(geoloc_df)
#
#geoloc_df.to_pickle("./geoloc.pkl")		


### B. then add longitude et latitude into the principal dataframe + Save as pickle
#geoloc_df = pd.read_pickle("./geoloc.pkl")
#
#geoloc_dict = {p : [la, lo] for p,la,lo in zip(geoloc_df['PAYS'],geoloc_df['latitude'],geoloc_df['longitude'])} #geoloc_df.to_dict('index')
#
#df_rl_total_test.insert(9, 'latitude', df_rl_total_test.PAYS.apply(lambda p :geoloc_dict[p][0]))
#df_rl_total_test.insert(10, 'longitude', df_rl_total_test.PAYS.apply(lambda p :geoloc_dict[p][1]))

#df_rl_total_test.to_pickle("./liste_rl_total_test.pkl")