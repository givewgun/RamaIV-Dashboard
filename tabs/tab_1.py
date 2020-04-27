'''
Live update every 1 minute
'''
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import pandas as pd
import json

# from google.oauth2 import service_account
# import pandas_gbq
from google.cloud import bigquery
import os

from tabs.utils import line_plot, map_plot, segmet_loader
from app import app

UPDATE_INTERVAL = 60*5 #seconds

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"""C:\Users\givew\Documents\senior\dashboard\tabs\config\gcloud_credential.json"""
project_id = 'taxi-272612'
client = bigquery.Client()

east_w = segmet_loader.east_w
west_w = segmet_loader.west_w
rama_iv_way = segmet_loader.rama_iv_way

# def connect_bq():
#     credentials = service_account.Credentials.from_service_account_file(
#         os.path.join(THIS_FOLDER, 'config', 'gcloud_credential.json'),
#     )
#     pandas_gbq.context.credentials = credentials
#     pandas_gbq.context.project = "taxi-272612"

def gen_query():
    now = datetime.datetime.now()
    cur_time = now.strftime("%H:%M:%S")
    cur_date = "201908" + now.strftime("%d")
    # cur_date = "201908"

    fmt = """FORMAT_TIME("%R",time)"""
    sql = """
    DECLARE cur_time TIME DEFAULT TIME "%s";
    select %s as time, wayids as wayids	, ROUND(projectedlng,3) as lon3, AVG(speed_km_h) as `speed_kph` from saved.combined%s
    where time between TIME_SUB(cur_time, INTERVAL %s SECOND) and cur_time GROUP BY wayids, ROUND(projectedlng,3), %s;
    """%(cur_time, fmt, cur_date, UPDATE_INTERVAL, fmt)

    return (sql, "%s %s"%(cur_date,cur_time))

# connect_bq()

layout = html.Div(children=[
    html.H1(
        children='Live สภาพการจราจรถนนพระราม 4',
        style={
            'textAlign': 'center',
        }
    ),
    # html.Div(id='live-update-text'),
    html.Div([dcc.Graph(id='live-update-map')], style={'padding' : 20}),
    html.Div([dcc.Graph(id='live-update-graph')],style={'padding' : 20}),
    dcc.Interval(
        id='interval-component',
        interval=UPDATE_INTERVAL*1000, # in milliseconds
        n_intervals=0
    ),
    # dcc.Interval(
    #     id='interval-component2',
    #     interval=1*1000, # in milliseconds
    #     n_intervals=0
    # ),
    #Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])


# @app.callback(Output('live-update-text', 'children'),
#               [Input('interval-component2', 'n_intervals')])
# def update_time(n):
#     now = datetime.datetime.now()
#     cur_time = now.strftime("%H:%M:%S")
#     style = {'padding': '5px', 'fontSize': '16px'}
#     return cur_time     



# Multiple components can update everytime interval gets fired.
@app.callback(Output('intermediate-value', 'children'),
            [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    sql, now = gen_query()
    
    df = client.query(sql, project=project_id).to_dataframe()

    df = df[df['wayids'].isin(rama_iv_way)]
    df['direction'] = 'west'
    df.loc[df['wayids'].isin(east_w), 'direction'] = 'east'
    df = df.groupby(['direction','lon3']).mean()['speed_kph'].reset_index()
    
    payload = {
        'df' : df.to_json(orient='split', date_format='iso'),
        'now' : now
    }
    return json.dumps(payload)

@app.callback(Output('live-update-graph', 'figure'),
            [Input('intermediate-value', 'children')])
def update_line_graph(jsonified_data):
    data = json.loads(jsonified_data)
    df = pd.read_json(data['df'], orient='split')
    now = data['now']

    return line_plot.plot_line(df,now)#, now

@app.callback(Output('live-update-map', 'figure'),
            [Input('intermediate-value', 'children')])
def update_map(jsonified_data):
    data = json.loads(jsonified_data)
    df = pd.read_json(data['df'], orient='split')
    now = data['now']

    return map_plot.plot_map(df,now)#, now