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


"""
Function for plotting the plot according to the dataframe created for Hashtag
"""


def create_plot(df_general_hashtag, hashtag_restriction, hashtag_vaccination):
    bar_general = [go.Bar(
        x=df_general_hashtag['Hashtag'],
        y=df_general_hashtag['Count'],
        marker_color='lightsalmon',
        text=df_general_hashtag['Count'],
        textposition='auto'
    )
    ]
    graph_general = go.Figure(bar_general)
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

    bar_restriction = [go.Bar(
        x=hashtag_restriction['Hashtag'],
        y=hashtag_restriction['Count'],
        marker_color='lightsalmon',
        text=hashtag_restriction['Count'],
        textposition='auto'
    )
    ]
    graph_restriction = go.Figure(bar_restriction)
    graph_restriction.update_layout(
        title='Restriction Frequency Tweet Count',
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

    bar_vaccination = [go.Bar(
        x=hashtag_vaccination['Hashtag'],
        y=hashtag_vaccination['Count'],
        marker_color='lightsalmon',
        text=hashtag_vaccination['Count'],
        textposition='auto'
    )
    ]
    graph_vaccination = go.Figure(bar_vaccination)
    graph_vaccination.update_layout(
        title='Vaccination Frequency Tweet Count',
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

    """ Scatter """

    # Create a trace
    scatter_general = [go.Scatter(
        x=df_general_hashtag['Hashtag'],
        y=df_general_hashtag['Count'],
        mode='lines+markers',
        name='lines+markers',
        marker_color='rgba(255, 182, 193, .9)'
        # mode='markers'
    )]

    """ Scatter """

    # Create a trace
    scatter_restriction = [go.Scatter(
        x=hashtag_restriction['Hashtag'],
        y=hashtag_restriction['Count'],
        mode='lines+markers',
        name='lines+markers',
        marker_color='rgba(255, 182, 193, .9)'
        # mode='markers'
    )]

    """ Scatter """

    # Create a trace
    scatter__vaccination = [go.Scatter(
        x=hashtag_vaccination['Hashtag'],
        y=hashtag_vaccination['Count'],
        mode='lines+markers',
        name='lines+markers',
        marker_color='rgba(255, 182, 193, .9)'
        # mode='markers'
    )]

    """ all toghether"""
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_general_hashtag['Hashtag'],
            y=df_general_hashtag['Count'],
            name='COVID-19 General Hashtag'
        ))

    fig.add_trace(
        go.Bar(
            x=hashtag_restriction['Hashtag'],
            y=hashtag_restriction['Count'],
            name='COVID-19 Restriction Hashtag'
        ))
    fig.add_trace(
        go.Bar(
            x=hashtag_vaccination['Hashtag'],
            y=hashtag_vaccination['Count'],
            name='COVID-19 Vaccination Hashtag'
        ))

    Scatter = go.Figure(data=go.Scatter(
        x=df_general_hashtag['Hashtag'],
        y=df_general_hashtag['Count'],
        mode='markers',
        marker=dict(size=[40, 40, 40, 40, 40, 40, 40, 40, 40, 40],
                    color=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ))

    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

    Pie = go.Figure(data=[go.Pie(labels=hashtag_vaccination['Hashtag'],
                                 values=hashtag_vaccination['Count'],
                                 textinfo='label+percent',
                                 insidetextorientation='radial',
                                 hole=.2)])

    general_JSON = json.dumps(graph_general, cls=plotly.utils.PlotlyJSONEncoder)
    restriction_JSON = json.dumps(graph_restriction, cls=plotly.utils.PlotlyJSONEncoder)
    vaccination_JSON = json.dumps(graph_vaccination, cls=plotly.utils.PlotlyJSONEncoder)
    scatter_general_graphJSON = json.dumps(scatter_general, cls=plotly.utils.PlotlyJSONEncoder)
    scatter_restriction_graphJSON = json.dumps(scatter_restriction, cls=plotly.utils.PlotlyJSONEncoder)
    scatter_vaccination_graphJSON = json.dumps(scatter__vaccination, cls=plotly.utils.PlotlyJSONEncoder)
    scatter_graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    actual_scatter = json.dumps(Scatter, cls=plotly.utils.PlotlyJSONEncoder)
    Pie_json = json.dumps(Pie, cls=plotly.utils.PlotlyJSONEncoder)

    return general_JSON, restriction_JSON, vaccination_JSON, scatter_general_graphJSON, scatter_restriction_graphJSON, scatter_vaccination_graphJSON, scatter_graphJSON, actual_scatter, Pie_json


# calling a function called hashtag from hashtag.py
covid_general_hashtag, covid_restriction_hashtag, covid_vaccination_hashtag = hashtag(df_general,
                                                                                      df_restriction,
                                                                                      df_vaccination)
