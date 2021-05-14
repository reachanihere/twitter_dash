from flask import Flask, render_template, request
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pandas as pd
import hashtag
import live_tweets_graphs
# from word_cloud import *
import user_sentiments
import page_with_filter
from covid_cases_datapoint import cleaning_data, loading_data, combining_data
import sentiment_plots

application = Flask(__name__)

df_general_filter = pd.read_csv(
    'https://raw.githubusercontent.com/FabioPalliparambil98/cleaned-covid-dataset/main/general_covid.csv')
df_restriction_filter = pd.read_csv(
    'https://raw.githubusercontent.com/FabioPalliparambil98/cleaned-covid-dataset/main/covid_restriction.csv')
df_vaccination_filter = pd.read_csv(
    'https://raw.githubusercontent.com/FabioPalliparambil98/cleaned-covid-dataset/main/covid_vaccination.csv')

df_general_filter_sentiment = df_general_filter.copy()
df_restriction_filter_sentiment = df_restriction_filter.copy()
df_vaccination_filter_sentiment = df_vaccination_filter.copy()

df_general_filter['sentiment'].replace(0, 'negative', inplace=True)
df_general_filter['sentiment'].replace(1, 'positive', inplace=True)

df_restriction_filter['sentiment'].replace(0, 'negative', inplace=True)
df_restriction_filter['sentiment'].replace(1, 'positive', inplace=True)

df_vaccination_filter['sentiment'].replace(0, 'negative', inplace=True)
df_vaccination_filter['sentiment'].replace(1, 'positive', inplace=True)

df_general_filter["tweetcreatedts"] = pd.to_datetime(df_general_filter["tweetcreatedts"], format='%Y/%m/%d %H:%M:%S')
df_general_filter = df_general_filter.sort_values(by="tweetcreatedts")

""" 
Data Imports for Covid Cases worldwide
"""

total_confirmed, total_death, total_recovered, df_pop = loading_data()

(grouped_total_confirmed, grouped_total_recovered,
 grouped_total_death, timeseries_final, country_names) = cleaning_data(total_confirmed, total_death,
                                                                       total_recovered)

df_covid_cases_data = combining_data(grouped_total_confirmed, grouped_total_recovered, grouped_total_death, df_pop)

"""
The is a function used to create visualisation for the home page of the web application.The @application.route is used 
to get the users input on the web and to run the fuction according to users selection.
"""


@application.route('/', methods=["GET", "POST"])
def homepage():
    # Combining multiple datasets together.
    union_cleaned_df = pd.concat([df_general_filter,
                                  df_restriction_filter,
                                  df_vaccination_filter
                                  ])
    # Retrieving the unique values in the day_in_week feature.
    days_in_weeks = union_cleaned_df['day_in_week'].unique()
    days_in_weeks.sort()

    # If the request from html is GET then run the code.
    if request.method == "GET":

        # Getting the sentiment on the whole datasets.
        sentiment_general = sentiment_data(df_general_filter_sentiment)
        sentiment_vaccination = sentiment_data(df_restriction_filter_sentiment)
        sentiment_restriction = sentiment_data(df_vaccination_filter_sentiment)

        # Creating plots using hashtags.
        line_general, line_restriction, line_vaccination, all_line_scatters, scatter_circles, pie_general = hashtag.create_plot(
            hashtag.df_general_hash_tag,
            hashtag.df_restriction_hash_tag,
            hashtag.df_vaccination_hash_tag)

        # Creating a table by combining multiple datasets together.
        table = create_table(union_cleaned_df)

        # User Sentiment Graphs
        df_users_general = user_sentiments.userdataframe(df_general_filter)
        df_users_vaccination = user_sentiments.userdataframe(df_vaccination_filter)
        df_users_restriction = user_sentiments.userdataframe(df_restriction_filter)

        # Calling a function created in user_sentiments.py to create graph with users and the high no of tweets.
        user_general, user_vaccination, user_restriction = user_sentiments.users_plot(df_users_general,
                                                                                      df_users_vaccination,
                                                                                      df_users_restriction)
        # This is Dictionaries created to pass in the values to index.HTML
        plots = {'line_general': line_general,
                 'line_restriction': line_restriction,
                 'line_vaccination': line_vaccination,
                 'all_line_scatters': all_line_scatters,
                 'scatter_circles': scatter_circles,
                 'pie_general': pie_general,
                 'user_general': user_general,
                 'user_vaccination': user_vaccination,
                 'user_restriction': user_restriction,
                 'table': table}

        # Creating a dataframe with unique sentiment and their count.
        df_general_sentiment = sentiment_plots.sentiment_dataframe(df_general_filter)
        df_restriction_sentiment = sentiment_plots.sentiment_dataframe(df_restriction_filter)
        df_vaccination_sentiment = sentiment_plots.sentiment_dataframe(df_vaccination_filter)

        # Calling a function in sentiment_plots.py to create the pie graph for sentiment of the people.
        pie_general_sentiment, pie_vaccination_sentiment, pie_restriction_sentiment = sentiment_plots.sentiment_pie(
            df_general_sentiment,
            df_vaccination_sentiment,
            df_restriction_sentiment)

        # This is Dictionaries created to pass in the values to index.HTML
        sentiment_pie = {'pie_general_sentiment': pie_general_sentiment,
                         'pie_vaccination_sentiment': pie_vaccination_sentiment,
                         'pie_restriction_sentiment': pie_restriction_sentiment}

        # rendering the index.html template and passing in all the graphs create.
        return render_template("index.html",
                               sentiment_general=sentiment_general,
                               sentiment_vaccination=sentiment_vaccination,
                               sentiment_restriction=sentiment_restriction,
                               plots=plots,
                               days_in_weeks=days_in_weeks,
                               sentiment_pie=sentiment_pie)
    else:
        # If the requested method  by index.HTML is POST run the following code.

        # Collect the value entered by the user in the form.
        day = request.form["day"]

        # Select the datasets according to the input of the user.
        df_general_sentiment = df_general_filter_sentiment[df_general_filter_sentiment['day_in_week'] == day]
        df_vaccination_sentiment = df_vaccination_filter_sentiment[
            df_vaccination_filter_sentiment['day_in_week'] == day]
        df_restriction_sentiment = df_restriction_filter_sentiment[
            df_restriction_filter_sentiment['day_in_week'] == day]

        # getting the Sentiment according to the filtered dataset according to users input..
        sentiment_general = sentiment_data(df_general_sentiment)
        sentiment_vaccination = sentiment_data(df_vaccination_sentiment)
        sentiment_restriction = sentiment_data(df_restriction_sentiment)

        # Collecting data from hashtag.py and assigning to a variable.
        general_hashtag = hashtag.df_general
        vaccination_hashtag = hashtag.df_vaccination
        restriction_hashtag = hashtag.df_restriction

        # filtering the datasets according to the input of the user.
        hashtag_general_df = general_hashtag[general_hashtag['day_in_week'] == day]
        hashtag_vaccination_df = vaccination_hashtag[vaccination_hashtag['day_in_week'] == day]
        hashtag_restriction_df = restriction_hashtag[restriction_hashtag['day_in_week'] == day]

        df_general_hash_tag = hashtag.hastag_dataframe(hashtag_general_df)
        df_restriction_hash_tag = hashtag.hastag_dataframe(hashtag_restriction_df)
        df_vaccination_hash_tag = hashtag.hastag_dataframe(hashtag_vaccination_df)

        # Plotting all the necessary plots according to users input
        line_general, line_restriction, line_vaccination, all_line_scatters, scatter_circles, pie_general = hashtag.create_plot(
            df_general_hash_tag,
            df_restriction_hash_tag,
            df_vaccination_hash_tag)

        # calling a function to create a table with all the feature using plotly.
        table = create_table(union_cleaned_df[union_cleaned_df['day_in_week'] == day])

        # User Sentiment Graphs.
        df_users_general = user_sentiments.userdataframe(df_general_filter[df_general_filter['day_in_week'] == day])
        df_users_vaccination = user_sentiments.userdataframe(
            df_vaccination_filter[df_vaccination_filter['day_in_week'] == day])
        df_users_restriction = user_sentiments.userdataframe(
            df_restriction_filter[df_restriction_filter['day_in_week'] == day])

        # calling a function from the user_sentiments.py to create plots accordin to the filtered data.
        user_general, user_vaccination, user_restriction = user_sentiments.users_plot(df_users_general,
                                                                                      df_users_vaccination,
                                                                                      df_users_restriction)

        # This is Dictionaries created to pass in the values to index.HTML
        plots = {'line_general': line_general,
                 'line_restriction': line_restriction,
                 'line_vaccination': line_vaccination,
                 'all_line_scatters': all_line_scatters,
                 'scatter_circles': scatter_circles,
                 'pie_general': pie_general,
                 'user_general': user_general,
                 'user_vaccination': user_vaccination,
                 'user_restriction': user_restriction,
                 'table': table}

        # It creates a filtered dataset with feature mentioned by the user.
        df_general_sentiment = sentiment_plots.sentiment_dataframe(
            df_general_filter[df_general_filter['day_in_week'] == day])
        df_restriction_sentiment = sentiment_plots.sentiment_dataframe(
            df_restriction_filter[df_restriction_filter['day_in_week'] == day])
        df_vaccination_sentiment = sentiment_plots.sentiment_dataframe(
            df_vaccination_filter[df_vaccination_filter['day_in_week'] == day])

        # calling a function from the sentiment_plots.py to create pie graphs according to the filtered data.
        pie_general_sentiment, pie_vaccination_sentiment, pie_restriction_sentiment = sentiment_plots.sentiment_pie(
            df_general_sentiment,
            df_vaccination_sentiment,
            df_restriction_sentiment)

        # This is another Dictionaries created to pass in the values to index.HTML regarding the sentiment_pie graphs.
        sentiment_pie = {'pie_general_sentiment': pie_general_sentiment,
                         'pie_vaccination_sentiment': pie_vaccination_sentiment,
                         'pie_restriction_sentiment': pie_restriction_sentiment}

        # rendering the index.html template and passing in all the graphs create.
        return render_template("index.html",
                               sentiment_general=sentiment_general,
                               sentiment_vaccination=sentiment_vaccination,
                               sentiment_restriction=sentiment_restriction,
                               plots=plots, days_in_weeks=days_in_weeks,
                               sentiment_pie=sentiment_pie)


"""
The is a function used to create visualisation for the page_with_filters of the web application.The @application.route 
is used to get the users input on the web and to run the function according to users selection.
"""


@application.route('/page_with_filters', methods=["GET", "POST"])
def page_with_filters():
    # combining 3 datasets together.
    union_cleaned_df = pd.concat([df_general_filter,
                                  df_restriction_filter,
                                  df_vaccination_filter
                                  ])
    # converting a feature to datetime for ease of use.
    union_cleaned_df["tweetcreatedts"] = pd.to_datetime(union_cleaned_df["tweetcreatedts"])
    union_cleaned_df = union_cleaned_df.sort_values(by="tweetcreatedts")

    # Creating another feature with the just the date when the tweet was created.
    union_cleaned_df['date_format'] = [d.date() for d in union_cleaned_df['tweetcreatedts']]
    union_cleaned_df["date_format"] = pd.to_datetime(union_cleaned_df["date_format"])

    # it is to check whether the method requested by the web page is equal to GET.
    if request.method == "GET":

        # assigning values to use as filtering values.
        start_date = '2021-03-12'
        end_date = '2021-03-20'

        # creating 2 datasets according to filter values and combining together.
        start = union_cleaned_df[union_cleaned_df.date_format == pd.Timestamp(start_date)]
        end = union_cleaned_df[union_cleaned_df.date_format == pd.Timestamp(end_date)]
        df_with_date = pd.concat([start, end])

        # creating a dataframe according to filter values and creating a graphs for negative sentiment.
        df_users_negative = user_sentiments.userdataframe(df_with_date[df_with_date['sentiment'] == 'negative'])
        user_bar_chart_negative = page_with_filter.create_graph_user_negative(df_users_negative)

        # creating a dataframe according to filter values and creating a graphs for positive sentiment.
        df_users_positive = user_sentiments.userdataframe(df_with_date[df_with_date['sentiment'] == 'positive'])
        user_bar_chart_positive = page_with_filter.create_graph_user_positive(df_users_positive)

        #  creating a dataframe according to filter values and creating a pie graphs to identify the sentiment.
        df_single_sentiment = sentiment_plots.sentiment_dataframe(df_with_date)
        pie_sentiment = sentiment_plots.single_sentiment_pie(df_single_sentiment)

        # Create a table according to the filtered dataset.
        table_date = create_table(df_with_date)

        # rendering the page_with_filters.html template and passing in all the graphs created.
        return render_template("page_with_filters.html",
                               user_bar_chart_negative=user_bar_chart_negative,
                               user_bar_chart_positive=user_bar_chart_positive,
                               pie_sentiment=pie_sentiment,
                               table_date=table_date)

    else:
        # If the requested method  by page_with_filters.HTML is POST run the following code.

        # getting the values from the HTML form.
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # creating 2 datasets according to filter values and combining together.
        start = union_cleaned_df[union_cleaned_df.date_format == pd.Timestamp(start_date)]
        end = union_cleaned_df[union_cleaned_df.date_format == pd.Timestamp(end_date)]
        df_with_date = pd.concat([start, end])

        # creating a dataframe according to filter values and creating a graphs for negative sentiment.
        df_users_negative = user_sentiments.userdataframe(df_with_date[df_with_date['sentiment'] == 'negative'])
        user_bar_chart_negative = page_with_filter.create_graph_user_negative(df_users_negative)

        # creating a dataframe according to filter values and creating a graphs for positive sentiment.
        df_users_positive = user_sentiments.userdataframe(df_with_date[df_with_date['sentiment'] == 'positive'])
        user_bar_chart_positive = page_with_filter.create_graph_user_positive(df_users_positive)

        #  creating a dataframe according to filter values and creating a pie graphs to identify the sentiment.
        df_single_sentiment = sentiment_plots.sentiment_dataframe(df_with_date)
        pie_sentiment = sentiment_plots.single_sentiment_pie(df_single_sentiment)

        # Create a table according to the filtered dataset.
        table_date = create_table(df_with_date)

        # rendering the page_with_filters.html template and according to the users input.
        return render_template("page_with_filters.html",
                               user_bar_chart_negative=user_bar_chart_negative,
                               user_bar_chart_positive=user_bar_chart_positive,
                               pie_sentiment=pie_sentiment,
                               table_date=table_date)


"""
This is a function used to create the graphs with live data which is added to the SQL database by the app created to 
collect live twitter data regarding covid-19.The following link show the Github repo to the data collector app:
https://github.com/FabioPalliparambil98/live_covid19_tweets
"""


@application.route('/live_tweets')
def live_tweets():
    line_graph, choropleth_map = live_tweets_graphs.live_tweet()
    return render_template("live_tweets.html", choropleth_map=choropleth_map, line_graph=line_graph)


"""
This is a function created to retrieve the contact details entered by the user in the web application to contact 
the developers.
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
This is a function created to display the Covid-19 cases dashboard. It consists os total cases,deaths and recovered and 
a graph to understand the cases of covid-29 in different locations.
"""


@application.route('/covidcases')
def covidcases():
    df = df_covid_cases_data
    df.index = df['Country/Region']
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["confirmed"],
            name="No of confirmed cases",
            marker_color='#087fff',
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
            marker_color='#b5ff08',
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
            'text': '<span style="font-size: 20px;">Global Covid-19 cases</span><br><span style="font-size: 10px;"></span>',
            'y': 0.97,
            'x': 0.45,
            'xanchor': 'center',
            'yanchor': 'top'}
    )

    # Set x-axis title
    fig.update_xaxes(tickangle=45)

    # Set y-axes titles
    fig.update_yaxes(title_text="No of confirmed cases",
                     secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="cases/millions", tickangle=45,
                     secondary_y=True, showgrid=False)

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()

    return render_template('covidcases.html', plot_json=plot_json,
                           total_all_confirmed=total_all_confirmed,
                           total_all_recovered=total_all_recovered,
                           total_all_deaths=total_all_deaths)
    return plot_json


"""
It get the sentimental value
"""


def sentiment_data(df):
    df_sentiment = df['sentiment'].value_counts()
    negative = df_sentiment.loc[0]
    positive = df_sentiment.loc[1]
    if negative > positive:
        return "negative"
    else:
        return "positive"


"""
create_table
"""


def create_table(df):
    df = df.head(20)


    table = go.Figure([go.Table(
        header=dict(
            values=["username", "acctdesc", "location", "following", "followers", "total<br>tweets",
                    "user<br>createdts", "tweet<br>created", "retweet<br>count", "text", "hashtags", "Month", "Hour",
                    "day_in_week", "day", "sentiment"],
            font=dict(size=10),
            align="left",
            fill_color='paleturquoise'
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[1:]],
            align="left",
            fill_color='lavender',
        )
    )
    ])

    table.update_layout(
        height=800,
        width=1500,
        showlegend=False,
        title_text="Covid-19 Data Collected Sample",
    )

    tableJSON = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)

    return tableJSON


if __name__ == '__main__':
    application.run()
