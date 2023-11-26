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

import pickle


# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(page_title="Rentree Litteraire 2023", page_icon="books", layout="wide")

st.header("RL_2023 - Ajout Prix Littéraire")

#### Import pickel de la liste de livre sous forme de dictionnaire
#@st.cache_data  # 👈 Add the caching decorator
#def load_data(dico):
#    dico_rl_pl = pd.read_pickle(dico)
#    return dico_rl_pl

dico_rl_pl_23 = pd.read_pickle("./dict_rl_final_23.pkl") #load_data("./dict_rl_23.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/

st.session_state['dico'] = dico_rl_pl_23

#st.write(st.session_state['dico'][379])

df_rl_pl_23 = pd.DataFrame(dico_rl_pl_23).T 

st.sidebar.write("Page pour mettre à jour la bdd \navec les infos autour des prix littéraire 2023")

st.dataframe(df_rl_pl_23.head(2))


# 1. Find an author by his/her name
col_find_author, col_vide, col_result_find_author = st.columns([2,1,4])
with col_find_author :
	st.subheader("1. Find the index of an auhor")
	auteur = st.selectbox("Chosse a name", list(df_rl_pl_23['nom_complet'].unique()))

	find_auteur = df_rl_pl_23.loc[df_rl_pl_23['nom_complet'] == auteur]
	index_find_auteur = int(find_auteur.index[0])
	
	st.dataframe(find_auteur)

	st.write(dico_rl_pl_23[index_find_auteur]["livre"]["prix_litteraire"])

	
# 2. add a book price according to the author's index
    #list of book prices and their id

with col_result_find_author :
	st.subheader("2. Add a book price according to the author's index")
	df_liste_pl = pd.DataFrame(
	list(zip(['Prix Alain Spiess','FEMINA','FEMINA','FEMINA','FEMINA','Grand Prix de l\'Académie Française','Prix André Malraux','Prix André Malraux','Prix André Malraux','Prix de Flore','Prix Décembre','Prix Goncourt','Prix Goncourt','Prix Interallié','Prix Wepler','Prix Wepler','RENAUDOT','RENAUDOT','RENAUDOT','Prix Medicis','Prix Medicis','Prix Medicis'],
	['Prix Alain Spiess du deuxième roman','FEMINA_FRANCAIS','FEMINA_ETRANGER','FEMINA_ESSAI','FEMINA_LYCEENS','Grand Prix de l\'Académie Française','Prix André Malraux_LITT_ENGAGEE','Prix André Malraux_ESSAI_ART','Prix André Malraux_PRIX-JURY','Prix de Flore','Prix Décembre','Prix Goncourt','Prix Goncourt des Lycéens','Prix Interallié','Prix Wepler-Fondation La Poste','Prix Wepler-Fondation La Poste - Mention special jury','RENAUDOT_ROMAN','RENAUDOT_ESSAI','Prix Renaudot des lycéens','Prix Medicis_FR','Prix Medicis_ET','Prix Medicis_ESSAIS'],
	['1AS','2FE','2FE','2FE','2FE','3AF','4AM','4AM','4AM','5FL','6DE','7GO','7GO','8IN','9WE','9WE','10RE','10RE','10RE','11ME','11ME','11ME'],['1AS1','2FE1FR','2FE2ET','2FE3ES','2FE4LY','3AF1','4AM1LI','4AM2ES','4AM3PJ','5FL1','6DE1','7GO1','7GO2LY','8IN1','9WE1','9WE2PJ','10RE1RO','10RE2ES','10RE3LY','11ME1FR','11ME2ET','11ME3ES'])), columns=['PRIX','PRIX_DETAIL','ID_PRIX','ID_PRIX_DETAIL'])
	
	#st.dataframe(df_liste_pl.head(2))
	st.write(index_find_auteur)
	nom_prix = st.selectbox("nom_prix", list(df_liste_pl['PRIX'].unique()), index = None)
	id_prix = df_liste_pl.loc[df_liste_pl['PRIX'] == nom_prix]['ID_PRIX'].unique()[0]
	st.write(id_prix)
	nom_prix_detail = st.selectbox('nom_prix_detail', list(df_liste_pl.loc[df_liste_pl['PRIX'] == nom_prix]['PRIX_DETAIL'].unique()), index = None)
	id_prix_detail = df_liste_pl.loc[df_liste_pl['PRIX_DETAIL'] == nom_prix_detail]['ID_PRIX_DETAIL'].unique()[0]
	st.write(id_prix_detail)
	premiere_selection = st.selectbox('premiere_selection', ['OUI', 'NON', 'PAS DE SELECTION SUPP'])
	deuxieme_selection = st.selectbox('deuxieme_selection', ['NON', 'OUI', 'PAS DE SELECTION SUPP'])
	troisieme_selection = st.selectbox('troisieme_selection', ['PAS DE SELECTION SUPP', 'NON', 'OUI'])
	laureat = st.selectbox('lauréat', ['NON', 'OUI'])

	add_to_dict = {'id_prix': id_prix,
	 'nom_prix': nom_prix,
	 'id_prix_detail': id_prix_detail,
	 'nom_prix_detail': nom_prix_detail,
	 'annee': '2023',
	 'premiere_selection': premiere_selection,
	 'deuxieme_selection': deuxieme_selection,
	 'troisieme_selection': troisieme_selection,
	 'lauréat': laureat}
				
	index_pl = st.number_input('which index ?')
	
	add_price = st.button('add a price')
	replace_price = st.button('modif a price')
	#delete_price = st.button('delete a price')

	if add_price :
		st.session_state['dico'][index_find_auteur]["livre"]["prix_litteraire"].setdefault( index_pl, add_to_dict)
	elif replace_price :
		st.session_state['dico'][index_find_auteur]["livre"]["prix_litteraire"][index_pl] = add_to_dict
		
	#if delete_price : 
		#st.session_state['dico'][index_find_auteur]["livre"]["prix_litteraire"].pop(index_pl)
	
	st.write(st.session_state['dico'][index_find_auteur]["livre"]["prix_litteraire"][index_pl])

	#st.session_state['dico'][158]["livre"]["prix_litteraire"][1]['lauréat'] = 'OUI'
	#st.session_state['dico'][316]["livre"]["prix_litteraire"].pop(2)
	with open('./dict_rl_final_23.pkl', 'wb') as fp:
		pickle.dump(st.session_state['dico'], fp)

	st.write(st.session_state['dico'][index_find_auteur]['livre']['titre'])
	
	
	
		
#df_rl_dataviz = load_data("liste_rl_total_sans_doublon.pkl") #### Import pickel pour dataviz  
#	df_rl_dataviz = df_rl_dataviz.loc[df_rl_dataviz.RL == 'RL']
#	dico_rl_dataviz = load_data_dict("./dict_rl_final_23.pkl")
#	dico_if_rl_dataviz = {e:r for e,r in zip(df_rl_dataviz['EAN'], df_rl_dataviz['RL'])}
#	
#	df_rl_dataviz_pl = pd.DataFrame.from_dict(load_data_dict("./dict_rl_final_23.pkl")).T
#	st.write("dico")
#	
#	
#	for k in dico_rl_dataviz.keys() : 
#		e = dico_rl_dataviz[k]['livre']['ean']
#		if e in dico_if_rl_dataviz.keys() :
#			dico_rl_dataviz[k]['livre']['RL'] = 'RL'
#		else :
#			dico_rl_dataviz[k]['livre']['RL'] = ''
#			

#	with open('./dict_rl_final_20231126.pkl', 'wb') as fp:
#		pickle.dump(dico_rl_dataviz, fp)#