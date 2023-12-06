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


# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(page_title="Rentree Litteraire", page_icon="books", layout="wide")

st.write("RL_2023 GO")

#### Import pickel pour test

df_rl_total_test = pd.read_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/


st.sidebar.success("Select and add method.")

st.dataframe(df_rl_total_test.tail(2))


# 1. Find a book by the Editor name "Emmanuelle"
editeur = st.selectbox("Pick one", list(df_rl_total_test['Editeur'].unique()))

find_editeur = df_rl_total_test.loc[df_rl_total_test['Editeur'] == editeur] #, ['Genre']] = 'F'
st.dataframe(find_editeur)

# 2. choice of a method to add info for a book or add a book

with st.form("my_form"):
	st.write("Inside the form")
	nb_index = st.number_input('index')
	types_livre = st.selectbox("type livre", ['Romans français' , 'Essais', 'Romans étrangers'])
	prem_roman = st.selectbox('PREMIER ROMAN', ['OUI', 'NON'])
	quel_genre = st.selectbox('genre', ['F', 'M', 'NB'])
	quel_pays = st.selectbox("Pays", list(df_rl_total_test['PAYS'].unique()), index = None)
	quel_continent = st.selectbox("Continent", list(df_rl_total_test['CONTINENT'].unique()), index = None)
	trad_de = st.selectbox("Traduit de", list(df_rl_total_test['Traduit de'].unique()), index = None)
	trad_par = st.text_input('Traduit par')
	st.form_submit_button('Submit my picks')

#if quel_pays == None:
#	quel_pays = st.text_input("ajout pays")
#
#if trad_de == None :
#	trad_de = st.text_input("ajout langue")
#
#if quel_continent == None :
#	quel_continent = st.text_input("ajout continent")

#nb_index = float(nb_index)
df_rl_total_test.loc[int(nb_index),'RL'] = 'RL'
df_rl_total_test.loc[int(nb_index),'TYPES'] = types_livre 
df_rl_total_test.loc[int(nb_index),'PREMIER_ROMAN'] = prem_roman #'PREMIER ROMAN'
df_rl_total_test.loc[int(nb_index),'TYPES'] = types_livre
df_rl_total_test.loc[int(nb_index),'GENRE'] = quel_genre
df_rl_total_test.loc[int(nb_index),'PAYS'] = quel_pays
df_rl_total_test.loc[int(nb_index),'CONTINENT'] = quel_continent #'EUROPE'
df_rl_total_test.loc[int(nb_index),'Traduit de'] = trad_de
df_rl_total_test.loc[int(nb_index),'Traduit par'] = trad_par


# export au format pickle
df_rl_total_test.to_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/

df_rl_total_test = pd.read_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/
st.dataframe(df_rl_total_test.tail(2))
