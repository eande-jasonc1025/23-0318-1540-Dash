##jwc https://dash.plotly.com/live-updates

##jwc
##
## The dcc.Interval Component
## Components in Dash usually update through user interaction like selecting a dropdown, dragging a slider, or hovering over points.
## If you're building an application for monitoring, you may want to update components in your application every few seconds or minutes.
## The dcc.Interval element allows you to update components on a predefined interval. The n_intervals property is an integer that is automatically incremented every time interval milliseconds pass. You can listen to this variable inside your app's callback to fire the callback on a predefined interval.
##
## This example pulls data from live satellite feeds and updates the graph and the text every second.

import datetime

import dash
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output

# pip install pyorbital
##jwc no from pyorbital.orbital import Orbital
##jwc no satellite = Orbital('TERRA')

##jwc
import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    ##jwc no lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    ##
    lon = random.uniform(-5,5)
    lat = random.uniform(-5,5)
    alt = random.uniform(-5,5)

    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    ##jwc no satellite = Orbital('TERRA')
    data = {
        'time': [],
        'Latitude': [],
        'Longitude': [],
        'Altitude': []
    }

    # Collect some data
    for i in range(180):
        time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
        ##jwc
        ##
        ## lon, lat, alt = satellite.get_lonlatalt(
        ##    time
        ## )
        lon = random.uniform(-5,5)
        lat = random.uniform(-5,5)
        alt = random.uniform(-5,5)
        
        data['Longitude'].append(lon)
        data['Latitude'].append(lat)
        data['Altitude'].append(alt)
        data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['Altitude'],
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['Longitude'],
        'y': data['Latitude'],
        'text': data['time'],
        'name': 'Longitude vs Latitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)