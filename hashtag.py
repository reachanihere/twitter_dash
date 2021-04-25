import json
import nltk
import pandas as pd
import plotly.graph_objects as go
import plotly
import re


df_general = pd.read_csv('https://raw.githubusercontent.com/FabioPalliparambil98/covid-dataset/main/combined_generaltweets.csv')



"""
Function for collecting all the Hashtag
"""


def collectHashtag(x):
    hashtags = []
    for i in x:
        ht = re.findall(r"#(\w+)", i)
        hashtags.append(ht)
    return hashtags


"""
Function for collecting hashed into multiple dataframe
"""

def hashtag(df_general):

    HT_general = collectHashtag(df_general['text'])
    HT_general = sum(HT_general,[])
    general_tag = nltk.FreqDist(HT_general)
    hashtag_general = pd.DataFrame({'Hashtag':list(general_tag.keys()),'Count':list(general_tag.values())})
    hashtag_general = hashtag_general.nlargest(columns='Count', n=10)

    return hashtag_general


def create_plot(df_general_hashtag):

    # Create a trace
    scatter_general = [go.Scatter(
        x=df_general_hashtag['Hashtag'],
        y=df_general_hashtag['Count'],
        mode='lines+markers',
        name='lines+markers',
        marker_color = 'rgba(255, 182, 193, .9)'
        # mode='markers'
    )]

    general_JSON = json.dumps(scatter_general, cls=plotly.utils.PlotlyJSONEncoder)

    return general_JSON


df_hash_tag = hashtag(df_general)