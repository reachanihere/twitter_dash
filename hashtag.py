import json
import nltk
import pandas as pd
import plotly.graph_objects as go
import plotly
import re

df_general = pd.read_csv(
    'https://raw.githubusercontent.com/FabioPalliparambil98/covid-dataset/main/combined_generaltweets.csv')
df_restriction = pd.read_csv(
    'https://raw.githubusercontent.com/FabioPalliparambil98/covid-dataset/main/combined_restrictiontweets.csv')
df_vaccination = pd.read_csv(
    'https://raw.githubusercontent.com/FabioPalliparambil98/covid-dataset/main/combined_vaccinationtweets.csv')

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


def hashtag(df_general, df_restriction, df_vaccination):

    HT_general = collectHashtag(df_general['text'])
    HT_general = sum(HT_general, [])
    general_tag = nltk.FreqDist(HT_general)
    hashtag_general = pd.DataFrame({'Hashtag': list(general_tag.keys()), 'Count': list(general_tag.values())})
    hashtag_general = hashtag_general.nlargest(columns='Count', n=10)

    HT_restriction = collectHashtag(df_restriction['text'])
    HT_restriction = sum(HT_restriction, [])
    restriction_tag = nltk.FreqDist(HT_restriction)
    hashtag_restriction = pd.DataFrame(
        {'Hashtag': list(restriction_tag.keys()), 'Count': list(restriction_tag.values())})
    hashtag_restriction = hashtag_restriction.nlargest(columns='Count', n=10)

    HT_vaccination = collectHashtag(df_vaccination['text'])
    HT_vaccination = sum(HT_vaccination, [])
    vaccination_tag = nltk.FreqDist(HT_vaccination)
    hashtag_vaccination = pd.DataFrame(
        {'Hashtag': list(vaccination_tag.keys()), 'Count': list(vaccination_tag.values())})
    hashtag_vaccination = hashtag_vaccination.nlargest(columns='Count', n=10)

    return hashtag_general, hashtag_restriction, hashtag_vaccination


df_general_hash_tag, df_restriction_hash_tag, df_vaccination_hash_tag = hashtag(df_general, df_restriction,
                                                                                df_vaccination)


def create_plot(df_general_hashtag, df_restriction_hashtag, df_vaccination_hashtag):


    scatter_general = [go.Bar(
        x=df_general_hashtag['Hashtag'],
        y=df_general_hashtag['Count'],
        marker_color='lightsalmon',
        text=df_general_hashtag['Count'],
        textposition='auto'
    )
    ]
    graph_general = go.Figure(scatter_general)
    graph_general.update_layout(
        title='General Frequency Tweet Count',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Word Frequency Count',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        xaxis_tickangle=-45,
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    scatter_restriction = [go.Bar(
        x=df_restriction_hashtag['Hashtag'],
        y=df_restriction_hashtag['Count'],
        marker_color='lightsalmon',
        text=df_restriction_hashtag['Count'],
        textposition='auto'
    )
    ]
    graph_restriction = go.Figure(scatter_restriction)
    graph_restriction.update_layout(
        title='restriction Frequency Tweet Count',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Word Frequency Count',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        xaxis_tickangle=-45,
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    scatter_vaccination = [go.Bar(
        x=df_vaccination_hashtag['Hashtag'],
        y=df_vaccination_hashtag['Count'],
        marker_color='lightsalmon',
        text=df_vaccination_hashtag['Count'],
        textposition='auto'
    )
    ]
    graph_vaccination = go.Figure(scatter_vaccination)
    graph_vaccination.update_layout(
        title='General Frequency Tweet Count',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Word Frequency Count',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        xaxis_tickangle=-45,
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    general_JSON = json.dumps(scatter_general, cls=plotly.utils.PlotlyJSONEncoder)
    restriction_JSON = json.dumps(scatter_restriction, cls=plotly.utils.PlotlyJSONEncoder)
    vaccination_JSON = json.dumps(scatter_vaccination, cls=plotly.utils.PlotlyJSONEncoder)

    return general_JSON, restriction_JSON, vaccination_JSON

