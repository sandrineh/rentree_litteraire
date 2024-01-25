# test.py
# 1.Importation des librairies nécessaires pour le script

import os
import time
import re

#scraping
from urllib.request import Request, urlopen
#from bs4 import BeautifulSoup
#import scrapy
import requests

import json
#from pandas.io.json import json_normalize

import pandas as pd
import numpy as np
import datetime as dt  #pour l'ajout de la date de l'extraction de données
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

#Datavisualisation
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt

#Web application
import streamlit as st
from streamlit_option_menu import option_menu

#from geopy.geocoders import Nominatim

#Export fichier
import pickle

#Text Analysis
from wordcloud import WordCloud
#from textblob import TextBlob
#import spacy

from PIL import Image
#from collections import defaultdict
#from collections import Counter
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.decomposition import LatentDirichletAllocation


#from spacy.lang.fr.examples import sentences 
#
#nlp = spacy.load("fr_core_news_sm")
#doc = nlp(sentences[0])
#print(doc.text)
#for token in doc:
#    st.write(token.text, token.pos_, token.dep_)


# Create and generate a word cloud image:
def create_wordcloud(topic):
	mask = np.array(Image.open("docs/cloud.png"))
	mask[mask == 1] = 255
	
	exclure_mots = ['d', 'du', 'de', 'la', 'des', 'le', 'et', 'est', 'elle', 'une', 'en', 'que', 'aux', 'qui', 'ces', 'les', 'dans', 'sur', 'l', 'un', 'pour', 'par', 'il', 'ou', 'à', 'ce', 'a', 'sont', 'cas', 'plus', 'leur', 'se', 's', 'vous', 'au', 'c', 'aussi', 'toutes', 'autre', 'comme']
	wordcloud = WordCloud(background_color = 'white', stopwords = exclure_mots, max_words = 50, mask = mask).generate(topic)
	
	return wordcloud



#sys.path.append("pages")
#from dataframes import displayText, displayTable
#displayText()
#displayTable()
#


#https://learningtofly.dev/blog/streamlit-class-based-app




