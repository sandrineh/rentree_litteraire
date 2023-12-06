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

st.sidebar.success("Select a demo above.")

st.dataframe(df_rl_total_test.tail(2))


# 1. Find a book by the Editor name "Emmanuelle"
editeur = st.selectbox("Pick one", list(df_rl_total_test['Editeur'].unique()))

find_editeur = df_rl_total_test.loc[df_rl_total_test['Editeur'].str.contains(editeur) ==True] #, ['Genre']] = 'F'
st.dataframe(find_editeur)

# 2. choice of a method to add info for a book or add a book

with st.form("ajout_manuel"):
	nb_index = st.number_input('index')
	prem_roman = st.selectbox('PREMIER ROMAN', ['OUI', 'NON'])
	quel_genre = st.selectbox('genre', ['F', 'M'])
	quel_pays = st.selectbox("Pays", list(df_rl_total_test['PAYS'].unique()))
	quel_continent = st.selectbox("Continent", list(df_rl_total_test['CONTINENT'].unique()))
	trad_de = st.selectbox("Traduit de", list(df_rl_total_test['Traduit de'].unique()))
	trad_par = st.text_input('Traduit par')
	ean = st.text_input('EAN')
	titre = st.text_input('titre')
	auteur = st.text_input('auteur')
	date_parution = st.text_input('Date de parution')
	mois= st.selectbox('MOIS', ['August', 'September','October'])
	annee_parution = st.number_input('ANNEE_PUBLICATION')
	url = st.text_input('url')
	categorie = st.text_input('categorie-liste')
	prix_gf = st.text_input('prix_gf')
	prix_ebook = st.text_input('prix_ebook ou pas de prix ebook')
	couverture= st.text_input('url couv ou pas de visuel')
	editeur = st.text_input('Editeur')
	isbn = st.text_input('ISBN')
	format = st.selectbox('genre', ['Grand Format', 'Poche'])
	presentation = st.text_input('Présentation')
	nb_pages = st.text_input('nb pages')
	poids = st.text_input('Poids')
	dimension= st.text_input('Dimensions')
	collection = st.text_input('Collection') 
	st.form_submit_button('Submit my picks')

if quel_pays == None :
	quel_pays = st.text_input("ajout pays")

if trad_de == None :
	trad_de = st.text_input("ajout langue")

dict_manuel = {'RL' : ['RL'],
			   'PREMIER_ROMAN' : [prem_roman], #PREMIER ROMAN NON
				'TYPES' : ['Romans étrangers'], #Essais Romans étrangers Romans français
				'GENRE' : [quel_genre],
				'PAYS' : [quel_pays],
				'CONTINENT' : [quel_continent],
				'Traduit de' : [trad_de],
				'Traduit par' : [trad_par],
				'EAN' : [ean],
				'titre' : [titre],
				'auteur' : [auteur],
				'Date de parution' : [date_parution],
				'MOIS' : [mois], #August September October
				'ANNEE_PUBLICATION' : [annee_parution],
				'url' : [url],
				'categorie' : [[categorie]],
				'prix_gf' : [prix_gf + ' €'],
				'prix_ebook' : [prix_ebook], #pas de prix ebook 15,99 €
				'couverture' : [couverture], #pas de visuel
				'caracteristiques' : ['Date de parution|'+date_parution+'|editeur|'+editeur+'|ISBN|'+isbn+'|EAN|'+ean+'|Format|'+format+'|Présentation|'+presentation+'|Nb. de pages|'+nb_pages+' pages|Poids|'+poids+' kg|Dimensions|'+dimension+'|Collection|'+collection],
				'Editeur' : [editeur],
				'ISBN' : [isbn],
				'Format' : [format], #Grand Format Poche
				'Présentation' : [presentation],
				'Nb. de pages' : [nb_pages+'pages'],
				'Poids' : [poids+'kg'],
				'Dimensions' : [dimension], #14cm x 22cm
				'Collection' : [collection]}

df1 = pd.DataFrame(dict_manuel, index=[int(nb_index)])

df_rl_total_test = pd.concat([df_rl_total_test, df1])


# export au format pickle
df_rl_total_test.to_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/

df_rl_total_test = pd.read_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/
st.dataframe(df_rl_total_test.tail(2))
