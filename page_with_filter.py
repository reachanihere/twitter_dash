import settings
import pandas as pd
import json
import plotly
import plotly.graph_objs as go

def graph_with_filter(df):
    '''
    Plot the Line Chart
    '''
    line_chart = go.Figure()
    # Clean and transform data to enable time series

    line_chart.add_trace(go.Scatter(
        x=df[df['sentiment'] == 'negative'].reset_index(drop=True),
        y=df['retweetcount'],
        name="Negative",
        opacity=0.8))
    line_chart.add_trace(go.Scatter(
        x=df[df['sentiment'] == 'positive'].reset_index(drop=True),
        y=df['retweetcount'],
        name="Positive",
        opacity=0.8))
    line_chart.update_layout(title_text="Sentiment Analysis on Collected COVID-19 data from Twitter", title_font_size=20)

    line_chart_JSON = json.dumps(line_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return line_chart_JSON


def create_graph_user_negative(df):
    '''
        Plot the bar Chart
        '''
    bar_chart = go.Figure()

    bar_chart.add_trace(go.Scatter(
        x=df['username'],
        y=df['Count'],
        marker_color='lightskyblue',
        opacity=0.8))

    bar_chart.update_layout(title_text="The top users who tweeted negative tweets", title_font_size=20)

    bar_chart_JSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_chart_JSON

def create_graph_user_positive(df):
    '''
            Plot the bar Chart
            '''
    bar_chart = go.Figure()

    bar_chart.add_trace(go.Scatter(
        x=df['username'],
        y=df['Count'],
        marker_color='lightskyblue',
        opacity=0.8))
    bar_chart.update_layout(title_text="The top users who tweeted positive tweets", title_font_size=20)

    bar_chart_JSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_chart_JSON
