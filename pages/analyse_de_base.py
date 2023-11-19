
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



# 3.Setup de l'application Streamlit  - Streamlit webpage properties / set up the app with wide view preset and a title
st.set_page_config(page_title="Rentree Litteraire", page_icon="books", layout="wide")

st.write("RL_2023 GO")

#df_rl_total = pd.read_pickle("liste_rl_total.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/
#df_rl_total.tail(2)



#### Import pickel pour test

df_rl_total_test = pd.read_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/

st.sidebar.success("Select an add method.")


row_nb = int(st.number_input('which row number ?'))

if st.button('drop index'):
    df_rl_total_test = df_rl_total_test.drop(index = row_nb)
    
if st.button("drop duplicate") :
    df_rl_total_test = df_rl_total_test[~df_rl_total_test.index.duplicated(keep='first')]

st.dataframe(df_rl_total_test.tail())


# 1. Find a book by the Editor name "Emmanuelle"
editeur = st.selectbox("Pick one", list(df_rl_total_test['Editeur'].unique()))

find_editeur = df_rl_total_test.loc[df_rl_total_test['Editeur'] == editeur] #, ['Genre']] = 'F'
st.dataframe(find_editeur)

# 2. choice of a method to add info for a book or add a book
#tab1, tab2, tab3 = st.tabs(["Ajout infos manquantes", "Ajout Automatique (url)", "Ajout Manuel"])
#tab1.write("this is tab 1")
#tab2.write("this is tab 2")


#with tab1:
#    with st.form("my_form"):
#        st.write("Inside the form")
#        nb_index = st.number_input('index')
#        prem_roman = st.selectbox('PREMIER ROMAN', ['OUI', 'NON'])
#        quel_genre = st.selectbox('genre', ['F', 'M'])
#        quel_pays = st.selectbox("Pays", list(df_rl_total_test['PAYS'].unique()), index = None)
#        quel_continent = st.selectbox("Continent", list(df_rl_total_test['CONTINENT'].unique()))
#        trad_de = st.selectbox("Traduit de", list(df_rl_total_test['Traduit de'].unique()), index = None)
#        trad_par = st.text_input('Traduit par')
#        st.form_submit_button('Submit my picks')
#
#    if quel_pays == None:
#        quel_pays = st.text_input("ajout pays")
#    
#    if trad_de == None :
#        trad_de = st.text_input("ajout langue")
#
#    #nb_index = float(nb_index)
#    df_rl_total_test.loc[int(nb_index),'RL'] = 'RL'
#    df_rl_total_test.loc[int(nb_index),'PREMIER_ROMAN'] = prem_roman #'PREMIER ROMAN'
#    df_rl_total_test.loc[int(nb_index),'TYPES'] = 'Romans étrangers'
#    df_rl_total_test.loc[int(nb_index),'GENRE'] = quel_genre
#    df_rl_total_test.loc[int(nb_index),'PAYS'] = quel_pays
#    df_rl_total_test.loc[int(nb_index),'CONTINENT'] = quel_continent #'EUROPE'
#    df_rl_total_test.loc[int(nb_index),'Traduit de'] = trad_de
#    df_rl_total_test.loc[int(nb_index),'Traduit par'] = trad_par


#with tab2 : 
#    #Pour ajout automatique
#    # url à scraper
#    with st.form("ajout auto"):
#        url_titre = st.text_input('url')
#        premier_roman = st.selectbox('PREMIER ROMAN', ['OUI', 'NON'])
#        types_livre = st.selectbox("type livre", ['Romans français' , 'Essais', 'Romans étrangers'])
#        genre = st.selectbox('genre', ['F', 'M'])
#        
#        pays = st.selectbox("Pays", list(df_rl_total_test['PAYS'].unique()))
#        continent = st.selectbox("Continent", list(df_rl_total_test['CONTINENT'].unique()))
#        langue_traduction = st.selectbox("Traduit de", list(df_rl_total_test['Traduit de'].unique()))
#        traducteurice = st.text_input('Traduit par')
#        
#        nb_index = st.number_input("index")
#        
#        submit_utl = st.form_submit_button('Submit my picks')
#    
#    liste_rl_titre = []
#
#    if pays == None :
#        pays = st.text_input("ajout pays")
#    
#    if traducteurice == None :
#        traducteurice = st.text_input("ajout langue")
#        
#    #your code
#    if submit_utl : 
#        data_livre = requests.get(url_titre).content
#        data_livre_soup = BeautifulSoup(data_livre,"html.parser")
#        
#        #### infos du livre ###
#        
#        ## Catégories
#        data_livre_cat = data_livre_soup.find('div', attrs={"id" : "main_breadcrumb",
#                                      "class" : "breadcrumbs"}).findAll('span')
#        liste_cat = [cat.get_text(strip=True) for cat in data_livre_cat]
#        liste_cat_final = [c for c in liste_cat if c !='›']
#        
#        ## Titre
#        data_livre_titre = data_livre_soup.find('h1', attrs={"class" : "product-title"}).get_text(strip=True)
#        #print("titre : ", data_livre_titre, "\n")
#        
#        ### Auteur
#        try :
#            data_livre_auteur = data_livre_soup.find('span', attrs={"class" : "author author--main"}).get_text(strip=True)
#        except :
#            data_livre_auteur = data_livre_soup.find('a', attrs={"class" : "author author--main trackme"}).get_text(strip=True)
#        #print("auteur : ", data_livre_auteur, "\n")
#        
#        
#        ### prix grand format
#        data_livre_prix_gf = data_livre_soup.find('div', attrs={"class" : "price fp-wide--margin-bottom"}).find('span').get_text(strip=True)#.findAll('span', attrs={"class" : "final-price"})
#        #print("prix grand format : ", data_livre_prix_gf, "\n")
#        
#        ### prix ebook
#        try :
#            data_livre_prix_ebook = data_livre_soup.find('a', attrs={"class" : "ebook"}).get_text(strip=True)
#            #print("prix ebook : ", data_livre_prix_ebook, "\n")
#        except AttributeError:
#            #print("pas de prix ebook", "\n")
#            data_livre_prix_ebook = "pas de prix ebook"
#        
#        
#        ## Couverture
#        data_livre_couv = data_livre_soup.find('source', attrs={"class" : "lozad"})['data-srcset']
#        #print("couv", data_livre_couv, "\n")
#        
#        
#        ## Caractéristique
#        data_livre_carac = data_livre_soup.find('ul', attrs={"class" :"informations-container"}).get_text("|",strip=True)#.find_all('li',attrs={"class" :"information"}).get_text()
#        #print("caracteristiques : ", data_livre_carac.get_text(),"\n")
#        
#        
#        dic_rl_parus = {'url' : url_titre, #https://www.decitre.fr/livres/la-femme-a-la-valise-9782376650959.html
#            'categorie' : liste_cat_final,
#            'titre':data_livre_titre,
#            'auteur':data_livre_auteur,
#            'prix_gf':data_livre_prix_gf,
#            'prix_ebook':data_livre_prix_ebook,
#            #'caracteristiques_bis' : temp_dict,
#            'couverture':data_livre_couv,
#            'caracteristiques':data_livre_carac,
#            'RL' : 'RL',
#            'PREMIER_ROMAN' : premier_roman,
#            'TYPES' : types_livre,
#            'GENRE' : genre,
#            'PAYS' : pays,
#            'CONTINENT' : continent,
#            'Traduit de' : langue_traduction,
#            'Traduit par' : traducteurice,
#            }
#        
#        
#        ## Caractéristique
#        data_livre_carac_dict = data_livre_soup.find('ul', attrs={"class" :"informations-container"}).findAll('li', attrs={"class" : "information"})
#        for c in data_livre_carac_dict :
#            try :
#                k = c.find('span').get_text(strip=True)
#                v = c.find('div', attrs={"class" :"value"}).get_text(strip=True)
#            except AttributeError:
#                print("NC")
#            dic_rl_parus[k]=v
#        
#        liste_rl_titre.append(dic_rl_parus)
#    
#        df_rl_total_test = pd.concat([df_rl_total_test,pd.DataFrame(liste_rl_titre, index=[int(nb_index)])])


#with tab3 :
#    with st.form("ajout_manuel"):
#        nb_index = st.number_input('index')
#        prem_roman = st.selectbox('PREMIER ROMAN', ['OUI', 'NON'])
#        quel_genre = st.selectbox('genre', ['F', 'M'])
#        quel_pays = st.selectbox("Pays", list(df_rl_total_test['PAYS'].unique()))
#        quel_continent = st.selectbox("Continent", list(df_rl_total_test['CONTINENT'].unique()))
#        trad_de = st.selectbox("Traduit de", list(df_rl_total_test['Traduit de'].unique()))
#        trad_par = st.text_input('Traduit par')
#        ean = st.text_input('EAN')
#        titre = st.text_input('titre')
#        auteur = st.text_input('auteur')
#        date_parution = st.text_input('Date de parution')
#        mois= st.selectbox('MOIS', ['August', 'September','October'])
#        annee_parution = st.number_input('ANNEE_PUBLICATION')
#        url = st.text_input('url')
#        categorie = st.text_input('categorie-liste')
#        prix_gf = st.text_input('prix_gf')
#        prix_ebook = st.text_input('prix_ebook ou pas de prix ebook')
#        couverture= st.text_input('url couv ou pas de visuel')
#        editeur = st.text_input('Editeur')
#        isbn = st.text_input('ISBN')
#        format = st.selectbox('genre', ['Grand Format', 'Poche'])
#        presentation = st.text_input('Présentation')
#        nb_pages = st.text_input('nb pages')
#        poids = st.text_input('Poids')
#        dimension= st.text_input('Dimensions')
#        collection = st.text_input('Collection') 
#        st.form_submit_button('Submit my picks')
#
#    if quel_pays == None :
#        quel_pays = st.text_input("ajout pays")
#    
#    if trad_de == None :
#        trad_de = st.text_input("ajout langue")
#    
#    dict_manuel = {'RL' : ['RL'],
#                   'PREMIER_ROMAN' : [prem_roman], #PREMIER ROMAN NON
#                    'TYPES' : ['Romans étrangers'], #Essais Romans étrangers Romans français
#                    'GENRE' : [quel_genre],
#                    'PAYS' : [quel_pays],
#                    'CONTINENT' : [quel_continent],
#                    'Traduit de' : [trad_de],
#                    'Traduit par' : [trad_par],
#                    'EAN' : [ean],
#                    'titre' : [titre],
#                    'auteur' : [auteur],
#                    'Date de parution' : [date_parution],
#                    'MOIS' : [mois], #August September October
#                    'ANNEE_PUBLICATION' : [annee_parution],
#                    'url' : [url],
#                    'categorie' : [[categorie]],
#                    'prix_gf' : [prix_gf + ' €'],
#                    'prix_ebook' : [prix_ebook], #pas de prix ebook 15,99 €
#                    'couverture' : [couverture], #pas de visuel
#                    'caracteristiques' : ['Date de parution|'+date_parution+'|editeur|'+editeur+'|ISBN|'+isbn+'|EAN|'+ean+'|Format|'+format+'|Présentation|'+presentation+'|Nb. de pages|'+nb_pages+' pages|Poids|'+poids+' kg|Dimensions|'+dimension+'|Collection|'+collection],
#                    'Editeur' : [editeur],
#                    'ISBN' : [isbn],
#                    'Format' : [format], #Grand Format Poche
#                    'Présentation' : [presentation],
#                    'Nb. de pages' : [nb_pages+'pages'],
#                    'Poids' : [poids+'kg'],
#                    'Dimensions' : [dimension], #14cm x 22cm
#                    'Collection' : [collection]}
#    
#    df1 = pd.DataFrame(dict_manuel, index=[int(nb_index)])
#    
#    df_rl_total_test = pd.concat([df_rl_total_test, df1])

#st.dataframe(df_rl_total_test(int(nb_index)))

# export au format pickle
df_rl_total_test.to_pickle("./liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/

#df_rl_total_test = pd.read_pickle("liste_rl_total_test.pkl") #/content/drive/MyDrive/Data4Good/rentree_litteraire/2023/
#st.dataframe(df_rl_total_test.tail(2))


