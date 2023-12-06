
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

import pickle



# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(page_title="Rentree Litteraire", page_icon="books", layout="wide")

st.write("RL_2023 GO")

#df_rl_total = pd.read_pickle("liste_rl_total.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/
#df_rl_total.tail(2)

@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df_rl_dataviz = pd.read_pickle(url) #"./dict_rl_final_23.pkl" pd.DataFrame.from_dict(pd.read_pickle(url)).T
    return df_rl_dataviz

@st.cache_data  # 👈 Add the caching decorator
def load_data_dict(url):
    df_rl_dataviz_pl = pd.read_pickle(url) #"./dict_rl_final_23.pkl" pd.DataFrame.from_dict(pd.read_pickle(url)).T
    return df_rl_dataviz_pl

#je charge le dictionnaire 
dico_rl_dataviz = load_data_dict("docs/dict_rl_final_20231126.pkl")


### B. Container 1
cont_1 = st.container()
cont_metric = st.container()
cont_geo = st.container()
cont_prix_litt = st.container()

with cont_1:
	with st.expander('dataframes') : 
		df_rl_dataviz = load_data("liste_rl_total_sans_doublon.pkl") #### Import pickel pour dataviz  
		df_rl_dataviz = df_rl_dataviz.loc[df_rl_dataviz.RL == 'RL']
	
	
		#je transforme le dictionnaire en dataframe
		df_rl_dataviz_pl = pd.DataFrame.from_dict(dico_rl_dataviz, orient='index')
	
		#affichage du dataframe créé depuis le dico
		st.subheader("dataframe from dico")
		st.dataframe(df_rl_dataviz_pl.head(2))

		st.divider()
	
		st.subheader("Filter of dataframe from dico")
		#l'idée est de filtrer sur les ouvrages identifié comme ouvrage de la rentrée littéraire
		# Filtre => unique les livres RL
		list_livre_rl = list(filter(lambda x: x['livre']['RL'] != '', dico_rl_dataviz.values()))
		df_list_livre_rl = pd.DataFrame(list_livre_rl)
		st.dataframe(df_list_livre_rl.head(2))
		st.write(len(df_list_livre_rl))

		#st.button("Rerun")