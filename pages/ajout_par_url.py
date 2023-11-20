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

st.dataframe(df_rl_total_test.tail())


# 1. Find a book by the Editor name "Emmanuelle"
editeur = st.selectbox("Pick one", list(df_rl_total_test['Editeur'].unique()))

find_editeur = df_rl_total_test.loc[df_rl_total_test['Editeur'] == editeur] #, ['Genre']] = 'F'
st.dataframe(find_editeur)

# 2. choice of a method to add info for a book or add a book
    #Pour ajout automatique
    # url à scraper
with st.form("ajout auto"):
	url_titre = st.text_input('url')
	rl = st.selectbox("RENTREE LITTERAIRE", ['RL', ''])
	premier_roman = st.selectbox('PREMIER ROMAN', ['OUI', 'NON'])
	types_livre = st.selectbox("type livre", ['Romans français' , 'Essais', 'Romans étrangers'])
	genre = st.selectbox('genre', ['F', 'M'])
	
	pays = st.selectbox("Pays", list(df_rl_total_test['PAYS'].unique()), index = None)
	continent = st.selectbox("Continent", list(df_rl_total_test['CONTINENT'].unique()), index = None)
	langue_traduction = st.selectbox("Traduit de", list(df_rl_total_test['Traduit de'].unique()), index = None)
	traducteurice = st.text_input('Traduit par')
	
	nb_index = st.number_input("index")
	
	submit_utl = st.form_submit_button('Submit my picks')

liste_rl_titre = []

if pays == None :
	pays = st.text_input("ajout pays")

if langue_traduction == None :
	langue_traduction = st.text_input("ajout langue")

if continent == None :
	continent = st.text_input("ajout continent")

	
#your code
if submit_utl : 
	data_livre = requests.get(url_titre).content
	data_livre_soup = BeautifulSoup(data_livre,"html.parser")
	
	#### infos du livre ###
	
	## Catégories
	data_livre_cat = data_livre_soup.find('div', attrs={"id" : "main_breadcrumb",
								  "class" : "breadcrumbs"}).findAll('span')
	liste_cat = [cat.get_text(strip=True) for cat in data_livre_cat]
	liste_cat_final = [c for c in liste_cat if c !='›']
	
	## Titre
	data_livre_titre = data_livre_soup.find('h1', attrs={"class" : "product-title"}).get_text(strip=True)
	#print("titre : ", data_livre_titre, "\n")
	
	### Auteur
	try :
		data_livre_auteur = data_livre_soup.find('span', attrs={"class" : "author author--main"}).get_text(strip=True)
	except :
		data_livre_auteur = data_livre_soup.find('a', attrs={"class" : "author author--main trackme"}).get_text(strip=True)
	#print("auteur : ", data_livre_auteur, "\n")
	
	
	### prix grand format
	data_livre_prix_gf = data_livre_soup.find('div', attrs={"class" : "price fp-wide--margin-bottom"}).find('span').get_text(strip=True)#.findAll('span', attrs={"class" : "final-price"})
	#print("prix grand format : ", data_livre_prix_gf, "\n")
	
	### prix ebook
	try :
		data_livre_prix_ebook = data_livre_soup.find('a', attrs={"class" : "ebook"}).get_text(strip=True)
		#print("prix ebook : ", data_livre_prix_ebook, "\n")
	except AttributeError:
		#print("pas de prix ebook", "\n")
		data_livre_prix_ebook = "pas de prix ebook"
	
	
	## Couverture
	data_livre_couv = data_livre_soup.find('source', attrs={"class" : "lozad"})['data-srcset']
	#print("couv", data_livre_couv, "\n")
	
	
	## Caractéristique
	data_livre_carac = data_livre_soup.find('ul', attrs={"class" :"informations-container"}).get_text("|",strip=True) #.find_all('li',attrs{"class" :"information"}).get_text()
	#print("caracteristiques : ", data_livre_carac.get_text(),"\n")
	
	
	dic_rl_parus = {'url' : url_titre, #https://www.decitre.fr/livres/la-femme-a-la-valise-9782376650959.html
		'categorie' : liste_cat_final,
		'titre':data_livre_titre,
		'auteur':data_livre_auteur,
		'prix_gf':data_livre_prix_gf,
		'prix_ebook':data_livre_prix_ebook,
		#'caracteristiques_bis' : temp_dict,
		'couverture':data_livre_couv,
		'caracteristiques':data_livre_carac,
		'RL' : rl,
		'PREMIER_ROMAN' : premier_roman,
		'TYPES' : types_livre,
		'GENRE' : genre,
		'PAYS' : pays,
		'CONTINENT' : continent,
		'Traduit de' : langue_traduction,
		'Traduit par' : traducteurice,
		}
	
	
	## Caractéristique
	data_livre_carac_dict = data_livre_soup.find('ul', attrs={"class" :"informations-container"}).findAll('li', attrs={"class" : "information"})
	for c in data_livre_carac_dict :
		try :
			k = c.find('span').get_text(strip=True)
			v = c.find('div', attrs={"class" :"value"}).get_text(strip=True)
		except AttributeError:
			print("NC")
		dic_rl_parus[k]=v
	
	liste_rl_titre.append(dic_rl_parus)

	df_rl_total_test = pd.concat([df_rl_total_test,pd.DataFrame(liste_rl_titre, index=[int(nb_index)])])

# export au format pickle
df_rl_total_test[1348:].to_pickle("./liste_rl_total_test_pour_prix_litt.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/

df_rl_total_test = pd.read_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/
st.dataframe(df_rl_total_test.tail(60))
