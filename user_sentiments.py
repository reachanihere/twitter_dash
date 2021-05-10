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

    """Top users tweeted about  COVID-19 Vaccination"""
    bar_general = go.Figure()

    bar_general.add_trace(go.Bar(
        x=df_general_hashtag['username'],
        y=df_general_hashtag['Count'],
        marker_color='rgb(76, 76, 214)',
        opacity=0.8))
    bar_general.update_layout(title_text="The top users who tweeted about COVID-19 in General Dataset",
                              title_font_size=14)

    # Set x-axis title
    bar_general.update_xaxes(tickangle=45)
    bar_general.update_xaxes(title_text="User names")

    # Set y-axes titles
    bar_general.update_yaxes(title_text="Number of Tweets tweeted")


    """Top users tweeted about  COVID-19 Vaccination"""
    bar_vaccination = go.Figure()

    bar_vaccination.add_trace(go.Bar(
        x=df_vaccination_hashtag['username'],
        y=df_vaccination_hashtag['Count'],
        marker_color='rgb(93, 213, 93)',
        opacity=0.8))
    bar_vaccination.update_layout(title_text="The top users who tweeted about COVID-19 Vaccination in Dataset",
                                  title_font_size=14)

    # Set x-axis title
    bar_vaccination.update_xaxes(tickangle=45)
    bar_vaccination.update_xaxes(title_text="User names")

    # Set y-axes titles
    bar_vaccination.update_yaxes(title_text="Number of Tweets tweeted")



    """Top users tweeted about  COVID-19 Restriction"""
    bar_restriction = go.Figure()

    bar_restriction.add_trace(go.Bar(
        x=df_restriction_hashtag['username'],
        y=df_restriction_hashtag['Count'],
        marker_color='rgb(255, 92, 51)',
        opacity=0.8))
    bar_restriction.update_layout(title_text="The top users who tweeted about COVID-19 Restriction in Dataset",
                                  title_font_size=14)

    # Set x-axis title
    bar_restriction.update_xaxes(tickangle=45)
    bar_restriction.update_xaxes(title_text="User names")

    # Set y-axes titles
    bar_restriction.update_yaxes(title_text="Number of Tweets tweeted")





    user_general_json = json.dumps(bar_general, cls=plotly.utils.PlotlyJSONEncoder)
    user_vaccination_json = json.dumps(bar_vaccination, cls=plotly.utils.PlotlyJSONEncoder)
    user_restriction_json = json.dumps(bar_restriction, cls=plotly.utils.PlotlyJSONEncoder)

    return user_general_json, user_vaccination_json, user_restriction_json
