import re
import json
import string
import nltk
import pandas as pd
import plotly.graph_objects as go
import plotly


def user_collection(x):
    hashtags = []
    for i in x:
        ht = re.findall(r"(\w+)", i)
        hashtags.append(ht)
    return hashtags


def userdataframe(df):

    HT_general = user_collection(df['username'])
    HT_general = sum(HT_general, [])
    general_tag = nltk.FreqDist(HT_general)
    hashtag_general = pd.DataFrame({'username': list(general_tag.keys()), 'Count': list(general_tag.values())})
    hashtag_general['username'] = hashtag_general['username'].drop_duplicates()
    hashtag_general = hashtag_general.dropna()
    hashtag_general = hashtag_general.nlargest(columns='Count', n=15)
    return hashtag_general


def users_plot(df_general_hashtag, df_vaccination_hashtag, df_restriction_hashtag):

    bar_general = [go.Bar(
        x=df_general_hashtag['username'],
        y=df_general_hashtag['Count'],
        marker_color='lightsalmon',
        text=df_general_hashtag['Count'],
        textposition='auto'
    )
    ]
    graph_general = go.Figure(bar_general)
    graph_general.update_layout(
        title_text='January 2013 Sales Report',
        # title='General Frequency Tweet Count',
        # xaxis_tickfont_size=14,
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
    # graph_general.update_layout(
    #     title_text='January 2013 Sales Report'
    # )

    bar_vaccination = [go.Bar(
        x=df_vaccination_hashtag['username'],
        y=df_vaccination_hashtag['Count'],
        marker_color='lightsalmon',
        text=df_vaccination_hashtag['Count'],
        textposition='auto'
    )
    ]
    graph_vaccination = go.Figure(bar_vaccination)
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

    bar_restriction = [go.Bar(
        x=df_restriction_hashtag['username'],
        y=df_restriction_hashtag['Count'],
        marker_color='lightsalmon',
        text=df_restriction_hashtag['Count'],
        textposition='auto'
    )
    ]
    graph_restriction = go.Figure(bar_restriction)
    graph_restriction.update_layout(
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


    user_general_json = json.dumps(bar_general, cls=plotly.utils.PlotlyJSONEncoder)
    user_vaccination_json = json.dumps(bar_vaccination, cls=plotly.utils.PlotlyJSONEncoder)
    user_restriction_json = json.dumps(bar_restriction, cls=plotly.utils.PlotlyJSONEncoder)

    return user_general_json, user_vaccination_json, user_restriction_json
