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