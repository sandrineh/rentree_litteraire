# imageColor.py = https://www.youtube.com/watch?v=6iE95W9cNcI&ab_channel=JCharisTech
# 1.Importation des librairies nécessaires pour le script
#Core Pkgs - Web application
import streamlit as st
from streamlit_option_menu import option_menu

import re

if 'select_prix_liit' not in st.session_state:
	st.session_state['select_prix_liit'] = ''

if 'select_prix_litt_detail' not in st.session_state:
	st.session_state['select_prix_litt_detail'] = ''

if 'df_select_prix_litt_detail' not in st.session_state:
	st.session_state['df_select_prix_litt_detail'] = ''
	
#1. Récupération des data
df_list_livre_rl = st.session_state['df_rl_dataviz_pl']


#### Analyse prix Littéraire
class analysePrixLitt() : 
	#2. Fonction pour afficher la liste des prix litteraires et selectionner le prix litteraire de son choix
	def sidebar_choix_prix():
		with st.sidebar : 
			#choix prix principal
			liste_prix_litt = set([pl['nom_prix'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values()])
			select_prix_litt = st.selectbox('Selection prix', liste_prix_litt)
			st.session_state['select_prix_liit'] = select_prix_litt
	
			#choix de la sub-division du prix
			liste_prix_litt_detail = set([pl['nom_prix_detail'] for l in df_list_livre_rl['livre'] for pl in l['prix_litteraire'].values() 
									  if pl['nom_prix'] == st.session_state['select_prix_liit']])
			select_prix_litt_detail = st.selectbox('Selection prix detail', liste_prix_litt_detail, None)
			st.session_state['select_prix_litt_detail'] = select_prix_litt_detail

	#3. Affichage de la liste des lauréats
	def info_laureat():
		col_laureat_img, col_laureat_titre= st.columns([0.5,8])
		with col_laureat_img :
			st.image('docs/icons8-couronne-de-laurier-80.png') 
		with col_laureat_titre :
			st.markdown('### Liste des lauréats aux Prix littéraire : Rentrée Littéraire 2023')
		
		df_laureat = st.session_state['df_prix_liit'].loc[st.session_state['df_prix_liit']['lauréat'] == 'OUI'].sort_values('nom_prix').reset_index(drop = True)

		#3.1 Je retire l'extension de format des titres
		df_laureat['Livre'] = [re.sub("- Grand Format|- Poche", "", str(x)) for x in df_laureat['Livre']]

		st.dataframe(df_laureat[['Auteur','Livre','maison_edition','nom_prix','nom_prix_detail']])
		
	#4. Fonction pour filtrer et afficher le tableau des livre suivant le prix-detail sélectionné
	def info_choix_prix():
		#Objectif : Afficher la liste des ouvrages avec au moins une sélection à un prix littéraire
		st.markdown('### Liste sélectionné•es par Prix littéraire : Rentrée Littéraire 2023')
		st.dataframe(st.session_state['df_prix_liit'])

		#4.1. Création d'un dataframe filtré sur le prix littéraire choisi
		if st.session_state['select_prix_litt_detail'] == None : 
			df_select_prix_liit = st.session_state['df_prix_liit'][['Auteur','Livre','maison_edition','nom_prix', 'nom_prix_detail','premiere_selection','deuxieme_selection','troisieme_selection','lauréat']].sort_values(['nom_prix','nom_prix_detail']).reset_index(drop = True)
		else :
			df_select_prix_liit = st.session_state['df_prix_liit'].loc[st.session_state['df_prix_liit']['nom_prix_detail'] == st.session_state['select_prix_litt_detail']][['lauréat','Auteur','Livre','maison_edition','nom_prix','nom_prix_detail',
							'premiere_selection','deuxieme_selection','troisieme_selection']].sort_values('nom_prix').reset_index(drop = True)

		###############
		#2.1 Je conserve un URL de couverture afin d'afficher la couv dans la colonne "couverture"
		#df_couv_livre_select_edit['couverture'] = df_couv_livre_select_edit['couverture'].apply(lambda i : re.sub("\s+(\d\D)", "", i.split(',')[1])
														 #if len(i.split(',')) > 1 else re.sub("\s+(\d\D)", "", i))
		#2.2 Je retire l'extension de format des titres
		df_select_prix_liit['Livre'] = [re.sub("- Grand Format|- Poche", "", str(x)) for x in df_select_prix_liit['Livre']]
		###############



		
		st.session_state['df_select_prix_litt_detail'] = df_select_prix_liit
		
		#4.2. Fonction pour mettre en couleur le titre qui est lauréat pour un prix
		def cooling_highlight(val):
			color = '#6dd3ce' if val == 'OUI' else ''
			return f'background-color: {color}'
		
		select_prix_liit_style = df_select_prix_liit.style.applymap(cooling_highlight, subset=['lauréat'])

		#4.3. Affichage du dataframe
		#st.dataframe(select_prix_liit_style)
		with st.expander('Voir la liste des ouvrages sélectionnés') : 
			edited_df = st.data_editor(
			    select_prix_liit_style,
			    column_config={
			        "lauréat": "Lauréat",
					"maison_edition": "Editeur",
					"nom_prix": None,
					'nom_prix': None,
					'nom_prix_detail': None,
					'premiere_selection': None,
					'deuxieme_selection': None,
					'troisieme_selection': None,
			    #    "rating": st.column_config.NumberColumn(
			    #        "Your rating",
			    #        help="How much do you like this command (1-5)?",
			    #        min_value=1,
			    #        max_value=5,
			    #        step=1,
			    #        format="%d ⭐",
			    #    ),
			    #    "is_widget": "Widget ?",
			    },
			    #disabled=["command", "is_widget"],
			    hide_index=True,
			)
		nom_prix_detail = st.session_state['select_prix_litt_detail']
		laureat_prix = edited_df.loc[edited_df["lauréat"] == 'OUI']["Auteur"].values[0]
		titre_livre_laureat = edited_df.loc[edited_df["lauréat"] == 'OUI']["Livre"].values[0]
		col_couv_laureat, col_texte_laureat, col_vide_laureat = st.columns([1,4,3])
		with col_couv_laureat:
			st.image('docs/icons8-couronne-de-laurier-80.png')
		with col_texte_laureat:
			st.markdown(f"Le/la lauréat•e du prix **{nom_prix_detail}** est\n **{laureat_prix}** pour le livre\n **{titre_livre_laureat}**")

	#5. Affichage des livres sélectionnées par Prix Littéraire suivant sélection dans sidebar. Tout est affiché si pas de sélection.
	def info_course():
		
		select_prix_liit= st.session_state['df_select_prix_litt_detail']
		#Affichage des livres suivant leur niveau de sélection
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

		
###################### ___________________
#def do_info_prix_litt():
#	
#
#
#
#
##Pour afficher la liste des ouvrages avec au moins une sélection à un prix littéraire
#def select_pl(pl):
#	if pl == None : 
#		select_prix_liit = st.session_state['df_prix_liit'][['Auteur','Livre','maison_edition','nom_prix', 'nom_prix_detail','premiere_selection','deuxieme_selection','troisieme_selection','lauréat']].sort_values(['nom_prix','nom_prix_detail']).reset_index(drop = True)
#	else :
#		select_prix_liit = st.session_state['df_prix_liit'].loc[st.session_state['df_prix_liit']['nom_prix_detail'] == pl]
#		#select_prix_liit = pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list_livre_prix_litt for y in x['livre']['prix_litteraire'].values() if y['nom_prix_detail'] == pl], columns = ['Auteur','Livre','maison_edition','prix'])
#		#select_prix_liit = pd.concat([select_prix_liit , pd.json_normalize(select_prix_liit.pop("prix"))], axis=1)
#		
#	return select_prix_liit #[['Auteur','Livre','maison_edition','prix']]
	
##Fonction pour mettre en lumière le titre qui est lauréat pour un prix
#def cooling_highlight(val):
#	color = '#6dd3ce' if val == 'OUI' else ''
#	return f'background-color: {color}'
		
##Affichage de la liste des lauréats
#col_laureat_img, col_laureat_titre= st.columns([0.5,8])
#with col_laureat_img :
#	st.image('docs/icons8-couronne-de-laurier-80.png') 
#with col_laureat_titre :
#	st.markdown('### Liste des lauréats aux Prix littéraire : Rentrée Littéraire 2023')
#
#df_laureat = st.session_state['df_prix_liit'].loc[st.session_state['df_prix_liit']['lauréat'] == 'OUI'].sort_values('nom_prix').reset_index(drop = True)
#
##pd.DataFrame([[x['nom_complet'], x['livre']['titre'], x['livre']['maison_edition'],y] for x in list_livre_prix_litt for y in x['livre']['prix_litteraire'].values() if y['lauréat'] == 'OUI'] , columns = ['Auteur','Livre','maison_edition','prix'])
##df_laureat = pd.concat([df_laureat , pd.json_normalize(df_laureat.pop("prix"))], axis=1)
#
#st.dataframe(df_laureat[['Auteur','Livre','maison_edition','nom_prix','nom_prix_detail']])
#	
##Affichage des livres sélectionnées par Prix Littéraire suivant sélection dans sidebar. Tout est affiché si pas de sélection.
#st.markdown('### Liste sélectionné•es par Prix littéraire : Rentrée Littéraire 2023')
#select_prix_liit = select_pl(st.session_state['select_prix_litt_detail'])
#select_prix_liit = select_prix_liit[['lauréat','Auteur','Livre','maison_edition','nom_prix','nom_prix_detail',
#								   'premiere_selection','deuxieme_selection','troisieme_selection']].sort_values('nom_prix').reset_index(drop = True)
#
#select_prix_liit_style = select_prix_liit.style.applymap(cooling_highlight, subset=['lauréat'])
#
#st.dataframe(select_prix_liit_style)
#
##### A SUPPRIMER PLUS HAUT
		
##Affichage des livres suivant leur niveau de sélection
#start_color, end_color = st.select_slider(
#	'Select a range of color wavelength',
#	options=['Première sélection', 'Deuxième sélection', 'Troisième sélection'],
#	value=('Première sélection', 'Troisième sélection'))
#st.write('You selected wavelengths between', start_color, 'and', end_color)
#
#if start_color == 'Première sélection' and end_color == 'Troisième sélection' :
#	st.dataframe(select_prix_liit.loc[select_prix_liit.troisieme_selection == 'OUI'])
#elif start_color == 'Première sélection' and end_color == 'Deuxième sélection' :
#	st.dataframe(select_prix_liit.loc[select_prix_liit.deuxieme_selection == 'OUI'])
#else : 
#	st.dataframe(select_prix_liit.loc[select_prix_liit.premiere_selection == 'OUI'])
		
###################### ___________________

#class InfoPrixLitt():
	#Affichage texts d'intro
	#def intro_form():
			# --------------- PRESENTATION DE LA PARTIE FORMULAIRE
#			st.header("INFOS FORMULAIRE")
#			st.write(""" En s'inspirant de l'étude Cinégalités du Collectif 50/50(1), l'objectif ici est d'étendre son périmètre (remonter dans le temps, plateformes indépendantes, séries) 
#				et automatiser la collecte de données pour les films d'initiative française(2).""")
#	
#			st.markdown(f'<p style="font-size:10px;">(1) Rapport Cinégalité (<a style="font-size:10px;" href="https://collectif5050.com/wordpress/wp-content/uploads/2022/05/Cinegalite-s-Rapport.pdf">Télecharger le rapport complet</a>) <br> (2) film d\'initiative française (FIF): "Un Film d’Initiative Française est un film agréé par le CNC dont le financement est majoritairement ou intégralement français. Ces Films d’Initiative Française peuvent être coproduits avec des coproducteurs étrangers mais, dans ce cas, la part étrangère sera minoritaire" (Source : (<a style="font-size:10px;" href="https://www.afar-fiction.com/IMG/pdf/L_economie_des_films_francais.pdf">Afar Fiction</a>)</p>', unsafe_allow_html=True)
#			
#			with st.expander("Principe"):
#				st.write(""" Ce formulaire est la version numérique de la grille de visionnage 
#				de l'étude Cinégalité. L'objectif est ici de recueillir les données relatives aux personnages locuteurs récurrents. 
#				On entend par là les personnages "apparaissant au moins dans deux séquences dans lesquelles ils s’expriment".
#				Les données sont de trois ordres : \n
#	-les caractéristiques sociodémographiques des personnages, \n
#	-leur place dans la narration,\n
#	-certains éléments relatifs à leurs actions ou à leur trajectoire dans le récit".""")
#	
#			st.write("""Méthodologie :\n
#	1) Sélectionnez le film (FIF) de votre choix. S'il n'est pas dans la liste, renseignez le champs vide.\n
#	2) Renseignez les champs du formulaire. Vous pouvez vous aider du menu à gauche pour accédez à un thème du questionnaire.
#				>>A noter : l'idéal est de remplir tous les champs.\n
#	3) une fois que vous avez terminé,cliquer sur "Submit". Deux options s'offrent alors à vous :\n
#		1) poursuivre et renseigner un nouveau film \n
#		2) terminer en cliquant sur "End" """)