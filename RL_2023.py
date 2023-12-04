
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


if 'select_prix_liit' not in st.session_state:
	st.session_state['select_prix_liit'] = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list(filter(lambda x: x['livre']['prix_litteraire'] != {}, dico_rl_dataviz.values())) for y in x['livre']['prix_litteraire'].values() ], columns = ['Auteur','Livre','maison_edition','prix'])
	st.session_state['select_prix_liit'] = pd.concat([st.session_state['select_prix_liit'], pd.json_normalize(st.session_state['select_prix_liit'].pop("prix"))], axis=1)


### A. Sidebar

with st.sidebar:
	st.success("Select an add method.")
	st.title('RENTRÉE LITTÉRAIRE & PRIX LITTÉRAIRES')
	st.header('2023')

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
	
	st.divider()
	st.divider()

	#st.subheader("liste RL")
	#st.dataframe(df_rl_dataviz)
	#st.write(dico_rl_dataviz[2]['livre'])
	
	#st.button("Rerun")

with cont_metric :
	col_metric, col_graph_saiso, col_graph_genre = st.columns([2,4,4])
	with col_metric : 
		st.markdown("#### Recap")
		#Metric nb Ouvrages
		liste_ean = set([l['ean'] for l in df_list_livre_rl['livre']])
		st.metric(label="Livres", value=len(liste_ean))

		#Metric nb Editeurs
		liste_editeur = set([l['maison_edition'] for l in df_list_livre_rl['livre']])
		st.metric(label="Editeurs", value = len(liste_editeur))

		#Metric Premier Roman
		list_livre_rl_prem_roman = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['premier_roman'] == 'PREMIER ROMAN',
											 dico_rl_dataviz.values()))
		st.metric(label="Premiers romans", value = len(list_livre_rl_prem_roman))
	
	with col_graph_saiso :
	# Filtre => unique les livres RL et mois de sortie
		dico_saiso_sorties_mensuelles = []
		liste_mois = ['June', 'July', 'August', 'September', 'October', 'November', 'December', 'January']
		for mois in liste_mois :
			list_livre_rl_mois = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['mois de parution'] == mois,
											 dico_rl_dataviz.values()))
			
			dico_saiso_sorties_mensuelles.append([mois, len(list_livre_rl_mois)])
	
		df_saiso_sorties_mensuelles = pd.DataFrame.from_dict(dico_saiso_sorties_mensuelles).rename(columns={0:'Mois', 1:'Nb ouvrages'})
		df_saiso_sorties_mensuelles['nb_mois'] = [str(i)+'_'+m for i, m in enumerate(df_saiso_sorties_mensuelles['Mois'])]
		#st.dataframe(df_saiso_sorties_mensuelles)
		st.markdown("#### Nombre d\'ouvrages sortis par mois")
		st.bar_chart(df_saiso_sorties_mensuelles, x='nb_mois', y="Nb ouvrages")
		
	with col_graph_genre :
		st.markdown("#### Nombre d\'ouvrages par genre")
		dico_genre = []
		liste_genre = ['M', 'F', 'MIXTE', 'NB', 'NC']
		for genre in liste_genre :
			list_livre_rl_genre = list(filter(lambda x: x['livre']['RL'] != '' and x['genre'] == genre,
											 dico_rl_dataviz.values()))
			dico_genre.append([genre, len(list_livre_rl_genre)])
	
		df_genre = pd.DataFrame.from_dict(dico_genre).rename(columns={0:'genre', 1:'Nb ouvrages'})
		#st.write(df_genre)
		
		## Create subplots: use 'domain' type for Pie subplot
		fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
		fig.add_trace(go.Pie(labels=df_genre['genre'], values=df_genre['Nb ouvrages'], name="Casting",
							 title='Nb de roman par genre', hole=.3))
		st.plotly_chart(fig,theme=None,use_container_width=True)

##### Pays d'origine des auteurs
with cont_geo:
	col_map, col_geo_chart = st.columns([4,2])
	
	liste_pays = set(df_list_livre_rl['pays'])
	dico_pays = []
	for pays in liste_pays :
		list_livre_rl_pays = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['ean'] != '' and x['pays'] == pays, dico_rl_dataviz.values()))
		dico_pays.append([pays, len(list_livre_rl_pays)])

	df_pays = pd.DataFrame.from_dict(dico_pays).rename(columns={0:'Pays', 1:'Nb ouvrages'})
	#st.write(df_pays)
	
	df_rl_dataviz_geo = df_list_livre_rl[['pays','latitude','longitude','continent']].groupby(['pays','latitude','longitude','continent']).count().reset_index()
	
	continent_color = {'EUROPE' : '#00b6cb',
	'NORTH AMERICA': '#124559',
	'ASIA' : '#5e35b1',
	'AFRICA' : '#7cb342',
	'SOUTH AMERICA' : '#598392',
	'CENTRAL AMERICA' : '#aec3b0',
	'OCEANIA' : '#ff7043',
	'CARIBBEAN' : '#f2bedb'}
	
	df_rl_dataviz_geo.insert(4, 'continent_color', df_rl_dataviz_geo.continent.apply(lambda c :continent_color[c]))
	with col_map :
		st.markdown("#### Répartition géographique des auteurs")
		st.map(df_rl_dataviz_geo,
		    latitude='latitude',
		    longitude='longitude',
			size=150,
			color='continent_color')

	with col_geo_chart :
		st.markdown("#### Pays d'origine des auteurs")
		#st.dataframe(df_rl_dataviz_geo.sort_values('EAN', ascending = False))
		fig=px.bar(df_pays.sort_values('Nb ouvrages', ascending = False).head(10), x='Nb ouvrages',y='Pays', orientation='h')
		st.write(fig)	

with st.sidebar:
	liste_prix_litt = set([pl['nom_prix'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values()])
	select_prix_litt = st.selectbox('Selection prix', liste_prix_litt)
	
	liste_prix_litt_detail = set([pl['nom_prix_detail'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values() 
								 if pl['nom_prix'] == select_prix_litt])
	select_prix_litt_detail = st.selectbox('Selection prix detail', liste_prix_litt_detail, None)

st.divider()

#### Analyse prix Littéraire
with cont_prix_litt :
	#Pour afficher la liste des ouvrages avec au moins une sélection à un prix littéraire
	def select_pl(pl):
		if pl == None : 
			select_prix_liit = st.session_state['select_prix_liit'][['Auteur','Livre','maison_edition','nom_prix', 'nom_prix_detail','premiere_selection','deuxieme_selection','troisieme_selection','lauréat']].sort_values(['nom_prix','nom_prix_detail']).reset_index(drop = True)
		else :
			select_prix_liit = st.session_state['select_prix_liit'].loc[st.session_state['select_prix_liit']['nom_prix_detail'] == pl]
			#select_prix_liit = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list_livre_prix_litt for y in x['livre']['prix_litteraire'].values() if y['nom_prix_detail'] == pl], columns = ['Auteur','Livre','maison_edition','prix'])
			#select_prix_liit = pd.concat([select_prix_liit , pd.json_normalize(select_prix_liit.pop("prix"))], axis=1)
			
		return select_prix_liit#[['Auteur','Livre','maison_edition','prix']]
	
	#Fonction pour mettre en lumière le titre qui est lauréat pour un prix
	def cooling_highlight(val):
		color = '#6dd3ce' if val == 'OUI' else ''
		return f'background-color: {color}'

	#Affichage de la liste des lauréats 
	st.markdown('### Liste des lauréats aux Prix littéraire : Rentrée Littéraire 2023')

	df_laureat = st.session_state['select_prix_liit'].loc[st.session_state['select_prix_liit']['lauréat'] == 'OUI'].sort_values('nom_prix').reset_index(drop = True)
	
	#pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list_livre_prix_litt for y in x['livre']['prix_litteraire'].values() if y['lauréat'] == 'OUI'] , columns = ['Auteur','Livre','maison_edition','prix'])
	#df_laureat = pd.concat([df_laureat , pd.json_normalize(df_laureat.pop("prix"))], axis=1)
	
	st.dataframe(df_laureat[['Auteur','Livre','maison_edition','nom_prix','nom_prix_detail']])

	#Affichage des livres sélectionnées par Prix Littéraire suivant sélection dans sidebar. Tout est affiché si pas de sélection.
	st.markdown('### Liste sélectionné•es par Prix littéraire : Rentrée Littéraire 2023')
	select_prix_liit = select_pl(select_prix_litt_detail)
	select_prix_liit = select_prix_liit[['lauréat','Auteur','Livre','maison_edition','nom_prix','nom_prix_detail',
									   'premiere_selection','deuxieme_selection','troisieme_selection']].sort_values('nom_prix').reset_index(drop = True)
	
	select_prix_liit_style = select_prix_liit.style.applymap(cooling_highlight, subset=['lauréat'])
	
	st.dataframe(select_prix_liit_style)

	start_color, end_color = st.select_slider(
	    'Select a range of color wavelength',
	    options=['Première sélection', 'Deuxième sélection', 'Troisième sélection'],
	    value=('Première sélection', 'Troisième sélection'))
	st.write('You selected wavelengths between', start_color, 'and', end_color)
	
	if start_color == 'Première sélection' and end_color == 'Troisième sélection' :
		st.dataframe(select_prix_liit.loc[select_prix_liit.troisieme_selection == 'OUI'])
	elif start_color == 'Première sélection' and end_color == 'Deuxième sélection' :
		st.dataframe(select_prix_liit.loc[select_prix_liit.deuxieme_selection == 'OUI'])
	else : 
		st.dataframe(select_prix_liit.loc[select_prix_liit.premiere_selection == 'OUI'])






