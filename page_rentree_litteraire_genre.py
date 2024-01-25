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
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import time
import re

import json

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

# 1. Classe lancée si choix de "rentrée littéraire" dans le menu en sidebar
def graph_genre(genre):
	fig_type=px.bar(df_type_rent_litt[df_type_rent_litt['Genre']==genre].sort_values('Nb ouvrages', ascending = True), x='Nb ouvrages',y='Type', orientation='h', text_auto=True)
	fig_type.update_traces(textfont_size=16, textangle=0, textposition="inside", 
										   cliponaxis=False, insidetextfont_color='black')
	fig_type.update_xaxes(showgrid=False,tickfont=dict(size=14), showticklabels=False)
	fig_type.update_yaxes(showgrid=False,tickfont=dict(size=14))
	fig_type.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title=None, yaxis_title=None)
	return fig_type
	

class InfoRentreeLittGenre():
	def do_info_rl_genre():
		liste_ean = st.session_state['liste_ean']
		df_list_livre_rl = st.session_state['df']
		dico_rl_dataviz = st.session_state['dico']

		liste_ean = set([l['ean'] for l in df_list_livre_rl['livre']])

		col_graph_rl, col_text_rl = st.columns(2, gap='small')
		with col_graph_rl : 
			dico_rent_litt = []
			liste_type_rent_litt = ['Romans français', 'Romans étrangers', 'Essais']
			for type in liste_type_rent_litt :
				for genre in ["F", "M", "MIXTE", "NB", "NC"] : 
					#Filtre afin de supprimer les titres qui ne sont pas de la rentrée littéraire dans le dico
					liste_type_rent_litt_temp = list(filter(lambda x: x['livre']['RL'] != '' and x['livre']['type'] == type and x['genre'] == genre,
													 dico_rl_dataviz.values()))
					#creation d'un dico avec le type d'un ouvrage, le genre de l'auteur.ice, le nb d'ouvrages pour le croisement type x genre
					dico_rent_litt.append([type, genre, len(liste_type_rent_litt_temp)])
		
			df_type_rent_litt = pd.DataFrame.from_dict(dico_rent_litt).rename(columns={0:'Type', 1:'Genre', 2:'Nb ouvrages'})
			
			st.session_state['roman_francais'] = df_type_rent_litt[df_type_rent_litt['Type']=='Romans français']#['Nb ouvrages'].sum()
			st.session_state['roman_etranger'] = df_type_rent_litt[df_type_rent_litt['Type']=='Romans étrangers']#['Nb ouvrages'].sum()
			st.session_state['essais'] = df_type_rent_litt[df_type_rent_litt['Type']=='Essais']#['Nb ouvrages'].sum()
	

			# Création du barchart horizontal
			def graph_genre(genre):
				fig_type=px.bar(df_type_rent_litt[df_type_rent_litt['Genre']==genre].sort_values('Nb ouvrages', ascending = True), x='Nb ouvrages',y='Type', orientation='h', text_auto=True)
				fig_type.update_traces(textfont_size=16, textangle=0, textposition="inside", 
													   cliponaxis=False, insidetextfont_color='black')
				fig_type.update_xaxes(showgrid=False,tickfont=dict(size=14), showticklabels=False)
				fig_type.update_yaxes(showgrid=False,tickfont=dict(size=14))
				fig_type.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title=None, yaxis_title=None)
				return fig_type
			# Choix du niveau de sélection
			selection = st.radio(
				"Consulter la liste des ouvrages de la ",
				df_type_rent_litt['Genre'].unique(),
				index=None,
				horizontal=True)
			
			if selection == "F":
				st.write('Female')
					
				st.write(f"Parmi les ouvrages parus et écrits par des autrices, **:blue[{int(round(st.session_state['roman_francais'][st.session_state['roman_francais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger'][st.session_state['roman_etranger']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais'][st.session_state['essais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des essais.")

				with st.container():
					st.plotly_chart(graph_genre(selection), use_container_width=True)
					#fig_type=px.bar(df_type_rent_litt[df_type_rent_litt['Genre']==selection].sort_values('Nb ouvrages', ascending = True), x='Nb ouvrages',y='Type', orientation='h', text_auto=True)
					#fig_type.update_traces(textfont_size=16, textangle=0, textposition="inside", 
										   #cliponaxis=False, insidetextfont_color='black')
					#fig_type.update_xaxes(showgrid=False,tickfont=dict(size=14), showticklabels=False)
					#fig_type.update_yaxes(showgrid=False,tickfont=dict(size=14))
					#fig_type.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title=None, yaxis_title=None)
			
					#st.plotly_chart(fig_type, use_container_width=True)
				
			elif selection == "M":
				st.write("Male")
				st.write(f"Parmi les ouvrages parus et écrits par des auteurs, **:blue[{int(round(st.session_state['roman_francais'][st.session_state['roman_francais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger'][st.session_state['roman_etranger']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais'][st.session_state['essais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des essais.")

				with st.container():
					st.plotly_chart(graph_genre(selection), use_container_width=True)

			elif selection == "MIXTE":
				st.write("Mixte")
				st.write(f"Parmi les ouvrages parus et écrits par des auteurs, **:blue[{int(round(st.session_state['roman_francais'][st.session_state['roman_francais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger'][st.session_state['roman_etranger']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais'][st.session_state['essais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des essais.")

				with st.container():
					st.plotly_chart(graph_genre(selection), use_container_width=True)

			elif selection == "NB":
				st.write("Non binaire")
				st.write(f"Parmi les ouvrages parus, **:blue[{int(round(st.session_state['roman_francais'][st.session_state['roman_francais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger'][st.session_state['roman_etranger']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais'][st.session_state['essais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des essais.")

				with st.container():
					st.plotly_chart(graph_genre(selection), use_container_width=True)

			elif selection == "NC":
				st.write("Non communiqué")
				st.write(f"Parmi les ouvrages parus, **:blue[{int(round(st.session_state['roman_francais'][st.session_state['roman_francais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger'][st.session_state['roman_etranger']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais'][st.session_state['essais']['Genre']==selection]['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des essais.")

				with st.container():
					st.plotly_chart(graph_genre(selection), use_container_width=True)
					
			else:
				st.write(f"Parmi les ouvrages parus, **:blue[{int(round(st.session_state['roman_francais']['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** sont des romans français, **:blue[{int(round(st.session_state['roman_etranger']['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des romans étrangers et **:blue[{int(round(st.session_state['essais']['Nb ouvrages'].sum()/len(liste_ean)*100,0))}%]** des essais.")

				with st.container():
					st.plotly_chart(graph_genre(selection), use_container_width=True)
			
			# Création du barchart horizontal
			#with st.container():
			#	fig_type=px.bar(df_type_rent_litt.sort_values('Nb ouvrages', ascending = True), x='Nb ouvrages',y='Type', orientation='h',
			#				   color = 'Genre', text_auto=True)
			#	fig_type.update_traces(textfont_size=16, textangle=0, textposition="inside", 
			#						   cliponaxis=False, insidetextfont_color='black')
			#	fig_type.update_xaxes(showgrid=False,tickfont=dict(size=14), showticklabels=False)
			#	fig_type.update_yaxes(showgrid=False,tickfont=dict(size=14))
			#	fig_type.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title=None, yaxis_title=None)
		
			#	st.plotly_chart(fig_type, use_container_width=True)
			
		with col_text_rl:
			df_caract_livre = st.session_state['caract_livre']
			df_caract_livre['nombre_pages'] = df_caract_livre['nombre_pages'].str.replace('\D', '',regex=True)
			df_caract_livre['prix_indicatif'] = df_caract_livre['prix_indicatif'].str.replace(' €','').str.replace(',','.')
			
			#st.dataframe(df_caract_livre)
			
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
				st.image('./docs/icons8-money_bag_euro-50_FFA400.png', width=30) 
			with colab:
				st.write('Min.')
				st.markdown(prix_min)
			with colvideab:
				st.markdown(':arrow_left:')
			with colac:
				st.markdown('<p style="text-align: center;">Prix Moyen</p>', unsafe_allow_html=True)
				st.markdown(f'<div style="text-align: center;">{prix_moyen}</div>', unsafe_allow_html=True) 
			with colvideac:
				st.markdown(':arrow_right:')
			with colad:
				st.write('Max.')
				st.markdown(prix_max)

			colba, colbb, colvidebb, colbc, colvidebc, colbd = st.columns([1,1,0.3,3,0.3,2])
			with colba:
				st.markdown(f':blanc[ .]')
				st.image('./docs/icons8-termes-et-conditions-50_FFA400.png', width=30)
			with colbb:
				st.write('Min.')
				st.markdown(nb_pages_min)
			with colvidebb:
				st.markdown(':arrow_left:')
			with colbc:
				st.markdown('<p style="text-align: center;">Nb moyen de pages</p>', unsafe_allow_html=True)
				st.markdown(f'<div style="text-align: center;">{int(nb_pages_total/nb_livre_nb_pages_total)}</div>', unsafe_allow_html=True) 
			with colvidebc:
				st.markdown(':arrow_right:')
			with colbd:
				st.write('Max.')
				st.markdown(nb_pages_max)

			note_page = "*On se base ici sur l'idée qu'un lecteur « normal » lit environs 250 à 300 mots par minute - ce qui représente 1 page toutes les deux minutes, soit environ 30 pages par heure."
			st.markdown(f'<div style="font-size: 12px;">{note_page}</div>', unsafe_allow_html=True)

	
		#st.divider()

	def do_info_editeur():
		#objectif: Partie Editeurs # Pour Sankey graph

		#1. Récupération des data
		df_list_livre_rl = st.session_state['df']
		dico_rl_dataviz = st.session_state['dico']

		if 'total_columns_rl' not in st.session_state:
			st.session_state['total_columns_rl'] = pd.DataFrame([[x, x['livre']] for x in list(filter(lambda x: x['livre'] != {}, dico_rl_dataviz.values()))])
			st.session_state['total_columns_rl'] = pd.concat([st.session_state['total_columns_rl'], pd.json_normalize(st.session_state['total_columns_rl'].pop(0))], axis=1).drop(columns=[1])
		
			#dependra du graph voulu
		only_rl = st.session_state['total_columns_rl'][st.session_state['total_columns_rl']['livre.RL']=='RL']

		#2. stucture et affichage du contenu
		
		col_edi_img, col_edi_titre= st.columns([0.5,8])
		with col_edi_img :
			st.image('docs/icons8-knowledge-64.png') 
		with col_edi_titre :
			st.markdown("#### Editeurs")
			
		col_top_edi, col_sankey_edi= st.columns([3,8])
		with col_top_edi :
			with st.container(border = True):
				#Affichage titre de la colonne
				st.markdown(f"**Top éditeurs avec plus de 10 ouvrages parus**")
				
				#Creation du df du nb de livre par editeur
				df_nb_livre_x_editeur = only_rl[['livre.maison_edition', 'livre.ean']].groupby('livre.maison_edition').count().sort_values('livre.ean', ascending=False).reset_index()
				#Réduction du df aux editeurs avec plus ou égal 10 lvres
				df_nb_livre_x_editeur_sup_dix = df_nb_livre_x_editeur[df_nb_livre_x_editeur['livre.ean']>=10]
				#Affichage du df final
				st.dataframe(df_nb_livre_x_editeur_sup_dix)
						
		with col_sankey_edi :
			with st.container(border = True):
				st.write('sankey')	
				#Dataframe pour la creation du graph de type Sankey
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
				#st.dataframe(df_label_sk)
			
				#pour la première partie du graph les sources sont les editeurs et les targets les types d'ouvrages. Pour déterminer les valeurs, je passe par un groupby. Pour la deuxièle partie, les sources sont les types d'ouvrages et les targets les genres. Pour les valeurs se sont le nb de livres.
				sankey_df_graph = pd.concat([sankey_df[["maison_edition", "type", "values"]].rename(columns = {"maison_edition": "source", "type": "target"}).groupby(["source", "target"]).sum(),
											 sankey_df[["type", 'genre', "values"]].rename(columns = {"type" : "source", "genre": "target"}).groupby(["source", "target"]).sum()]).reset_index()
			
				
				sankey_df_graph.insert(1, 'index_source', sankey_df_graph['source'].apply(lambda x: df_label_sk[df_label_sk['maison_edition']==x]['index'].values[0]))
				sankey_df_graph.insert(3, 'index_target', sankey_df_graph['target'].apply(lambda x: df_label_sk[df_label_sk['maison_edition']==x]['index'].values[0]))
				sankey_df_graph.insert(4, 'color', sankey_df_graph['source'].apply(lambda x: df_label_sk[df_label_sk['maison_edition']==x]['color'].values[0]))
				
				#st.dataframe(sankey_df_graph)
				
				# override gray link colors with 'source' colors
				opacity = 0.4
				
				fig_rl = go.Figure(data=[go.Sankey(
				node = dict(
				pad = 15,
				thickness = 20,
				line = dict(color = "black", width = 0.5),
				label = [l for l in dico_label_sk.keys()],
				color = [c for c in df_label_sk['color']],
				),
				link = dict(
				source = [s for s in sankey_df_graph.index_source], # indices correspond to labels, eg A1, A2, A1, B1, …
				target = [t for t in sankey_df_graph.index_target],
				value = [v for v in sankey_df_graph['values']],
				color = [c.replace('0.8',str(opacity)) for c in sankey_df_graph['color']]	
				))])
			
				fig_rl.update_layout(
				title_text="Répartition des ouvrages de la Rentrée Littéraire 2023 par éditeur, type et genre",
				font_family="Courier New",
				font_color="blue",
				font_size=12,
				#title_font_family="Times New Roman",
				title_font_color="white",
				)
		
				#st.markdown(f"**Répartition des ouvrages de la Rentrée Littéraire 2023 par éditeur, type et genre**")
				with st.container(border=True): 
					st.plotly_chart(fig_rl, use_container_width=True)

	
		with st.container(border = True):
			st.markdown(f"**On the cover of...**")
			col_choix_edit, col_couv_edi= st.columns([3,8])
			with col_choix_edit:
				with st.container(border = True):
					st.write('choix Editeur')
					#création du df
					df_couv_livre = st.session_state['couv_livre'].loc[st.session_state['couv_livre']['RL'] =='RL']
					df_couv_livre = df_couv_livre[['Auteur', 'Livre', 'maison_edition', 'RL', 'couverture']]
					df_couv_livre['couverture'] = df_couv_livre['couverture'].apply(lambda i : re.sub("\s+(\d\D)", "", i.split(',')[1])
														 if len(i.split(',')) > 1 else re.sub("\s+(\d\D)", "", i))
					df_couv_livre['Livre'] = df_couv_livre['Livre'].apply(lambda i : re.sub("- Grand Format|- Poche", "", str(i)))
	
					# --------------- DEBUT CHOIX IMAGE + COMPUTER VISION
							#"""
							#	L'idée est ici de créer une vue de visuels de couvertures de livres alignés
							#	1. Dans un premier temps, dans un container, 
									# je mets la liste des urls des images dans une liste et le nom du livre dans une autre
							#	2. Je crée la possibilité de sélectionné le ou les livres que je veux afficher
							#	3. Si je retrouve le titre de la selection dans la liste totale alors j'affiche l'image correspondante
							#"""
					
					#Fonction pour choix editeurs
					def load_images():
						titres_livres = []
						image_files = []
						for i,b in zip(df_couv_livre['couverture'],df_couv_livre['Livre']): #i=image, b=book
							if len(i.split(',')) > 1:
								i_replace = i.split(',')[1]
							else :
								i_replace = i
							image_link = re.sub("\s+(\d\D)", "", i_replace)
							image_files.append(image_link)
				
							part = image_link.replace('.webp','').split('/')
							
							if b not in titres_livres :
								titres_livres.append(b)
							
						return image_files, titres_livres
						
					image_files, titres_livres = load_images()
	
					# creation de la liste des editeurs
					liste_editeur= set([edi for edi in df_couv_livre['maison_edition']])
					
					select_editeur = st.selectbox("Selectionnez une maison d'éditions", liste_editeur)
					st.session_state['select_editeur'] = select_editeur
					# creation de la liste des titres pour l'editeur sélectionné
					liste_titre_par_editeur = set([titre for edi,couv,titre in zip(df_couv_livre['maison_edition'], df_couv_livre['couverture'],
																				 df_couv_livre['Livre']) if edi == select_editeur])
					n = st.number_input("select images grid", 1,7,5)

			with col_couv_edi : 
				with st.container(border = True):
					st.write('Couv affichées')

				#st.write(liste_couv_par_editeur)
				#select_couv_par_editeur = st.selectbox('Selection un ou plusieurs ouvrages', liste_couv_par_editeur, None)
					
				#view_titres_livres = st.multiselect("select image(s)", liste_titre_par_editeur, liste_titre_par_editeur)
					st.session_state['liste_ouvrage'] = liste_titre_par_editeur
					view_images = []
					# Si je retrouve le titre de la selection dans la liste totale alors j'affiche l'image correspondante
					for image_file, titre_livre in zip(image_files, titres_livres) :
						#st.write(image_file, titre_livre )
						if titre_livre in liste_titre_par_editeur :#view_titres_livres:
							view_images.append(image_file)
					
					groups = []
					for i in range(0, len(view_images), n):
						groups.append(view_images[i:i+n])
					##with col_titre_livre :
					for group in groups:
						cols = st.columns(n)
						for i, image_file in enumerate(group):
							cols[i].image(image_file, use_column_width=True)

			# --------------- FIN CHOIX IMAGE + COMPUTER VISION
							
		##### IDEE
		#choisir les maisons d'édition et voir le graph sankey s'adapter en fonction 
		#sinon affiche par défaut le sankey des editeurs qui ont sorti au moins 10 ouvrages

	def do_info_ouvrage():
		#objectif: Partie Ouvrages suivant l'éditeurs
		
		#1. Récupération des data
		df_couv_livre = st.session_state['couv_livre'].loc[st.session_state['couv_livre']['RL'] =='RL']

		#2. Je filtre sur l'éditeur sélectionné
		df_couv_livre_select_edit = df_couv_livre[['maison_edition', 'Auteur', 'Livre', 'couverture']].loc[ df_couv_livre['maison_edition']== st.session_state['select_editeur']]
		#2.1 Je conserve un URL de couverture afin d'afficher la couv dans la colonne "couverture"
		df_couv_livre_select_edit['couverture'] = df_couv_livre_select_edit['couverture'].apply(lambda i : re.sub("\s+(\d\D)", "", i.split(',')[1])
														 if len(i.split(',')) > 1 else re.sub("\s+(\d\D)", "", i))
		#2.2 Je retire l'extension de format des titres
		df_couv_livre_select_edit['Livre'] = [re.sub("- Grand Format|- Poche", "", str(x)) for x in df_couv_livre_select_edit['Livre']]


		#3. Titre du container avec icone
		col_edi_img, col_edi_titre= st.columns([0.5,8])
		with col_edi_img :
			st.image('docs/icons8-livres-64_FFA400.png') 
		with col_edi_titre :
			st.markdown("#### Liste des ouvrages")
			
		#4. Colonnes liste ouvrage & nuage de mots
		col_liste_livre, col_nuage_mot= st.columns([5,3])
		#4.1 Pour afficher la couverture de l'ouvrage plutôt que l'url dans la colonne "couverture"
		with col_liste_livre:
			st.markdown(f"**Liste des ouvrages**")
			st.data_editor(
				df_couv_livre_select_edit,
				column_config={
					"couverture": st.column_config.ImageColumn(
						"couverture", help="Streamlit app preview screenshots"
					)
				},
				hide_index=True,
			)

		with col_nuage_mot: 
			st.markdown(f"**Nuage de mots**")
			from nuagemot import create_wordcloud
			topic = ' '.join(st.session_state['liste_ouvrage'])

			# Retrait des stopwords
			wordcloud = create_wordcloud(topic)
		
			# Display the generated image:
			def couleur(*args, **kwargs):
			    import random
			    return "rgb(0, 100, {})".format(random.randint(100, 255))
			
			fig, ax = plt.subplots(figsize = (12, 8))
			ax.imshow(wordcloud.recolor(color_func = couleur), )
			plt.axis("off")
			st.pyplot(fig)
			
			
class InfoRentreeLittGeo(): 
	def do_info_geo():
		df_list_livre_rl = st.session_state['df']
		dico_rl_dataviz = st.session_state['dico']
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


	
#with st.container(border = True):
#			st.write('containe 1')
#			col_log, col_tr= st.columns([0.5,8])
#			with col_log :
#				with st.container(border = True):
#					st.write('logo')
#			with col_tr :
#				with st.container(border = True):
#					st.write('nom container')
#				
#			col_A, col_B= st.columns([3,8])
#			with col_A :
#				with st.container(border = True):
#					st.write('Top Editeur')
#			with col_B :
#				with st.container(border = True):
#					st.write('Couv pour editeur')
#					col_C, col_D= st.columns([3,8])
#					with col_C :
#						with st.container(border = True):
#							st.write('choix Editeur')
#					with col_D :
#						with st.container(border = True):
#							st.write('Couv affichees')
#			with st.container(border = True):
#				st.write('sankey')	