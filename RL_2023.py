
# 1.Importation des librairies nécessaires pour le script
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
#import scrapy
import re
import requests

import json
from pandas.io.json import json_normalize

import pandas as pd
import numpy as np
import datetime as dt  #pour l'ajout de la date de l'extraction de données
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import os

import time

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

import streamlit as st
from streamlit_option_menu import option_menu

## Import the required library
#from geopy.geocoders import Nominatim

import altair as alt



# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(page_title="Rentree Litteraire", page_icon="books", layout="wide")

st.write("RL_2023 GO")

#df_rl_total = pd.read_pickle("liste_rl_total.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/
#df_rl_total.tail(2)

@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df_rl_dataviz = pd.read_pickle(url)
    return df_rl_dataviz

### A. Sidebar

with st.sidebar:
	st.success("Select an add method.")
	st.title('RENTRÉE LITTÉRAIRE & PRIX LITTÉRAIRES')
	st.header('2023')

### B. Container 1
cont_1 = st.container()
cont_metric = st.container()
cont_geo = st.container()
with cont_1:
	df_rl_dataviz = load_data("liste_rl_total_sans_doublon.pkl") #### Import pickel pour dataviz
	df_rl_dataviz = df_rl_dataviz.loc[df_rl_dataviz.RL == 'RL']
	st.dataframe(df_rl_dataviz.head())

	st.button("Rerun")

with cont_metric :
	col_metric, col_graph_saiso, col_graph_genre = st.columns([2,4,4])
	with col_metric : 
		st.metric(label="Livres", value=len(df_rl_dataviz.EAN.unique()))
		st.metric(label="Editeurs", value = len(df_rl_dataviz.Editeur.unique()))
		st.metric(label="Premiers romans", value = len(df_rl_dataviz.loc[df_rl_dataviz['PREMIER_ROMAN']=='PREMIER ROMAN']))
	with col_graph_saiso :
		df_rl_dataviz_saiso = df_rl_dataviz['MOIS'].value_counts().reset_index().rename(columns={'index':'Mois','MOIS':"Nb ouvrages"}).sort_values(by='Mois')
		#st.dataframe(df_rl_dataviz_saiso) 
		st.bar_chart(df_rl_dataviz_saiso, x='Mois', y="Nb ouvrages")
	with col_graph_genre : 
		## Create subplots: use 'domain' type for Pie subplot
		fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
		df_rl_dataviz_genre = df_rl_dataviz.GENRE.value_counts().reset_index()
		#st.dataframe(df_rl_dataviz_genre) #fig.update_layout(height=800)
		fig.add_trace(go.Pie(labels=df_rl_dataviz_genre['index'], values=round(df_rl_dataviz_genre.GENRE,0), name="Casting",
							 title='Nb de roman par genre', hole=.3))
		st.plotly_chart(fig,theme=None,use_container_width=True)

with cont_geo:
	col_map, col_geo_chart = st.columns([4,2])
	df_rl_dataviz_geo = df_rl_dataviz[['PAYS','latitude','longitude','CONTINENT','EAN']].loc[df_rl_dataviz.RL == 'RL'].groupby(['PAYS','latitude','longitude','CONTINENT']).count().reset_index()
	
	continent_color = {'EUROPE' : '#00b6cb',
	'NORTH AMERICA': '#124559',
	'ASIA' : '#5e35b1',
	'AFRICA' : '#7cb342',
	'SOUTH AMERICA' : '#598392',
	'CENTRAL AMERICA' : '#aec3b0',
	'OCEANIA' : '#ff7043',
	'CARIBBEAN' : '#f2bedb'}
	
	df_rl_dataviz_geo.insert(4, 'continent_color', df_rl_dataviz_geo.CONTINENT.apply(lambda c :continent_color[c]))
	with col_map : 
		st.map(df_rl_dataviz_geo,
		    latitude='latitude',
		    longitude='longitude',
			size=150,
			color='continent_color')

	with col_geo_chart :
		#st.dataframe(df_rl_dataviz_geo.sort_values('EAN', ascending = False))
		fig=px.bar(df_rl_dataviz_geo.sort_values('EAN', ascending = False).head(10), x='EAN',y='PAYS', orientation='h')
		st.write(fig)
