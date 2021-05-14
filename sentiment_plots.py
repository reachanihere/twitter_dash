import re
import nltk
import plotly.graph_objects as go
import json
import plotly
import pandas as pd


def sentiment_collection(x):
    hashtags = []
    for i in x:
        ht = re.findall(r"(\w+)", i)
        hashtags.append(ht)
    return hashtags


def sentiment_dataframe(df):
    HT_general = sentiment_collection(df['sentiment'])
    HT_general = sum(HT_general, [])
    general_tag = nltk.FreqDist(HT_general)
    hashtag_general = pd.DataFrame({'sentiment': list(general_tag.keys()), 'Count': list(general_tag.values())})
    hashtag_general['sentiment'] = hashtag_general['sentiment'].drop_duplicates()
    hashtag_general = hashtag_general.dropna()
    hashtag_general = hashtag_general.nlargest(columns='Count', n=15)
    return hashtag_general


"""
Create a Sentiment analysis and display the ration of negative and positive tweets in a pie Chart. 
The graphs data is returned in the form of json .But this function is for a multiple dataset.
"""


def sentiment_pie(df_general, df_vaccination, df_restriction):
    Pie_general = go.Figure()
    Pie_general.add_trace(go.Pie(labels=df_general['sentiment'],
                                 values=df_general['Count'],
                                 hole=.2))

    Pie_general.update_layout(title_text="Sentiment on general data", title_font_size=20)

    Pie_general.update_traces(textposition='inside', textinfo='percent+label')

    Pie_vaccination = go.Figure()
    Pie_vaccination.add_trace(go.Pie(labels=df_vaccination['sentiment'],
                                     values=df_vaccination['Count'],
                                     hole=.2))

    Pie_vaccination.update_layout(title_text="Sentiment on vaccination data", title_font_size=20)
    Pie_vaccination.update_traces(textposition='inside', textinfo='percent+label')

    Pie_restriction = go.Figure()
    Pie_restriction.add_trace(go.Pie(labels=df_restriction['sentiment'],
                                     values=df_restriction['Count'],
                                     hole=.2))

    Pie_restriction.update_layout(title_text="Sentiment on restriction data", title_font_size=20)
    Pie_restriction.update_traces(textposition='inside', textinfo='percent+label')

    pie_general_JSON = json.dumps(Pie_general, cls=plotly.utils.PlotlyJSONEncoder)
    pie_vaccination_JSON = json.dumps(Pie_vaccination, cls=plotly.utils.PlotlyJSONEncoder)
    Pie_restriction_JSON = json.dumps(Pie_restriction, cls=plotly.utils.PlotlyJSONEncoder)

    return pie_general_JSON, pie_vaccination_JSON, Pie_restriction_JSON


"""
Create a Sentiment analysis and display the ration of negative and positive tweets in a pie Chart. 
The graphs data is returned in the form of json .But this function is for a single dataset.
"""


def single_sentiment_pie(df_general):
    Pie_general = go.Figure()
    Pie_general.add_trace(go.Pie(labels=df_general['sentiment'],
                                 values=df_general['Count'],
                                 hole=.2))

    Pie_general.update_layout(title_text="Sentiment on the tweets collected", title_font_size=20)

    pie_general_JSON = json.dumps(Pie_general, cls=plotly.utils.PlotlyJSONEncoder)

    return pie_general_JSON
