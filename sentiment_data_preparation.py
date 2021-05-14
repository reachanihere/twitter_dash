import json
import string
from sre_parse import Tokenizer

import nltk
import pandas as pd
import numpy as np
import emojis
import dash
from nltk.corpus import stopwords

from nltk import *
# from keras.preprocessing.text import Tokenizer
import plotly.graph_objects as go
import plotly
# import tensorflow as tf
# from sklearn.feature_extraction.text import CountVectorizer

wn = nltk.WordNetLemmatizer()
ps = nltk.PorterStemmer()

df_general = pd.read_csv(r"static\dataset\combined_generaltweets.csv")
df_restriction = pd.read_csv(r"static\dataset\combined_restrictiontweets.csv")
df_vaccination = pd.read_csv(r"static\dataset\combined_vaccinationtweets.csv")

df_general['tweetcreatedts'] = pd.to_datetime(df_general['tweetcreatedts'])
df_restriction['tweetcreatedts'] = pd.to_datetime(df_restriction['tweetcreatedts'])
df_vaccination['tweetcreatedts'] = pd.to_datetime(df_vaccination['tweetcreatedts'])

df_general = df_general.dropna()
df_restriction = df_restriction.dropna()
df_vaccination = df_vaccination.dropna()

df_general = df_general.drop_duplicates()
df_restriction = df_restriction.drop_duplicates()
df_vaccination = df_vaccination.drop_duplicates()

# df_general = df_general.reset_index(drop=True, inplace=True)
# df_restriction = df_restriction.reset_index(drop=True, inplace=True)
# df_vaccination = df_vaccination.reset_index(drop=True, inplace=True)
"""
Function For Tweet Cleaning.
"""


def clean_data(text):
    text = "".join([char for char in text if char not in string.punctuation])
    # text = re.sub('[0-9]+', '', text)
    text = re.sub(r'^RT[\s]+', '', text)
    text = emojis.decode(text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'_', '', text)
    text = re.sub(r'[0-9]', '', text)
    text = re.sub('@[^\s]+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = text.lower()
    return text


"""
General COVID-19
"""
df_general['Month'] = df_general.tweetcreatedts.dt.month
df_general['Hour'] = df_general.tweetcreatedts.dt.hour
df_general['day_in_week'] = df_general.tweetcreatedts.dt.weekday
df_general['day'] = df_general.tweetcreatedts.dt.day

df_general['day_in_week'].replace(0, 'Monday', inplace=True)
df_general['day_in_week'].replace(1, 'Tuesday', inplace=True)
df_general['day_in_week'].replace(2, 'Wednesday', inplace=True)
df_general['day_in_week'].replace(3, 'Thursday', inplace=True)
df_general['day_in_week'].replace(4, 'Friday', inplace=True)
df_general['day_in_week'].replace(5, 'Saturday', inplace=True)
df_general['day_in_week'].replace(6, 'Sunday', inplace=True)

df_general['text'] = df_general['text'].apply(lambda x: clean_data(x))
df_general['location'] = df_general['location'].apply(lambda x: clean_data(x))
df_general['text'] = df_general['text'].apply(lambda x: wn.lemmatize(x))
df_general['text'] = df_general['text'].apply(lambda x: ps.stem(x))

"""
Restriction
"""

df_restriction['Month'] = df_restriction.tweetcreatedts.dt.month
df_restriction['Hour'] = df_restriction.tweetcreatedts.dt.hour
df_restriction['day_in_week'] = df_restriction.tweetcreatedts.dt.weekday
df_restriction['day'] = df_restriction.tweetcreatedts.dt.day

df_restriction['day_in_week'].replace(0, 'Monday', inplace=True)
df_restriction['day_in_week'].replace(1, 'Tuesday', inplace=True)
df_restriction['day_in_week'].replace(2, 'Wednesday', inplace=True)
df_restriction['day_in_week'].replace(3, 'Thursday', inplace=True)
df_restriction['day_in_week'].replace(4, 'Friday', inplace=True)
df_restriction['day_in_week'].replace(5, 'Saturday', inplace=True)
df_restriction['day_in_week'].replace(6, 'Sunday', inplace=True)

df_restriction['text'] = df_restriction['text'].apply(lambda x: clean_data(x))
df_restriction['location'] = df_restriction['location'].apply(lambda x: clean_data(x))
df_restriction['text'] = df_restriction['text'].apply(lambda x: wn.lemmatize(x))
df_restriction['text'] = df_restriction['text'].apply(lambda x: ps.stem(x))

"""
Vaccination
"""
df_vaccination['Month'] = df_vaccination.tweetcreatedts.dt.month
df_vaccination['Hour'] = df_vaccination.tweetcreatedts.dt.hour
df_vaccination['day_in_week'] = df_vaccination.tweetcreatedts.dt.weekday
df_vaccination['day'] = df_vaccination.tweetcreatedts.dt.day

df_vaccination['day_in_week'].replace(0, 'Monday', inplace=True)
df_vaccination['day_in_week'].replace(1, 'Tuesday', inplace=True)
df_vaccination['day_in_week'].replace(2, 'Wednesday', inplace=True)
df_vaccination['day_in_week'].replace(3, 'Thursday', inplace=True)
df_vaccination['day_in_week'].replace(4, 'Friday', inplace=True)
df_vaccination['day_in_week'].replace(5, 'Saturday', inplace=True)
df_vaccination['day_in_week'].replace(6, 'Sunday', inplace=True)

df_vaccination['text'] = df_vaccination['text'].apply(lambda x: clean_data(x))
df_vaccination['location'] = df_vaccination['location'].apply(lambda x: clean_data(x))
df_vaccination['text'] = df_vaccination['text'].apply(lambda x: wn.lemmatize(x))
df_vaccination['text'] = df_vaccination['text'].apply(lambda x: ps.stem(x))


"""
Sentiment Analysis Model Preprocessing
"""
# max_fatures = 2000
# tokenizer = Tokenizer(num_words=max_fatures, split=' ')
# tokenizer.fit_on_texts(df_general['text'].values)
# X = tokenizer.texts_to_sequences(df_general['text'].values)
