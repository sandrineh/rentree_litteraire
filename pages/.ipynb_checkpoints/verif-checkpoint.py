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

st.write(len(df_rl_total_test.loc[df_rl_total_test.RL == 'RL']))


# PAYS
cont_pays = st.container()
with cont_pays:
	st.subheader("PAYS")
	df_rl_total_test['PAYS'] = df_rl_total_test['PAYS'].apply(lambda p :str(p).upper())
	
	col_df_pays, col_pr_correction_pays,col_correction_pays = st.columns([2,4,2])
	
	with col_df_pays :
		st.dataframe(df_rl_total_test.loc[df_rl_total_test.RL == 'RL'].value_counts('PAYS'))
		
	with col_pr_correction_pays : 
		st.dataframe(df_rl_total_test.loc[(df_rl_total_test.RL == 'RL') & (df_rl_total_test.PAYS == '')])
	
		
	with col_correction_pays :
		with st.form("my_form"):
			nb_index = st.number_input('index')
			quel_pays = st.selectbox("Pays", list(df_rl_total_test['PAYS'].unique()), index = None)
			pays_submit = st.form_submit_button('Corriger le pays')

			if pays_submit : 
				df_rl_total_test.loc[nb_index,'PAYS'] = quel_pays
			
			df_rl_total_test.to_pickle("./liste_rl_total_test.pkl")

# CONTINENT
cont_continent = st.container()
with cont_continent:
	st.subheader("CONTINENT")
	#df_rl_total_test['CONTINENT'] = df_rl_total_test['CONTINENT'].apply(lambda p :str(p).upper())	
	#df_rl_total_test.to_pickle("./liste_rl_total_test.pkl")
	
	col_df_conti, col_pr_correction_conti,col_correction_conti = st.columns([2,4,2])
	
	with col_df_conti :
		st.dataframe(df_rl_total_test.loc[df_rl_total_test.RL == 'RL'].value_counts('CONTINENT').reset_index())

	with col_pr_correction_conti : 
		continent = st.selectbox("Pick continent", list(df_rl_total_test['CONTINENT'].unique()))
		pays_continent = st.selectbox("Pick pays", list(df_rl_total_test.loc[df_rl_total_test['CONTINENT'] == continent]['PAYS'].unique()))
		find_continent = df_rl_total_test.loc[(df_rl_total_test.RL == 'RL') & (df_rl_total_test['CONTINENT'] == continent) & (df_rl_total_test['PAYS'] == pays_continent)]
		st.dataframe(find_continent)
		
	with col_correction_conti :
		with st.form("continent à corriger"):
			
			#continent_erreur = st.selectbox("ancien continent", list(df_rl_total_test['CONTINENT'].unique()))
			continent_correction = st.selectbox("nouveau continent ", ['NORTH AMERICA', 'CENTRAL AMERICA', 'SOUTH AMERICA', 'CARIBBEAN',
																	   'EUROPE', 'ASIA','AFRICA', 'MIDDLE EAST' ,'OCEANIA'])
			conti_submit = st.form_submit_button('Corriger le continent')

			if conti_submit :
				df_rl_total_test.loc[ df_rl_total_test.PAYS == pays_continent,'CONTINENT'] = continent_correction
			
			#df_rl_total_test['CONTINENT'] = df_rl_total_test['CONTINENT'].apply(lambda c : c.replace('AFRIQUE', 'AFRICA'))
			
			df_rl_total_test.to_pickle("./liste_rl_total_test.pkl")
		
# AUTEUR
cont_auteur = st.container()
with cont_auteur:
	st.subheader("AUTEUR")
	col_count_auteur, col_auteur_df, col_auteur_correc = st.columns([2,4,2])
	with col_count_auteur : 
		st.dataframe(df_rl_total_test.loc[df_rl_total_test.RL == 'RL']['auteur'].value_counts())
		
	with col_auteur_df : 
		author = st.selectbox("Pick auteur", list(df_rl_total_test['auteur'].unique()))
		find_author = df_rl_total_test.loc[(df_rl_total_test.RL == 'RL') & (df_rl_total_test['auteur'] == author)]		# 
		st.dataframe(find_author)
		
	with col_auteur_correc :
		with st.form("auteur à corriger"):
			ean = st.text_input("EAN")
			new_auteur = st.text_input("new auteur")
			author_submit = st.form_submit_button('Corriger auteur')

			if author_submit :
				df_rl_total_test.loc[ df_rl_total_test.EAN == ean,'auteur'] = new_auteur
			
				df_rl_total_test.to_pickle("./liste_rl_total_test.pkl")


# TITRE BOUBLON
cont_titre = st.container()
with cont_titre:
	df_doublon = pd.read_pickle("./liste_rl_total_sans_doublon.pkl")
	st.subheader("TITRE")
	col_count_titre, col_titre_df, col_titre_correc = st.columns([2,4,2])
	with col_count_titre : 
		st.dataframe(df_doublon['EAN'].value_counts(ascending = False)>=2) #.loc[df_rl_total_test.RL == 'RL']
		
	with col_titre_df : 
		titre_ean = st.selectbox("Pick titre", list(df_rl_total_test['EAN'].unique()))
		find_titre = df_rl_total_test.loc[(df_rl_total_test['EAN'] == titre_ean)] #(df_rl_total_test.RL == 'RL') & 
		st.dataframe(find_titre)
		#st.write(find_titre.to_dict('index'))
		
	with col_titre_correc :
		with st.form("drop titre doublon"):
			row_nb = int(st.number_input('which row number ?'))
			drop_duplicate_titre_submit = st.form_submit_button('drop duplicate titre')
			
			if drop_duplicate_titre_submit :
				df_doublon = df_doublon.drop(index = row_nb)
				df_doublon.to_pickle("./liste_rl_total_sans_doublon.pkl")
		
	st.dataframe(df_doublon[['EAN','titre','Date de parution','ANNEE_PUBLICATION','MOIS']])




#CONTINENT
#### EUROPE
#### NORTH AMERICA
#### ASIA
#### AFRICA
#### SOUTH AMERICA
#### MIDDLE EAST
#### CENTRAL AMERICA
#### OCEANIA

