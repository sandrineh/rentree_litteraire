
# 1.Importation des librairies nécessaires pour le script
from urllib.request import Request, urlopen
#from bs4 import BeautifulSoup
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
import sys

import time

#Datavisualisation
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

import streamlit as st
from streamlit_option_menu import option_menu

## Import the required library
#from geopy.geocoders import Nominatim

import altair as alt

import pickle

import base64

# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(page_title="Rentree Litteraire", page_icon="books", layout="wide")

#st.write("RL_2023 GO")

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

# Pour création dataframe caractéristiques ouvrages
if 'caract_livre' not in st.session_state:
	st.session_state['caract_livre'] = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'], x['livre']['RL'], x['livre']['caracteristiques']] for x in list(filter(lambda x: x['livre']['caracteristiques'] != {}, dico_rl_dataviz.values()))], columns = ['Auteur','Livre','maison_edition','RL','caracteristiques'])
	st.session_state['caract_livre'] = pd.concat([st.session_state['caract_livre'], pd.json_normalize(st.session_state['caract_livre'].pop("caracteristiques"))], axis=1)
	#Je conserve uniquement les livres de la rentree litteraire
	st.session_state['caract_livre'] = st.session_state['caract_livre'].loc[st.session_state['caract_livre']['RL'] =='RL']

# Pour creéation dataframe prix littéraire
if 'df_prix_liit' not in st.session_state:
	st.session_state['df_prix_liit'] = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],x['livre']['autres_infos'],y] for x in list(filter(lambda x: x['livre']['prix_litteraire'] != {}, dico_rl_dataviz.values())) for y in x['livre']['prix_litteraire'].values() ], columns = ['Auteur','Livre','maison_edition','couv','prix'])
	#pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list(filter(lambda x: x['livre']['prix_litteraire'] != {}, dico_rl_dataviz.values())) for y in x['livre']['prix_litteraire'].values() ], columns = ['Auteur','Livre','maison_edition','prix'])
	st.session_state['df_prix_liit'] = pd.concat([st.session_state['df_prix_liit'], pd.json_normalize(st.session_state['df_prix_liit'].pop("prix"))], axis=1)
	st.session_state['df_prix_liit'] = pd.concat([st.session_state['df_prix_liit'], pd.json_normalize(st.session_state['df_prix_liit'].pop("couv"))], axis=1)

# Données Romans français
if 'roman_francais' not in st.session_state:
	st.session_state['roman_francais'] = ''

# Données Romans français
if 'roman_etranger' not in st.session_state:
	st.session_state['roman_etranger'] = ''

# Données Essais
if 'essais' not in st.session_state:
	st.session_state['essais'] = ''

if 'couv_livre' not in st.session_state:
	st.session_state['couv_livre'] = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'], x['livre']['RL'], x['livre']['autres_infos']] for x in list(filter(lambda x: x['livre']['autres_infos'] != {}, dico_rl_dataviz.values()))], columns = ['Auteur','Livre','maison_edition','RL','autres_infos'])
	st.session_state['couv_livre'] = pd.concat([st.session_state['couv_livre'], pd.json_normalize(st.session_state['couv_livre'].pop("autres_infos"))], axis=1)

	
### A. Sidebar
#x['livre']['autres_infos']] for x in list(filter(lambda x: x['livre']['autres_infos'] != {}, dico_rl_dataviz.values()))
#with st.sidebar:
	#st.success("Select an add method.")
	#st.title('RENTRÉE LITTÉRAIRE & PRIX LITTÉRAIRES')
	#st.header('2023')


##### AJOUT DANS SIDEBAR

# 6. Création du sidebar de l'app
class sidebar():
    def __init__(self):
        self.selected = ''

    def display_sidebar() : 
        with st.sidebar:
            # 6.1 --------------- HEADER du sidebar avec le nom du projet et le logo
            def header(projet,sous_projet):
                st.markdown(f'<div><h1 style="background-color:#E3879E;color:#000;height:150px;justify-content:center;align-items:center;margin-bottom:20px;text-align:center;border-radius:6px;font-size:30px;">{projet}</br><p style="font-size:20px;padding-top:10px; color:#363535">{sous_projet}</p></div>',unsafe_allow_html=True)
				#(palette : 80A1C1 air superiority blue - 6F2DBD Grape - 3B413C Black olive - FFA400 Orange (web) - E3879E Rose pompadour)
            header("RENTRÉE LITTÉRAIRE & PRIX LITTÉRAIRES","2023")

            # 6.2 Ajout de 2 menus déroulants qui permettent d'avoir des infos sur le projet et l'application
            # --------------- Add two expanders to provide additional information about this e-tutorial and the app
            with st.expander("Le projet"):
                url="https://dataforgood.fr/projects/bechdelai"
                st.image('https://dataforgoodfr.github.io/img/logo-dfg-new2.png', width=50) #use_column_width=True, https://dataforgoodfr.github.io/img/logo-dfg-new2.png, https://dataforgood.fr/img/logo-dfg-new2.png
                st.write("""Mesure et automatisation du test de Bechdel, de la (sous)représentation féminine 
                    et des inégalités de représentation dans le cinéma et l'audiovisuel """)
                st.markdown(f'<a href={url} style="text-decoration:none;color:#000">En savoir plus</a>', unsafe_allow_html=True)

            with st.expander("L'application"):
                 st.write("""This interactive eCourse App was built by Sharone Li using Streamlit and Streamlit_book. 
                    Streamlit_book is a Streamlit companion library that was written in Python and created by Sebastian Flores Benner. 
                     \n  \nThe Streamlit_book library was released on 01/20/2022. 
                     If you want to learn more about Streamlit_book, please read Sebastian's post here:
                     https://blog.streamlit.io/how-to-create-interactive-books-with-streamlit-and-streamlit-book-in-5-steps/""")    
            # 6.3 Création du menu de sélection des "chapitres" de l'application - infos films, formulaire, Age gap
			# la liste des icones sont là : https://icons.getbootstrap.com/
			
            selected = option_menu(None, 
                ["Rentrée Littéraire", "Prix Littéraire"], 
                icons=['book', 'award'], 
                menu_icon="cast", 
                default_index=0, 
                orientation="vertical",
                styles={
                    "container": {"padding": "0!important", "background-color": "#grey"},
                    "icon": {"color": "#FFA400", "font-size": "20px"}, 
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#3B413C"},
                    "nav-link-selected": {"background-color": "#3B413C"},})
            
            return (selected)


### B. Container 
cont_metric = st.container(border = True) #st.container(border = True)
cont_tab = st.container()
cont_geo = st.container()
cont_prix_litt = st.container()

#je transforme le dictionnaire en dataframe
df_rl_dataviz_pl = pd.DataFrame.from_dict(dico_rl_dataviz, orient='index')
st.session_state['df_rl_dataviz_pl']  = df_rl_dataviz_pl

#l'idée est de filtrer sur les ouvrages identifié comme ouvrage de la rentrée littéraire
# Filtre => unique les livres RL
list_livre_rl = list(filter(lambda x: x['livre']['RL'] != '', dico_rl_dataviz.values()))
df_list_livre_rl = pd.DataFrame(list_livre_rl)

# A. afficher le menu en sidebar                        
selected = sidebar.display_sidebar()


if selected == "Rentrée Littéraire":
	from page_rentree_litteraire import *
	#je recupère les données sous forme de dataframe et de dictionnaire pour les mettre dans des "session_state"
	InfoRentreeLitt.get_data(df_list_livre_rl,dico_rl_dataviz)

	with cont_metric :
		#j'affiche les metriques macro relatives à la rentrée littéraire 2023
		InfoRentreeLitt.do_metric_macro()
		#J'affiche le graphique de saisonnalité des parutions
		InfoRentreeLitt.do_saiso_sortie(dico_rl_dataviz)
	# J'affiche le menu pour la annalyses spécifiques : générale, zone géographiques, par genre, pour les premiers romans
	selected_info = InfoRentreeLitt.menu_horizontal()

	# B. afficher le menu d'analyse de film 
	if selected_info == "Informations":
		with st.container(border = True): 
			InfoRentreeLitt.do_info_rl()
		with st.container(border = True):
			InfoRentreeLitt.do_info_editeur()
		with st.container(border = True):
			InfoRentreeLitt.do_info_ouvrage()
			
	elif selected_info == "Géographie":
	    InfoRentreeLittGeo.do_info_geo()
		
	else :
	    st.empty()

# C. Prix litt
if selected == "Prix Littéraire":
	st.header('Prix Littéraires 2023')
	
	from page_prix_litteraire import *
	# C.1. afficher la sidebar 
	analysePrixLitt.sidebar_choix_prix()

	# C.2. afficher le menu horizontal 
	with st.container(border = True):
		selected_prix = analysePrixLitt.menu_horizontal()

	# C.3. afficher le contenu suivant le choix du menu horizontal
	if selected_prix == "Lauréats 2023":
		with st.container(border = True):
			analysePrixLitt.info_laureat()
			
	elif selected_prix == "Prix Littéraire":
		with st.container(border = True):
			analysePrixLitt.info_choix_prix()
		#with st.container(border = True):
			#analysePrixLitt.info_choix_prix.info_course()
		
	else :
	    st.empty()
		
	
	

#with cont_metric :
#	rl_title, rl_espce_vide, rl_metric = st.columns([2,1,5])
#	with rl_title : 
#		st.markdown("# Rentrée Littéraire\
#						   &\
#					   Prix Littéraire 2023")
#
#	with rl_metric : 
#		col_nb_livre, col_nb_editeur, col_nb_prem_roman = st.columns([2,2,2])
#		with col_nb_livre : 
#			#Metric nb Ouvrages
#			liste_ean = set([l['ean'] for l in df_list_livre_rl['livre']])
#			st.metric(label="Livres", value=len(liste_ean))
#		with col_nb_editeur :
#			#Metric nb Editeurs
#			liste_editeur = set([l['maison_edition'] for l in df_list_livre_rl['livre']])
#			st.metric(label="Editeurs", value = len(liste_editeur))
#		with col_nb_prem_roman : 
#			#Metric Premier Roman
#			list_livre_rl_prem_roman = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['premier_roman'] == 'PREMIER ROMAN',
#												 dico_rl_dataviz.values()))
#			st.metric(label="Premiers romans", value = len(list_livre_rl_prem_roman))
#
#		st.divider()
#
#		## Graph Nb parution par mois
#		# Filtre => unique les livres RL et mois de sortie
#		dico_saiso_sorties_mensuelles = []
#		liste_mois = ['June', 'July', 'August', 'September', 'October', 'November', 'December', 'January']
#		for mois in liste_mois :
#			list_livre_rl_mois = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['mois de parution'] == mois,
#											 dico_rl_dataviz.values()))
#			
#			dico_saiso_sorties_mensuelles.append([mois, len(list_livre_rl_mois)])
#	
#		df_saiso_sorties_mensuelles = pd.DataFrame.from_dict(dico_saiso_sorties_mensuelles).rename(columns={0:'Mois', 1:'Nb ouvrages'})
#		df_saiso_sorties_mensuelles['nb_mois'] = [str(i)+'_'+m for i, m in enumerate(df_saiso_sorties_mensuelles['Mois'])]
#		#st.dataframe(df_saiso_sorties_mensuelles)
#		st.markdown("#### Nombre de parutions par mois")
#		st.bar_chart(df_saiso_sorties_mensuelles, x='nb_mois', y="Nb ouvrages")

#with cont_tab :
		
	#rent_litt, prem_roman, genre_tab, prixlitt = st.tabs(["Rentrée Littéraire", "Premier Roman", "Geographie", "Prix Littéraire"])	
#	with rent_litt:
#		col_graph_rl, col_text_rl = st.columns(2, gap='small')
#
#		with col_graph_rl : 
#			dico_rent_litt = []
#			liste_type_rent_litt = ['Romans français', 'Romans étrangers', 'Essais']
#			for type in liste_type_rent_litt :
#				liste_type_rent_litt_temp = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['type'] == type,
#												 dico_rl_dataviz.values()))
#				dico_rent_litt.append([type, len(liste_type_rent_litt_temp)])
#		
#			df_type_rent_litt = pd.DataFrame.from_dict(dico_rent_litt).rename(columns={0:'Type', 1:'Nb ouvrages'})
#			
#			st.session_state['roman_francais'] = df_type_rent_litt[df_type_rent_litt['Type']=='Romans français']['Nb ouvrages'].values[0]
#			st.session_state['roman_etranger'] = df_type_rent_litt[df_type_rent_litt['Type']=='Romans étrangers']['Nb ouvrages'].values[0]
#			st.session_state['essais'] = df_type_rent_litt[df_type_rent_litt['Type']=='Essais']['Nb ouvrages'].values[0]
#
#			st.write(f"Parmi les ouvrages parus, **:blue[{int(round(st.session_state['roman_francais']/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger']/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais']/len(liste_ean)*100,0))}%]** des essais.")
#			
#			# Création du barchart horizontal
#			with st.container():
#				fig_type=px.bar(df_type_rent_litt.sort_values('Nb ouvrages', ascending = True), x='Nb ouvrages',y='Type', orientation='h',
#							   text_auto=True)
#				fig_type.update_traces(textfont_size=16, textangle=0, textposition="inside", 
#									   cliponaxis=False, insidetextfont_color='black')
#				fig_type.update_xaxes(showgrid=False,tickfont=dict(size=14), showticklabels=False)
#				fig_type.update_yaxes(showgrid=False,tickfont=dict(size=14))
#				fig_type.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title=None, yaxis_title=None)
#		
#				st.plotly_chart(fig_type, use_container_width=True)
#				
#
#		with col_text_rl:
#			df_caract_livre = st.session_state['caract_livre']
#			df_caract_livre['nombre_pages'] = df_caract_livre['nombre_pages'].str.replace('\D', '',regex=True)
#			df_caract_livre['prix_indicatif'] = df_caract_livre['prix_indicatif'].str.replace(' €','').str.replace(',','.')
#			
#			#st.dataframe(df_caract_livre)
#			
#			#nettoyer les valeurs pour conserver uniquement les nombres. Par exemple je retire pages à "138 pages"
#					#pour garder 138 que je passerais ensuite en int.
#			### ATTENTION, j'ai 9 livres avec 0 pages ou NONE
#			nb_pages_total = sum(filter(None, [s for s in df_caract_livre['nombre_pages'].str.replace('\D', '',
#											   regex=True).fillna(0).astype('int64')]))
#			nb_livre_nb_pages_total = len(list(filter(None, [s for s in df_caract_livre['nombre_pages'].str.replace('\D', '',
#											   regex=True).fillna(0).astype('int64')])))
#			nb_pages_moyen = int(nb_pages_total/nb_livre_nb_pages_total)
#			
#			nb_pages_min = min(filter(None, [s for s in df_caract_livre['nombre_pages'].str.replace('\D', '',
#											   regex=True).fillna(0).astype('int64')]))
#			nb_pages_max = max(filter(None, [s for s in df_caract_livre['nombre_pages'].str.replace('\D', '',
#											   regex=True).fillna(0).astype('int64')]))
#			
#			# même travail avec les prix
#			prix_total = round(sum(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])),2)
#			nb_livre_prix_total = len(list(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])))
#			prix_moyen = round(prix_total/nb_livre_prix_total,2)
#			
#			prix_min = round(min(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])),2)
#			#prix_moyen = round(mean(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])),2)
#			prix_max = round(max(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])),2)
#			#st.write(prix_total)
#		    
#			st.markdown(f"Acheter l'ensemble des livres de la Rentrée Littéraire vous coûtera **:blue[{prix_total}€]**. Avec un nombre total de **:blue[{nb_pages_total}]** pages, c'est **:blue[{nb_pages_total/30}]*** heures de lecture qui vous attend, soit un équivalent de **:blue[{int(nb_pages_total/30/24)}]** jours.")
#
#
#			colaa, colab, colvideab, colac, colvideac, colad = st.columns([1,1,0.3,3,0.3,2])
#			with colaa:
#				st.markdown(f':blanc[ .]')
#				st.markdown("### :moneybag:")#st.image('./docs/icons8-euro-money-50.png', width=30) 
#			with colab:
#				st.write('Min.')
#				st.markdown(prix_min)
#			with colvideab:
#				st.markdown(':arrow_left:')
#			with colac:
#				st.markdown('<div style="text-align: center;">Prix Moyen</div>', unsafe_allow_html=True)
#				st.markdown(f'<div style="text-align: center;">{prix_moyen}</div>', unsafe_allow_html=True) 
#			with colvideac:
#				st.markdown(':arrow_right:')
#			with colad:
#				st.write('Max.')
#				st.markdown(prix_max)
#
#			colba, colbb, colvidebb, colbc, colvidebc, colbd = st.columns([1,1,0.3,3,0.3,2])
#			with colba:
#				st.markdown(f':blanc[ .]')
#				st.image('./docs/icons8-terms-and-conditions-50.png', width=30)
#			with colbb:
#				st.write('Min.')
#				st.markdown(nb_pages_min)
#			with colvidebb:
#				st.markdown(':arrow_left:')
#			with colbc:
#				st.markdown('<div style="text-align: center;">Nb moyen de pages</div>', unsafe_allow_html=True)
#				st.markdown(f'<div style="text-align: center;">{int(nb_pages_total/nb_livre_nb_pages_total)}</div>', unsafe_allow_html=True) 
#			with colvidebc:
#				st.markdown(':arrow_right:')
#			with colbd:
#				st.write('Max.')
#				st.markdown(nb_pages_max)
#
#			note_page = "*On se base ici sur l'idée qu'un lecteur « normal » lit environs 250 à 300 mots par minute - ce qui représente 1 page toutes les deux minutes, soit environ 30 pages par heure."
#			st.markdown(f'<div style="font-size: 12px;">{note_page}</div>', unsafe_allow_html=True)
#
#	
#		st.divider()
		
		#col_map_2, col_graph_saiso, col_graph_genre = st.columns(3)
	
#		with st.container() :
#			# Filtre => uniquement les livres de la Rentree Litteraire
#			
#			col_map, col_geo_chart = st.columns(2)
#			with col_map :
#					
#				df_rl_dataviz_geo = df_list_livre_rl[['pays','latitude','longitude','continent','nom_complet']].groupby(['pays',
#													  'latitude','longitude','continent']).count().reset_index()
#				df_rl_dataviz_geo['nom_complet'] = df_rl_dataviz_geo['nom_complet'].astype('int64')
#				continent_color = {'EUROPE' : '#00b6cb',
#				'NORTH AMERICA': '#124559',
#				'ASIA' : '#5e35b1',
#				'AFRICA' : '#7cb342',
#				'SOUTH AMERICA' : '#598392',
#				'CENTRAL AMERICA' : '#aec3b0',
#				'OCEANIA' : '#ff7043',
#				'CARIBBEAN' : '#f2bedb'}
#		
#				df_rl_dataviz_geo.insert(4, 'continent_color', df_rl_dataviz_geo.continent.apply(lambda c :continent_color[c]))
#				#st.dataframe(df_rl_dataviz_geo)
#	
#				nb_livre_vf = len(list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['ean'] != '' and x['livre']['traduit_de'] == 'VF', dico_rl_dataviz.values())))
#				nb_livre_hors_vf = len(list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['ean'] != '' and x['livre']['traduit_de'] != 'VF', dico_rl_dataviz.values())))
#			
#				st.markdown(f"**Répartition Géographique des auteurs (cliquer pour filtrer)**")
#				st.markdown(f"Pour rappel : **:blue[{nb_livre_vf}]** sont de langue française, **:blue[{nb_livre_hors_vf}]** sont des traductions.")
#				
#				st.map(df_rl_dataviz_geo,
#				    latitude='latitude',
#				    longitude='longitude',
#					size= 'nom_complet',
#					color='continent_color')
#		
#			
#			with col_geo_chart :
#				st.markdown(f"**Top 10 des pays d'origine des auteurs**")
#				liste_pays = set(df_list_livre_rl['pays'])
#				dico_pays = []
#				for pays in liste_pays :
#					list_livre_rl_pays = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['ean'] != '' and x['pays'] == pays, dico_rl_dataviz.values()))
#					dico_pays.append([pays, len(list_livre_rl_pays)])
#		
#				df_pays = pd.DataFrame.from_dict(dico_pays).rename(columns={0:'Pays', 1:'Nb ouvrages'})
#				#st.write(df_pays)
#			
#				fig_top_origine_auteur = px.bar(df_pays.sort_values('Nb ouvrages', ascending = True).tail(10), x='Nb ouvrages',
#												y='Pays', orientation='h')
#				st.plotly_chart(fig_top_origine_auteur, use_container_width=True)
#		st.divider()
	
		

	
###### Pays d'origine des auteurs
#	with genre_tab:
#
#		#with col_graph_genre :
#		st.markdown("#### Nombre d\'ouvrages par genre")
#		dico_genre = []
#		liste_genre = ['M', 'F', 'MIXTE', 'NB', 'NC']
#		for genre in liste_genre :
#			list_livre_rl_genre = list(filter(lambda x: x['livre']['RL'] != '' and x['genre'] == genre,
#											 dico_rl_dataviz.values()))
#			dico_genre.append([genre, len(list_livre_rl_genre)])
#	
#		df_genre = pd.DataFrame.from_dict(dico_genre).rename(columns={0:'genre', 1:'Nb ouvrages'})
#		#st.write(df_genre)
#		
#		## Create subplots: use 'domain' type for Pie subplot
#		fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
#		fig.add_trace(go.Pie(labels=df_genre['genre'], values=df_genre['Nb ouvrages'], name="Casting",
#							 title='Nb de roman par genre', hole=.3))
#		st.plotly_chart(fig,theme=None,use_container_width=True)
#
#	
#	#### Analyse prix Littéraire
#	with prixlitt:#cont_prix_litt :
#		with st.sidebar:
#			liste_prix_litt = set([pl['nom_prix'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values()])
#			select_prix_litt = st.selectbox('Selection prix', liste_prix_litt)
#			
#			liste_prix_litt_detail = set([pl['nom_prix_detail'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values() 
#										 if pl['nom_prix'] == select_prix_litt])
#			select_prix_litt_detail = st.selectbox('Selection prix detail', liste_prix_litt_detail, None)
#
#
#		
#		#Pour afficher la liste des ouvrages avec au moins une sélection à un prix littéraire
#		def select_pl(pl):
#			if pl == None : 
#				select_prix_liit = st.session_state['select_prix_liit'][['Auteur','Livre','maison_edition','nom_prix', 'nom_prix_detail','premiere_selection','deuxieme_selection','troisieme_selection','lauréat']].sort_values(['nom_prix','nom_prix_detail']).reset_index(drop = True)
#			else :
#				select_prix_liit = st.session_state['select_prix_liit'].loc[st.session_state['select_prix_liit']['nom_prix_detail'] == pl]
#				#select_prix_liit = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list_livre_prix_litt for y in x['livre']['prix_litteraire'].values() if y['nom_prix_detail'] == pl], columns = ['Auteur','Livre','maison_edition','prix'])
#				#select_prix_liit = pd.concat([select_prix_liit , pd.json_normalize(select_prix_liit.pop("prix"))], axis=1)
#				
#			return select_prix_liit#[['Auteur','Livre','maison_edition','prix']]
#		
#		#Fonction pour mettre en lumière le titre qui est lauréat pour un prix
#		def cooling_highlight(val):
#			color = '#6dd3ce' if val == 'OUI' else ''
#			return f'background-color: {color}'
#	
#		#Affichage de la liste des lauréats 
#		st.markdown('### Liste des lauréats aux Prix littéraire : Rentrée Littéraire 2023')
#	
#		df_laureat = st.session_state['select_prix_liit'].loc[st.session_state['select_prix_liit']['lauréat'] == 'OUI'].sort_values('nom_prix').reset_index(drop = True)
#		
#		#pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list_livre_prix_litt for y in x['livre']['prix_litteraire'].values() if y['lauréat'] == 'OUI'] , columns = ['Auteur','Livre','maison_edition','prix'])
#		#df_laureat = pd.concat([df_laureat , pd.json_normalize(df_laureat.pop("prix"))], axis=1)
#		
#		st.dataframe(df_laureat[['Auteur','Livre','maison_edition','nom_prix','nom_prix_detail']])
#	
#		#Affichage des livres sélectionnées par Prix Littéraire suivant sélection dans sidebar. Tout est affiché si pas de sélection.
#		st.markdown('### Liste sélectionné•es par Prix littéraire : Rentrée Littéraire 2023')
#		select_prix_liit = select_pl(select_prix_litt_detail)
#		select_prix_liit = select_prix_liit[['lauréat','Auteur','Livre','maison_edition','nom_prix','nom_prix_detail',
#										   'premiere_selection','deuxieme_selection','troisieme_selection']].sort_values('nom_prix').reset_index(drop = True)
#		
#		select_prix_liit_style = select_prix_liit.style.applymap(cooling_highlight, subset=['lauréat'])
#		
#		st.dataframe(select_prix_liit_style)
#	
#		start_color, end_color = st.select_slider(
#		    'Select a range of color wavelength',
#		    options=['Première sélection', 'Deuxième sélection', 'Troisième sélection'],
#		    value=('Première sélection', 'Troisième sélection'))
#		st.write('You selected wavelengths between', start_color, 'and', end_color)
#		
#		if start_color == 'Première sélection' and end_color == 'Troisième sélection' :
#			st.dataframe(select_prix_liit.loc[select_prix_liit.troisieme_selection == 'OUI'])
#		elif start_color == 'Première sélection' and end_color == 'Deuxième sélection' :
#			st.dataframe(select_prix_liit.loc[select_prix_liit.deuxieme_selection == 'OUI'])
#		else : 
#			st.dataframe(select_prix_liit.loc[select_prix_liit.premiere_selection == 'OUI'])
#
#with st.container():
#	from imageColor import *
#	
#	if __name__ == '__main__' :
#		main()
#	#st.image(image_file, use_column_width=True)

