from flask import Flask, render_template, request
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pandas as pd
from source import *
from flask_mail import Mail
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
    plot_general = create_plot(df_general)

    return render_template("index.html",sentiment_general=sentiment_general,
                           sentiment_vaccination=sentiment_vaccination,
                           sentiment_restriction=sentiment_restriction,
                           plot_general=plot_general)


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


def create_plot(df_general_hashtag, hashtag_restriction, hashtag_vaccination):

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

    return(general_JSON)
    



if __name__ == '__main__':
    application.run()
