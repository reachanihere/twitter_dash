import settings
import pandas as pd
import json
import plotly
import plotly.graph_objs as go

"""
Create a Scatter graph with usernames and counts.
Then a json data is returned at the end of the function
"""


def create_graph_user_negative(df):

    bar_chart = go.Figure()

    bar_chart.add_trace(go.Scatter(
        x=df['username'],
        y=df['Count'],
        marker_color='rgb(76, 76, 214)',
        opacity=0.8))

    bar_chart.update_layout(title_text="The top users who tweeted negative tweets", title_font_size=20)

    # Set x-axis title
    bar_chart.update_xaxes(tickangle=45)
    bar_chart.update_xaxes(title_text="User names")

    # Set y-axes titles
    bar_chart.update_yaxes(title_text="Number of Tweets tweeted")

    bar_chart_JSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_chart_JSON


"""
Create a Scatter graph with usernames and counts.
Then a json data is returned at the end of the function
"""


def create_graph_user_positive(df):

    bar_chart = go.Figure()

    bar_chart.add_trace(go.Scatter(
        x=df['username'],
        y=df['Count'],
        marker_color='rgb(207, 42, 42)',
        opacity=0.8))
    bar_chart.update_layout(title_text="The top users who tweeted positive tweets", title_font_size=20)

    # Set x-axis title
    bar_chart.update_xaxes(tickangle=45)
    bar_chart.update_xaxes(title_text="User names")

    # Set y-axes titles
    bar_chart.update_yaxes(title_text="Number of Tweets tweeted")

    bar_chart_JSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_chart_JSON
