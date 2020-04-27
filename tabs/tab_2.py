import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import datetime
import pandas as pd
import os

from tabs.utils import line_plot, map_plot
from app import app

UPDATE_INTERVAL = 60*5 #seconds

layout = html.Div(children=[
    html.H1(
        children='Speed forecasting for Rama IV',
        style={
            'textAlign': 'center',
        }
    ),

    html.H1(children='พยากรณ์ความเร็วเฉลี่ยบนถนนพระราม 4', style={
        'textAlign': 'center',
    }),

    html.Div(children='ความเร็วคลาดเคลื่อนได้ประมาณ 10 กม/ชม', style={
        'textAlign': 'center',
        'padding': '5px', 
        'fontSize': '12px'
    }),
    

    html.Div(children='speed may deviate by 10km/hr ', style={
        'textAlign': 'center',
        'padding': '5px', 
        'fontSize': '12px'
    }),

    # html.Div(id='test-interval'),
    
    html.Div([dcc.Graph(id='predict-graph')],style={'padding' : 20}),
    html.Div([dcc.Graph(id='predict-map-5min')], style={'padding' : 20}),
    html.Div([dcc.Graph(id='predict-map-10min')],style={'padding' : 20}), 

    dcc.Interval(
        id='interval-predict',
        interval=UPDATE_INTERVAL*1000, # in milliseconds
        n_intervals=0
    ),

    html.Div(id='intermediate-value2', style={'display': 'none'})
])

# @app.callback(Output('test-interval', 'children'),
#               [Input('interval-predict', 'n_intervals')])
# def update_time(n):
#     now = datetime.datetime.now()
#     cur_time = now.strftime("%H:%M:%S")
#     style = {'padding': '5px', 'fontSize': '16px'}
#     return cur_time     

# Multiple components can update everytime interval gets fired.
@app.callback(Output('intermediate-value2', 'children'),
            [Input('interval-predict', 'n_intervals')])
def fetching_prediction(n):
    print("beginning request")
    url = 'https://ramaivpredict-s66niuzd5q-de.a.run.app/predict'
    now = datetime.datetime.now()
    now = now.strftime("%Y/%m/%d %H:%M:%S")

    payload = {
        'datetime' : now
    }

    # r = requests.get(url)
    r = requests.post(url, json = payload)
    r = r.json()
    payload = {'now':now}
    payload.update(r)
    print("Finish fetching data")
    return json.dumps(payload)

@app.callback(Output('predict-graph', 'figure'),
            [Input('intermediate-value2', 'children')])
def update_line_graph(jsonified_data):
    data = json.loads(jsonified_data)
    df = pd.read_json(data['df'], orient='split')
    now = data['now']

    return line_plot.plot_line_pred(df,now)#, now

@app.callback(Output('predict-map-5min', 'figure'),
            [Input('intermediate-value2', 'children')])
def update_map(jsonified_data):
    data = json.loads(jsonified_data)
    df = pd.read_json(data['df'], orient='split')
    time_list = sorted(df['time'].unique())

    df = df[df['time'] == time_list[0]]
    now = time_list[0]

    return map_plot.plot_map(df,now)#, now

@app.callback(Output('predict-map-10min', 'figure'),
            [Input('intermediate-value2', 'children')])
def update_map(jsonified_data):
    data = json.loads(jsonified_data)
    df = pd.read_json(data['df'], orient='split')
    time_list = sorted(df['time'].unique())
    
    df = df[df['time'] == time_list[1]]
    now = time_list[1]

    return map_plot.plot_map(df,now)#, now