
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

if 'caract_livre' not in st.session_state:
	st.session_state['caract_livre'] = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'], x['livre']['RL'], x['livre']['caracteristiques']] for x in list(filter(lambda x: x['livre']['caracteristiques'] != {}, dico_rl_dataviz.values()))], columns = ['Auteur','Livre','maison_edition','RL','caracteristiques'])
	st.session_state['caract_livre'] = pd.concat([st.session_state['caract_livre'], pd.json_normalize(st.session_state['caract_livre'].pop("caracteristiques"))], axis=1)
	#Je conserve uniquement les livres de la rentree litteraire
	st.session_state['caract_livre'] = st.session_state['caract_livre'].loc[st.session_state['caract_livre']['RL'] =='RL']


if 'couv_livre' not in st.session_state:
	st.session_state['couv_livre'] = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'], x['livre']['RL'], x['livre']['autres_infos']] for x in list(filter(lambda x: x['livre']['autres_infos'] != {}, dico_rl_dataviz.values()))], columns = ['Auteur','Livre','maison_edition','RL','autres_infos'])
	st.session_state['couv_livre'] = pd.concat([st.session_state['couv_livre'], pd.json_normalize(st.session_state['couv_livre'].pop("autres_infos"))], axis=1)
	

ah = pd.DataFrame([[x, x['livre']] for x in list(filter(lambda x: x['livre'] != {}, dico_rl_dataviz.values()))])
ah = pd.concat([ah, pd.json_normalize(ah.pop(0))], axis=1)
st.dataframe(ah)


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

		st.subheader("Dataframe of books features")
		df_caract_livre = st.session_state['caract_livre']
		df_caract_livre['nombre_pages'] = df_caract_livre['nombre_pages'].str.replace('\D', '',regex=True)
		df_caract_livre['prix_indicatif'] = df_caract_livre['prix_indicatif'].str.replace(' €','').str.replace(',','.')
		st.dataframe(df_caract_livre)
		
		st.write(len(df_caract_livre))

		st.subheader("Dataframe of books cover link")
		#Je conserve uniquement les livres de la rentree litteraire
		df_couv_livre = st.session_state['couv_livre'].loc[st.session_state['couv_livre']['RL'] =='RL']
		st.dataframe(df_couv_livre)
		
		st.write(len(df_couv_livre))


data_df = df_couv_livre.head(10)
data_df['couverture'] = data_df['couverture'].apply(lambda i : re.sub("\s+(\d\D)", "", i.split(',')[1])
													 if len(i.split(',')) > 1 else re.sub("\s+(\d\D)", "", i))

st.data_editor(
    data_df,
    column_config={
        "couverture": st.column_config.ImageColumn(
            "couverture", help="Streamlit app preview screenshots"
        )
    },
    hide_index=True,
)

# --------------- DEBUT CHOIX IMAGE + COMPUTER VISION
"""
	L'idée est ici de créer une vue de visuels de couvertures de livres alignés
	1. Dans un premier temps, dans un container, je mets la liste des urls des images dans une liste et le nom du livre dans une autre
	2. Je crée la possibilité de sélectionné le ou les livres que je veux afficher
	3. Si je retrouve le titre de la selection dans la liste totale alors j'affiche l'image correspondante
"""
	
container_cv = st.container()

with container_cv:
	st.write('pour affichage des couvertures de livres')
	
	container_choix_image = st.container()
	#all_images = st.checkbox("Select one or more images(s)")
	
	def load_images():
		titres_livres = []
		image_files = []
		for i,b in zip(data_df['couverture'],data_df['Livre']):
			if len(i.split(',')) > 1:
				i_replace = i.split(',')[1]
			else :
				i_replace = i
			image_link = re.sub("\s+(\d\D)", "", i_replace)
			image_files.append(image_link)

			part = image_link.replace('.webp','').split('/')
			if b not in titres_livres :
				titres_livres.append(b)
			
			#st.markdown(f"""![Foo]({image_link})""")
			#st.write(re.sub("\s+(\d\D)", "", i_replace))
			
		return image_files, titres_livres
		
	image_files, titres_livres = load_images()

	#st.write(image_files, titres_livres)
	
	#if all_images:
	#	view_titres_livres = container_choix_image.multiselect("Select one or more options:", image_files,image_files)
	#else:
	#	view_titres_livres =  container_choix_image.multiselect("Select one or more options:", image_files)
		
	view_titres_livres = st.multiselect("select image(s)", titres_livres, titres_livres)
	
	n = st.number_input("select images grid", 1,7,5)
	
	view_images = []
	# Si je retrouve le titre de la selection dans la liste totale alors j'affiche l'image correspondante
	for image_file, titre_livre in zip(image_files, titres_livres) :
		if titre_livre in view_titres_livres:
			view_images.append(image_file)
	
	groups = []
	for i in range(0, len(view_images), n):
		groups.append(view_images[i:i+n])
		
	for group in groups:
		cols = st.columns(n)
		for i, image_file in enumerate(group):
			cols[i].image(image_file, use_column_width=True)
# --------------- FIN CHOIX IMAGE + COMPUTER VISION