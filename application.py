from flask import Flask, render_template, request
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pandas as pd
import hashtag
from source import preprocessed_data, load_data, merge_data

application = Flask(__name__)

""" 
Data Imports for Covid Cases worldwide
"""

total_confirmed, total_death, total_recovered, df_pop = load_data()

(grouped_total_confirmed, grouped_total_recovered,
 grouped_total_death, timeseries_final, country_names) = preprocessed_data(total_confirmed, total_death,
                                                                           total_recovered)

final_df = merge_data(grouped_total_confirmed, grouped_total_recovered, grouped_total_death, df_pop)

df_general = pd.read_csv('https://raw.githubusercontent.com/FabioPalliparambil98/covid-dataset/main/combined_generaltweets.csv')

"""
It displays the Home Pages of the Visualisations.
"""


@application.route('/')
def homepage():
    sentiment_general = "positive"
    sentiment_vaccination = "positive"
    sentiment_restriction = "positive"

    plot_general, plot_restriction, plot_vaccination = hashtag.create_plot(hashtag.df_general_hash_tag,
                                                                           hashtag.df_restriction_hash_tag,
                                                                           hashtag.df_vaccination_hash_tag)

    return render_template("index.html",
                           sentiment_general=sentiment_general,
                           sentiment_vaccination=sentiment_vaccination,
                           sentiment_restriction=sentiment_restriction,
                           plot_general=plot_general,
                           plot_restriction=plot_restriction,
                           plot_vaccination=plot_vaccination)


"""
It displays the analysis of live tweets.
"""


@application.route('/live_tweets')
def live_tweets():
    return render_template("live_tweets.html")


"""
It displays the analysis of live tweets.
"""


@application.route('/contact', methods=["GET", "POST"])
def contact_page():
    if request.method == "GET":

        return render_template('contact.html')

    elif request.method == "POST":

        name = request.form["txtName"]
        email = request.form["txtEmail"]
        phone = request.form["txtPhone"]
        message = request.form["txtMsg"]
        print(name, email, phone, message)

        return render_template('test.html')


"""
It displays the analysis of live tweets.
"""


@application.route('/covidcases')
def covidcases():
    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()

    df = final_df
    df.index = df['Country/Region']
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["confirmed"],
            name="# of confirmed cases",
            marker_color='#39ac39',
            opacity=1
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["cases/million"],
            mode="lines",
            name="cases/million",
            marker_color='#b23434',
            opacity=0.7
        ),
        secondary_y=True
    )

    # Add figure title
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=0.93),
        title={
            'text': '<span style="font-size: 20px;">Global aggregate cases</span><br><span style="font-size: 10px;">(click and drag)</span>',
            'y': 0.97,
            'x': 0.45,
            'xanchor': 'center',
            'yanchor': 'top'},
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        width=1500, height=700
    )

    # Set x-axis title
    fig.update_xaxes(tickangle=45)

    # Set y-axes titles
    fig.update_yaxes(title_text="# of confirmed cases",
                     secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="cases/millions", tickangle=45,
                     secondary_y=True, showgrid=False)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plot_global_cases_per_country = plot_json

    context = {'plot_global_cases_per_country': plot_global_cases_per_country}
    return render_template('covidcases.html', context=context, total_all_confirmed=total_all_confirmed,
                           total_all_recovered=total_all_recovered,
                           total_all_deaths=total_all_deaths)


if __name__ == '__main__':
    application.run()
