from flask import Flask, render_template, request
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pandas as pd
import hashtag


application = Flask(__name__)


df_general = pd.read_csv('https://raw.githubusercontent.com/FabioPalliparambil98/covid-dataset/main/combined_generaltweets.csv')



"""
It displays the Home Pages of the Visualisations.
"""


@application.route('/')
def homepage():
    sentiment_general = "positive"
    sentiment_vaccination = "positive"
    sentiment_restriction = "positive"
    plot_general = hashtag.create_plot(hashtag.df_hash_tag)

    return render_template("index.html",
                           sentiment_general=sentiment_general,
                           sentiment_vaccination=sentiment_vaccination,
                           sentiment_restriction=sentiment_restriction,
                           plot_general=plot_general)




if __name__ == '__main__':
    application.run()
