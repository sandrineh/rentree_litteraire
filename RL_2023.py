
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
if 'select_prix_liit' not in st.session_state:
	st.session_state['select_prix_liit'] = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list(filter(lambda x: x['livre']['prix_litteraire'] != {}, dico_rl_dataviz.values())) for y in x['livre']['prix_litteraire'].values() ], columns = ['Auteur','Livre','maison_edition','prix'])
	st.session_state['select_prix_liit'] = pd.concat([st.session_state['select_prix_liit'], pd.json_normalize(st.session_state['select_prix_liit'].pop("prix"))], axis=1)

# Données Romans français
if 'roman_francais' not in st.session_state:
	st.session_state['roman_francais'] = ''


# Données Romans français
if 'roman_etranger' not in st.session_state:
	st.session_state['roman_etranger'] = ''


# Données Essais
if 'essais' not in st.session_state:
	st.session_state['essais'] = ''


### A. Sidebar

with st.sidebar:
	st.success("Select an add method.")
	st.title('RENTRÉE LITTÉRAIRE & PRIX LITTÉRAIRES')
	st.header('2023')


### B. Container 
cont_metric = st.container() #st.container(border = True)
cont_tab = st.container()
cont_geo = st.container()
cont_prix_litt = st.container()

df_rl_dataviz = load_data("liste_rl_total_sans_doublon.pkl") #### Import pickel pour dataviz  
df_rl_dataviz = df_rl_dataviz.loc[df_rl_dataviz.RL == 'RL']

#je transforme le dictionnaire en dataframe
df_rl_dataviz_pl = pd.DataFrame.from_dict(dico_rl_dataviz, orient='index')

#l'idée est de filtrer sur les ouvrages identifié comme ouvrage de la rentrée littéraire
# Filtre => unique les livres RL
list_livre_rl = list(filter(lambda x: x['livre']['RL'] != '', dico_rl_dataviz.values()))
df_list_livre_rl = pd.DataFrame(list_livre_rl)


with cont_metric :
	rl_title, rl_espce_vide, rl_metric = st.columns([2,1,5])
	with rl_title : 
		st.markdown("# Rentrée Littéraire\
						   &\
					   Prix Littéraire 2023")

	with rl_metric : 
		col_nb_livre, col_nb_editeur, col_nb_prem_roman = st.columns([2,2,2])
		with col_nb_livre : 
			#Metric nb Ouvrages
			liste_ean = set([l['ean'] for l in df_list_livre_rl['livre']])
			st.metric(label="Livres", value=len(liste_ean))
		with col_nb_editeur :
			#Metric nb Editeurs
			liste_editeur = set([l['maison_edition'] for l in df_list_livre_rl['livre']])
			st.metric(label="Editeurs", value = len(liste_editeur))
		with col_nb_prem_roman : 
			#Metric Premier Roman
			list_livre_rl_prem_roman = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['premier_roman'] == 'PREMIER ROMAN',
												 dico_rl_dataviz.values()))
			st.metric(label="Premiers romans", value = len(list_livre_rl_prem_roman))

		st.divider()

		## Graph Nb parution par mois
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
		st.markdown("#### Nombre de parutions par mois")
		st.bar_chart(df_saiso_sorties_mensuelles, x='nb_mois', y="Nb ouvrages")

with cont_tab :
	rent_litt, prem_roman, genre_tab, prixlitt = st.tabs(["Rentrée Littéraire", "Premier Roman", "Geographie", "Prix Littéraire"])	
	with rent_litt:
		col_graph_rl, col_text_rl = st.columns(2, gap='small')

		with col_graph_rl : 
			dico_rent_litt = []
			liste_type_rent_litt = ['Romans français', 'Romans étrangers', 'Essais']
			for type in liste_type_rent_litt :
				liste_type_rent_litt_temp = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['type'] == type,
												 dico_rl_dataviz.values()))
				dico_rent_litt.append([type, len(liste_type_rent_litt_temp)])
		
			df_type_rent_litt = pd.DataFrame.from_dict(dico_rent_litt).rename(columns={0:'Type', 1:'Nb ouvrages'})
			
			st.session_state['roman_francais'] = df_type_rent_litt[df_type_rent_litt['Type']=='Romans français']['Nb ouvrages'].values[0]
			st.session_state['roman_etranger'] = df_type_rent_litt[df_type_rent_litt['Type']=='Romans étrangers']['Nb ouvrages'].values[0]
			st.session_state['essais'] = df_type_rent_litt[df_type_rent_litt['Type']=='Essais']['Nb ouvrages'].values[0]

			st.write(f"Parmi les ouvrages parus, **:blue[{int(round(st.session_state['roman_francais']/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger']/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais']/len(liste_ean)*100,0))}%]** des essais.")
			
			# Création du barchart horizontal
			with st.container():
				fig_type=px.bar(df_type_rent_litt.sort_values('Nb ouvrages', ascending = True), x='Nb ouvrages',y='Type', orientation='h',
							   text_auto=True)
				fig_type.update_traces(textfont_size=16, textangle=0, textposition="inside", 
									   cliponaxis=False, insidetextfont_color='black')
				fig_type.update_xaxes(showgrid=False,tickfont=dict(size=14), showticklabels=False)
				fig_type.update_yaxes(showgrid=False,tickfont=dict(size=14))
				fig_type.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title=None, yaxis_title=None)
		
				st.plotly_chart(fig_type, use_container_width=True)
				

		with col_text_rl:
			df_caract_livre = st.session_state['caract_livre']
			df_caract_livre['nombre_pages'] = df_caract_livre['nombre_pages'].str.replace('\D', '',regex=True)
			df_caract_livre['prix_indicatif'] = df_caract_livre['prix_indicatif'].str.replace(' €','').str.replace(',','.')
			
			st.dataframe(df_caract_livre)
			
			#nettoyer les valeurs pour conserver uniquement les nombres. Par exemple je retire pages à "138 pages"
					#pour garder 138 que je passerais ensuite en int.
			### ATTENTION, j'ai 9 livres avec 0 pages ou NONE
			nb_pages_total = sum(filter(None, [s for s in df_caract_livre['nombre_pages'].str.replace('\D', '',
											   regex=True).fillna(0).astype('int64')]))
			nb_livre_nb_pages_total = len(list(filter(None, [s for s in df_caract_livre['nombre_pages'].str.replace('\D', '',
											   regex=True).fillna(0).astype('int64')])))
			nb_pages_moyen = int(nb_pages_total/nb_livre_nb_pages_total)
			
			nb_pages_min = min(filter(None, [s for s in df_caract_livre['nombre_pages'].str.replace('\D', '',
											   regex=True).fillna(0).astype('int64')]))
			nb_pages_max = max(filter(None, [s for s in df_caract_livre['nombre_pages'].str.replace('\D', '',
											   regex=True).fillna(0).astype('int64')]))
			
			# même travail avec les prix
			prix_total = round(sum(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])),2)
			nb_livre_prix_total = len(list(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])))
			prix_moyen = round(prix_total/nb_livre_prix_total,2)
			
			prix_min = round(min(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])),2)
			#prix_moyen = round(mean(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])),2)
			prix_max = round(max(filter(None, [s for s in df_caract_livre['prix_indicatif'].fillna(0).astype('float')])),2)
			#st.write(prix_total)
		    
			st.markdown(f"Acheter l'ensemble des livres de la Rentrée Littéraire vous coûtera **:blue[{prix_total}€]**. Avec un nombre total de **:blue[{nb_pages_total}]** pages, c'est **:blue[{nb_pages_total/30}]*** heures de lecture qui vous attend, soit un équivalent de **:blue[{int(nb_pages_total/30/24)}]** jours.")


			colaa, colab, colvideab, colac, colvideac, colad = st.columns([1,1,0.3,3,0.3,2])
			with colaa:
				st.markdown(f':blanc[ .]')
				st.image('./docs/icons8-euro-money-50.png', width=30)
			with colab:
				st.write('Min.')
				st.markdown(prix_min)
			with colvideab:
				st.markdown(':arrow_left:')
			with colac:
				st.markdown('<div style="text-align: center;">Prix Moyen</div>', unsafe_allow_html=True)
				st.markdown(f'<div style="text-align: center;">{prix_moyen}</div>', unsafe_allow_html=True) 
			with colvideac:
				st.markdown(':arrow_right:')
			with colad:
				st.write('Max.')
				st.markdown(prix_max)

			colba, colbb, colvidebb, colbc, colvidebc, colbd = st.columns([1,1,0.3,3,0.3,2])
			with colba:
				st.markdown(f':blanc[ .]')
				st.image('./docs/icons8-terms-and-conditions-50.png', width=30)
			with colbb:
				st.write('Min.')
				st.markdown(nb_pages_min)
			with colvidebb:
				st.markdown(':arrow_left:')
			with colbc:
				st.markdown('<div style="text-align: center;">Nb moyen de pages</div>', unsafe_allow_html=True)
				st.markdown(f'<div style="text-align: center;">{int(nb_pages_total/nb_livre_nb_pages_total)}</div>', unsafe_allow_html=True) 
			with colvidebc:
				st.markdown(':arrow_right:')
			with colbd:
				st.write('Max.')
				st.markdown(nb_pages_max)

			note_page = "*On se base ici sur l'idée qu'un lecteur « normal » lit environs 250 à 300 mots par minute - ce qui représente 1 page toutes les deux minutes, soit environ 30 pages par heure."
			st.markdown(f'<div style="font-size: 12px;">{note_page}</div>', unsafe_allow_html=True)

	
	st.divider()
	
	col_map_2, col_graph_saiso, col_graph_genre = st.columns(3)

	with st.container() :
		# Filtre => uniquement les livres de la Rentree Litteraire
		
		col_map, col_geo_chart = st.columns(2)
		with col_map :
				
			df_rl_dataviz_geo = df_list_livre_rl[['pays','latitude','longitude','continent','nom_complet']].groupby(['pays',
												  'latitude','longitude','continent']).count().reset_index()
			df_rl_dataviz_geo['nom_complet'] = df_rl_dataviz_geo['nom_complet'].astype('int64')
			continent_color = {'EUROPE' : '#00b6cb',
			'NORTH AMERICA': '#124559',
			'ASIA' : '#5e35b1',
			'AFRICA' : '#7cb342',
			'SOUTH AMERICA' : '#598392',
			'CENTRAL AMERICA' : '#aec3b0',
			'OCEANIA' : '#ff7043',
			'CARIBBEAN' : '#f2bedb'}
	
			df_rl_dataviz_geo.insert(4, 'continent_color', df_rl_dataviz_geo.continent.apply(lambda c :continent_color[c]))
			#st.dataframe(df_rl_dataviz_geo)

			nb_livre_vf = len(list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['ean'] != '' and x['livre']['traduit_de'] == 'VF', dico_rl_dataviz.values())))
			nb_livre_hors_vf = len(list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['ean'] != '' and x['livre']['traduit_de'] != 'VF', dico_rl_dataviz.values())))
		
			st.markdown(f"**Répartition Géographique des auteurs (cliquer pour filtrer)**")
			st.markdown(f"Pour rappel : **:blue[{nb_livre_vf}]** sont de langue française, **:blue[{nb_livre_hors_vf}]** sont des traductions.")
			
			st.map(df_rl_dataviz_geo,
			    latitude='latitude',
			    longitude='longitude',
				size= 'nom_complet',
				color='continent_color')
	
		
		with col_geo_chart :
			st.markdown(f"**Top 10 des pays d'origine des auteurs**")
			liste_pays = set(df_list_livre_rl['pays'])
			dico_pays = []
			for pays in liste_pays :
				list_livre_rl_pays = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['ean'] != '' and x['pays'] == pays, dico_rl_dataviz.values()))
				dico_pays.append([pays, len(list_livre_rl_pays)])
	
			df_pays = pd.DataFrame.from_dict(dico_pays).rename(columns={0:'Pays', 1:'Nb ouvrages'})
			#st.write(df_pays)
		
			fig_top_origine_auteur = px.bar(df_pays.sort_values('Nb ouvrages', ascending = True).tail(10), x='Nb ouvrages',
											y='Pays', orientation='h')
			st.plotly_chart(fig_top_origine_auteur, use_container_width=True)
	st.divider()

	# Partie Editeurs
	# Pour Sankey graph
	if 'total_columns_rl' not in st.session_state:
		st.session_state['total_columns_rl'] = pd.DataFrame([[x, x['livre']] for x in list(filter(lambda x: x['livre'] != {}, dico_rl_dataviz.values()))])
		st.session_state['total_columns_rl'] = pd.concat([st.session_state['total_columns_rl'], pd.json_normalize(st.session_state['total_columns_rl'].pop(0))], axis=1).drop(columns=[1])
	
	#dependra du graph voulu
	only_rl = st.session_state['total_columns_rl'][st.session_state['total_columns_rl']['livre.RL']=='RL']
	
	col_edi_img, col_edi_titre= st.columns([0.5,8])
	with col_edi_img :
		st.image('docs/icons8-livres-64.png') 
	with col_edi_titre :
		st.markdown("#### Editeurs")

	#dataframe Editeurs | nb d'ouvrages
	#liste_editeur = set([x['livre']['maison_edition'] for x in dico_rl_dataviz.values() if x['livre']['RL']=='RL'])
	#dico_editeur = []
	#for editeur in liste_editeur :
	#	list_livre_rl_editeur = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['ean'] != '' and x['livre']['maison_edition']==editeur,
	#									 dico_rl_dataviz.values()))
	#	dico_editeur.append([editeur, len(list_livre_rl_editeur)])
	df_nb_livre_x_editeur = only_rl[['livre.maison_edition', 'livre.ean']].groupby('livre.maison_edition').count().sort_values('livre.ean', ascending=False).reset_index()
	#df_nb_livre_x_editeur = pd.DataFrame.from_dict(dico_editeur).rename(columns={0:'editeur', 1:'Nb ouvrages'}).sort_values('Nb ouvrages', ascending=False).reset_index(drop = True)

	df_nb_livre_x_editeur_sup_dix = df_nb_livre_x_editeur[df_nb_livre_x_editeur['livre.ean']>=10]
	st.markdown(f"**Top éditeurs avec plus de 10 ouvrages parus**")
	st.dataframe(df_nb_livre_x_editeur_sup_dix)


	#Dataframe Sankey
	sankey_df = only_rl[['livre.maison_edition','livre.type',  'genre', 'livre.ean']].groupby(['livre.maison_edition','livre.type',  'genre',]).count().sort_values('livre.ean', ascending=False).reset_index().rename(columns = { "livre.maison_edition": 'maison_edition', 'livre.type': 'type', 'livre.ean':'values'})
	
	#pour mon test sur la construction du graphique sankey, je réduis mon analyse sur les editeurs ayant plus de 10 ouvrages à la RL 2023
	liste_editeur = [e for e in df_nb_livre_x_editeur_sup_dix['livre.maison_edition']]
	#st.write(liste_editeur)
	sankey_df = sankey_df[sankey_df['maison_edition'].isin(liste_editeur)]

	#Ici, je crée un dictionnaire permettant d'avoir un index pour les identifier les sources et les targets
	label_sk = [*sankey_df['maison_edition'].unique(), *sankey_df['type'].unique(), *sankey_df['genre'].unique()]
	color = ["rgba(31, 119, 180, 0.8)",
              "rgba(255, 127, 14, 0.8)",
              "rgba(44, 160, 44, 0.8)",
              "rgba(214, 39, 40, 0.8)",
              "rgba(148, 103, 189, 0.8)",
              "rgba(140, 86, 75, 0.8)",
              "rgba(227, 119, 194, 0.8)",
              "rgba(127, 127, 127, 0.8)",
              "rgba(188, 189, 34, 0.8)",
              "rgba(23, 190, 207, 0.8)",
              "rgba(31, 119, 180, 0.8)"]
	
	
	
	dico_label_sk = dict(zip(label_sk,color))
	df_label_sk = pd.DataFrame.from_dict(dico_label_sk, orient = 'index').reset_index().rename(columns = {'index':'maison_edition', 0:'color'}).reset_index()
	st.write(df_label_sk.to_dict())


	#pour la première partie du graph les sources sont les editeurs et les targets les types d'ouvrages. Pour déterminer les valeurs, je passe par un groupby. Pour la deuxièle partie, les sources sont les types d'ouvrages et les targets les genres. Pour les valeurs se sont le nb de livres.
	sankey_df_graph = pd.concat([sankey_df[["maison_edition", "type", "values"]].rename(columns = {"maison_edition": "source", "type": "target"}).groupby(["source", "target"]).sum(),
								 sankey_df[["type", 'genre', "values"]].rename(columns = {"type" : "source", "genre": "target"}).groupby(["source", "target"]).sum()]).reset_index()


	sankey_df_graph.insert(1, 'index_source', sankey_df_graph['source'].apply(lambda x: df_label_sk.to_dict()))
	#sankey_df_graph.insert(3, 'index_target', sankey_df_graph['target'].apply(lambda x: dico_label_sk[x][0]))
	#sankey_df_graph.insert(5, 'index_target', sankey_df_graph['target'].apply(lambda x: dico_label_sk[x][1]))

	#st.dataframe(sankey_df_graph)
	
	sankey_dico_graph = [{"source":s,"target":t,"value":v} for s,t,v in zip(sankey_df_graph['index_source'],sankey_df_graph['index_target'], sankey_df_graph['values'])]
	# override gray link colors with 'source' colors
	opacity = 0.4

	
	
	
	fig_rl = go.Figure(data=[go.Sankey(
	node = dict(
	pad = 15,
	thickness = 20,
	line = dict(color = "black", width = 0.5),
	label = [l for l in dico_label_sk.keys()], #[s for s in sankey_df_graph['source']],#+[t for t in sankey_df['livre.type']],
	color = ["rgba(31, 119, 180, 0.8)",
              "rgba(255, 127, 14, 0.8)",
              "rgba(44, 160, 44, 0.8)",
              "rgba(214, 39, 40, 0.8)",
              "rgba(148, 103, 189, 0.8)",
              "rgba(140, 86, 75, 0.8)",
              "rgba(227, 119, 194, 0.8)",
              "rgba(127, 127, 127, 0.8)",
              "rgba(188, 189, 34, 0.8)",
              "rgba(23, 190, 207, 0.8)",
              "rgba(31, 119, 180, 0.8)"],#"blue",
	),
	link = dict(
	source = [s for s in sankey_df_graph.index_source], # indices correspond to labels, eg A1, A2, A1, B1, …
	target = [t for t in sankey_df_graph.index_target],
	value = [v for v in sankey_df_graph['values']],
	color = ["rgba(31, 119, 180,   0.4)",
              "rgba(255, 127, 14,  0.4)",
              "rgba(44, 160, 44,   0.4)",
              "rgba(214, 39, 40,   0.4)",
              "rgba(148, 103, 189, 0.4)",
              "rgba(140, 86, 75,   0.4)",
              "rgba(227, 119, 194, 0.4)",
              "rgba(127, 127, 127, 0.4)",
              "rgba(188, 189, 34,  0.4)",
              "rgba(23, 190, 207,  0.4)",
              "rgba(31, 119, 180,  0.4)"]	
	))])

	fig_rl.update_layout(
	title_text="Répartition des ouvrages de la Rentrée Littéraire 2023 par éditeur, type et genre",
	font_family="Courier New",
	font_color="blue",
	font_size=12,
	title_font_family="Times New Roman",
	title_font_color="red",
	)
	st.write(fig_rl)

	
##### Pays d'origine des auteurs
	with genre_tab:

		#with col_graph_genre :
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

	
	#### Analyse prix Littéraire
	with prixlitt:#cont_prix_litt :
		with st.sidebar:
			liste_prix_litt = set([pl['nom_prix'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values()])
			select_prix_litt = st.selectbox('Selection prix', liste_prix_litt)
			
			liste_prix_litt_detail = set([pl['nom_prix_detail'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values() 
										 if pl['nom_prix'] == select_prix_litt])
			select_prix_litt_detail = st.selectbox('Selection prix detail', liste_prix_litt_detail, None)


		
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






