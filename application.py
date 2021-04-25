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



"""
It displays the Home Pages of the Visualisations.
"""


@application.route('/')
def homepage():
    sentiment_general = "positive"
    sentiment_vaccination = "positive"
    sentiment_restriction = "positive"

    return render_template("index.html",sentiment_general=sentiment_general,sentiment_vaccination=sentiment_vaccination,sentiment_restriction=sentiment_restriction)



if __name__ == '__main__':
    application.run()
