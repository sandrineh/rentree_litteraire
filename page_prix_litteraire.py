# imageColor.py = https://www.youtube.com/watch?v=6iE95W9cNcI&ab_channel=JCharisTech
# 1.Importation des librairies nécessaires pour le script
#Core Pkgs - Web application
import streamlit as st
from streamlit_option_menu import option_menu

#Other Pkgs
from PIL import Image
import os
import random 

#Datavisualisation
import altair as alt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

#from collections import Counter
#from sklearn.cluster import KMeans
#import cv2

import time
import re

import json
from pandas.io.json import json_normalize

#from geopy.geocoders import Nominatim

#Export fichier
import pickle

if 'df' not in st.session_state:
	st.session_state['df'] = ''
if 'dico' not in st.session_state:
	st.session_state['dico'] = ''
if 'liste_ean' not in st.session_state:
	st.session_state['liste_ean'] = ''
if 'select_editeur' not in st.session_state:
	st.session_state['select_editeur'] = ''
if 'liste_ouvrage' not in st.session_state:
	st.session_state['liste_ouvrage'] = ''

class InfoPrixLitt():
	def intro_form():
	        # --------------- PRESENTATION DE LA PARTIE FORMULAIRE
	        st.header("INFOS FORMULAIRE")
	        st.write(""" En s'inspirant de l'étude Cinégalités du Collectif 50/50(1), l'objectif ici est d'étendre son périmètre (remonter dans le temps, plateformes indépendantes, séries) 
	            et automatiser la collecte de données pour les films d'initiative française(2).""")
	
	        st.markdown(f'<p style="font-size:10px;">(1) Rapport Cinégalité (<a style="font-size:10px;" href="https://collectif5050.com/wordpress/wp-content/uploads/2022/05/Cinegalite-s-Rapport.pdf">Télecharger le rapport complet</a>) <br> (2) film d\'initiative française (FIF): "Un Film d’Initiative Française est un film agréé par le CNC dont le financement est majoritairement ou intégralement français. Ces Films d’Initiative Française peuvent être coproduits avec des coproducteurs étrangers mais, dans ce cas, la part étrangère sera minoritaire" (Source : (<a style="font-size:10px;" href="https://www.afar-fiction.com/IMG/pdf/L_economie_des_films_francais.pdf">Afar Fiction</a>)</p>', unsafe_allow_html=True)
	        
	        with st.expander("Principe"):
	            st.write(""" Ce formulaire est la version numérique de la grille de visionnage 
	            de l'étude Cinégalité. L'objectif est ici de recueillir les données relatives aux personnages locuteurs récurrents. 
	            On entend par là les personnages "apparaissant au moins dans deux séquences dans lesquelles ils s’expriment".
	            Les données sont de trois ordres : \n
	-les caractéristiques sociodémographiques des personnages, \n
	-leur place dans la narration,\n
	-certains éléments relatifs à leurs actions ou à leur trajectoire dans le récit".""")
	
	        st.write("""Méthodologie :\n
	1) Sélectionnez le film (FIF) de votre choix. S'il n'est pas dans la liste, renseignez le champs vide.\n
	2) Renseignez les champs du formulaire. Vous pouvez vous aider du menu à gauche pour accédez à un thème du questionnaire.
	            >>A noter : l'idéal est de remplir tous les champs.\n
	3) une fois que vous avez terminé,cliquer sur "Submit". Deux options s'offrent alors à vous :\n
	    1) poursuivre et renseigner un nouveau film \n
	    2) terminer en cliquant sur "End" """)


	def get_data(df,dico):
		st.session_state['df'] = df
		st.session_state['dico'] = dico

	#1. Récupération des data
	df_list_livre_rl = st.session_state['df']
	#dico_rl_dataviz = st.session_state['dico']
	#### Analyse prix Littéraire
	with st.container(border = True) : #prixlitt:#cont_prix_litt :
		with st.sidebar:
			liste_prix_litt = set([pl['nom_prix'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values()])
			select_prix_litt = st.selectbox('Selection prix', liste_prix_litt)
			
			liste_prix_litt_detail = set([pl['nom_prix_detail'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values() 
										  if pl['nom_prix'] == select_prix_litt])
			st.write(liste_prix_litt_detail)
			#select_prix_litt_detail = st.selectbox('Selection prix detail', liste_prix_litt_detail, None)


		
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
