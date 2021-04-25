from flask import Flask, render_template, request
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pandas as pd
import hashtag

application = Flask(__name__)

df_general = pd.read_csv(
    'https://raw.githubusercontent.com/FabioPalliparambil98/covid-dataset/main/combined_generaltweets.csv')

"""
It displays the Home Pages of the Visualisations.
"""


@application.route('/')
def homepage():
    sentiment_general = "positive"
    sentiment_vaccination = "positive"
    sentiment_restriction = "positive"

    plot_general, plot_restriction, plot_vaccination, scatter_general, scatter_restriction, scatter_vaccination, \
    all, actual_scatter, pie = hashtag.create_plot(hashtag.covid_general_hashtag,
                                                   hashtag.covid_restriction_hashtag,
                                                   hashtag.covid_vaccination_hashtag)

    return render_template("index.html",
                           plot1=plot_general,
                           plot2=plot_vaccination,
                           plot3=plot_restriction,
                           scatter1=scatter_general,
                           scatter2=scatter_restriction,
                           scatter3=scatter_vaccination,
                           all=all,
                           sentiment_general=sentiment_general,
                           sentiment_vaccination=sentiment_vaccination,
                           sentiment_restriction=sentiment_restriction,
                           actual_scatter=actual_scatter,
                           pie=pie)


if __name__ == '__main__':
    application.run()
