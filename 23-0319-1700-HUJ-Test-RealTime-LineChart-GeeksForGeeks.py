import dash
from dash.dependencies import Output, Input
##jwc o import dash_core_components as dcc
##jwc o import dash_html_components as html
from dash import dcc
from dash import html

import plotly
import plotly.graph_objs as go

import random
from collections import deque

import time
import serial
from datetime import datetime

##jwc o X_ArrayList = deque(maxlen = 20)
X_ArrayList = deque(maxlen = 5)
X_ArrayList.append(1)
##jwc o Y_ArrayList = deque(maxlen = 20)
Y_ArrayList = deque(maxlen = 5)
Y_ArrayList.append(1)

##jwc n was here:     ser = serial.Serial(

app = dash.Dash(__name__)
  
app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            ##jwc yo interval = 1000,
            interval = 500,
            n_intervals = 0
        ),
    ]
)
  
@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)
def update_graph_scatter(n):

    x=ser.readline()
    if x:
        dt = datetime.now()
        datestamp = str(dt)[:16]
        ###jwc o temp, light = x.decode().split(':')
        ###jwc 23-0310-1120 y id, te, li, co = x.decode().split(',')
        ###jwc n id, te, li, co, m1, m2, m3, m4 = x.decode().split('|')

        ###jwc o newData = [datestamp,temp,light]
        ###jwc 23-0310-1120 y newData = [datestamp, id, te, li, co]
        ###jwc n newData = [datestamp, id, te, li, co, m1, m2, m3, m4]
        newData = [datestamp, x]
        print(newData)

    X_ArrayList.append(X_ArrayList[-1]+1)
    ##jwc yo Y_ArrayList.append(Y_ArrayList[-1]+Y_ArrayList[-1] * random.uniform(-0.1,0.1))
    Y_ArrayList.append(Y_ArrayList[-1] + int(random.uniform(-5,5)))
    print("*** "+str(X_ArrayList)+" "+str(Y_ArrayList))
  
    data = plotly.graph_objs.Scatter(
            x=list(X_ArrayList),
            y=list(Y_ArrayList),
            name='Scatter',
            mode='lines+markers'
    )
  
    return {'data': [data],
            ##jwc axis unit labels
            'layout' : go.Layout(xaxis=dict(range=[min(X_ArrayList),max(X_ArrayList)]),yaxis = dict(range = [min(Y_ArrayList),max(Y_ArrayList)]),)}
  
if __name__ == '__main__':

    ser = serial.Serial(
            ##jwc o port='/dev/ttyACM0',
            port='COM3',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
    )

    ##jwc yo app.run_server()
    app.run_server(debug=True)
    