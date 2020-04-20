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

from app import app

UPDATE_INTERVAL = 60*5 #seconds

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"""C:\Users\givew\Documents\senior\dashboard\tabs\config\gcloud_credential.json"""
project_id = 'taxi-272612'
client = bigquery.Client()

east_w = []
east_seg = []
east_seg_id = {}
west_w = []
west_seg = []
west_seg_id = {}
rama_iv_way = []
los_color = {
    "A":"#03fc52",
    "B":"#03fc52",
    "C":"#fcfc03",
    "D":"#fcfc03",
    "E":"#fc9803",
    "F":"#ff0000",
    "X":"#fcfcfc"
}
group_color = {
    "การจราจรคล่องตัว":"#03fc52",
    "การจราจรหนาแน่น":"#fcfc03",
    "การจราจรติดขัด":"#fc9803",
    "การจราจรติดขัดมาก":"#ff0000",
    "ไม่มีข้อมูล":"#fcfcfc"
}


def load_segment():
    global east_w, east_seg, east_seg_id, west_w, west_seg, west_seg_id, rama_iv_way
    print(THIS_FOLDER)
    ways_json_f = os.path.join(THIS_FOLDER, 'config', 'segment.json')
    with open(ways_json_f) as json_file:
        ways_json = json_file.read()
        ways_json = json.loads(ways_json)
    east_w = ways_json['east']['way_id']
    east_w = [str(w) for w in east_w]
    east_seg = ways_json['east']['segment']
    west_w = ways_json['west']['way_id']
    west_w = [str(w) for w in west_w]
    west_seg = ways_json['west']['segment']
    rama_iv_way = east_w + west_w

    lon_seg_f =  os.path.join(THIS_FOLDER, 'config', 'lon_to_seg_map.json')
    with open(lon_seg_f) as json_file:
        lon_seg = json_file.read()
        lon_seg = json.loads(lon_seg)
    east_seg_id = lon_seg['east_seg_id']
    west_seg_id = lon_seg['west_seg_id']
    east_seg_id = { float(key):value for key,value in east_seg_id.items()}
    west_seg_id = { float(key):value for key,value in west_seg_id.items()}

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

def cal_los(row):
  speed = row['speed_kph']
  if speed == 0:
    los = "X"
    # group = "ไม่มีข้อมูล"
  elif speed < 21:
    los = "F"
    # group = "การจราจรติดขัดมาก"
  elif speed <= 26:
    los = "E"
    # group = "การจราจรติดขัด"
  elif speed <= 33:
    # group = "การจราจรหนาแน่น"
    los = "D"
  elif speed <= 46:
    los = "C"
    # group = "การจราจรคล่องตัว"
  elif speed <= 59:
    los = "B"
    # group = "การจราจรคล่องตัว"
  else:
    los = "A"
    # group = "การจราจรคล่องตัว"
  return los


def plot_line(df,date):
    fig = px.line(df, x="lon3", y="speed_kph", title='ค.เร็วเฉลี่ย(km/h) ทุกๆ100เมตร ',color = "direction")

    fig.update_layout(
        title='Speed line %s'%(date),
        xaxis_title = "longitude",
        xaxis_showgrid = False,
        xaxis_range=[100.533,100.594],
        yaxis_title = "speed km/h",
        yaxis_range=[0,90],
        yaxis_showgrid = False,
        xaxis_nticks=35,
        yaxis_nticks = 35,
        autosize=True,
        # height = 600,
        # width = 1400,
        shapes=[     
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 1,
                xref= 'x', x0= 100.536, x1= 100.536,
            ),         
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 1,
                xref= 'x', x0= 100.545, x1= 100.545,
            ),
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 1,
                xref= 'x', x0= 100.552, x1= 100.552,
            ),
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 1,
                xref= 'x', x0= 100.558, x1= 100.558,
            ),
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 1,
                xref= 'x', x0= 100.567, x1= 100.567,
            ),
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 1,
                xref= 'x', x0= 100.584, x1= 100.584,
            ),
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 1,
                xref= 'x', x0= 100.592, x1= 100.592,
            ),
            #speed
            dict(
                layer="below",
                x0= 100.533,
                x1= 100.594,
                y0= 0,
                y1= 21,
                type= 'rect',
                fillcolor= '#EF9A9A',
                line_width=0
            ),
            dict(
                layer="below",
                x0= 100.533,
                x1= 100.594,
                y0= 21,
                y1= 26,
                type= 'rect',
                fillcolor= '#FFC300',
                line_width=0
            ),
            dict(
                layer="below",
                x0= 100.533,
                x1= 100.594,
                y0= 26,
                y1= 46,
                type= 'rect',
                fillcolor= '#FFFF8D',
                line_width=0
            ),
            dict(
                layer="below",
                x0= 100.533,
                x1= 100.594,
                y0= 46,
                y1= 90,
                type= 'rect',
                fillcolor= '#CCFF90',
                line_width=0
            ),

    ])

    fig.add_annotation(
                x=100.536,
                y= 70,
                text="แยกศาลาแดง",
                showarrow=False,
                font = dict(
                    family='Courier New, monospace',
                    size=18,
                    )
                )

    fig.add_annotation(
                x=100.545,
                y= 70,
                text="แยกวิทยุ",
                showarrow=False,
                font = dict(
                    family='Courier New, monospace',
                    size=18,
                    )
                )

    fig.add_annotation(
                x=100.551,
                y= 70,
                text="แยกใต้ทางด่วน",
                showarrow=False,
                font = dict(
                    family='Courier New, monospace',
                    size=18,
                    )
                )

    fig.add_annotation(
                x=100.558,
                y= 70,
                text="แยกพระราม4",
                showarrow=False,
                font = dict(
                    family='Courier New, monospace',
                    size=18,
                    )
                )

    fig.add_annotation(
                x=100.567,
                y= 70,
                text="แยกเกษมราษฎร์",
                showarrow=False,
                font = dict(
                    family='Courier New, monospace',
                    size=18,
                    )
                )

    fig.add_annotation(
                x=100.584,
                y= 70,
                text="แยกกล้วยน้ำไท",
                showarrow=False,
                font = dict(
                    family='Courier New, monospace',
                    size=18,
                    )
                )

    fig.add_annotation(
                x=100.592,
                y= 70,
                text="แยกพระขโนง",
                showarrow=False,
                font = dict(
                    family='Courier New, monospace',
                    size=18,
                    )
                )

    # fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500

    return fig

def plot_map(df, date):

    df['los'] = df.apply(lambda row: cal_los(row), axis=1)

    fig = go.Figure()

  #plot way legend
    fig.add_trace(go.Scattermapbox(
        name = "🢂 East Bound",
        mode = "markers",
        legendgroup = "East",
        showlegend = True,
        lon = [-50],
        lat = [30],
        marker = {'color': '#fcfcfc'}
    ))
    fig.add_trace(go.Scattermapbox(
        name = "🢀 West Bound",
        mode = "markers",
        legendgroup = "West",
        showlegend = True,
        lon = [-50],
        lat = [30],
        marker = {'color': '#fcfcfc'}
    ))

      #plot Level of service legend
    for g in list(group_color.keys()):
        name_c = g
        fig.add_trace(go.Scattermapbox(
            name = name_c,
            mode = "lines",
            showlegend = True,
            lon = [-50],
            lat = [30],
            visible = True,
            marker = {'color': group_color[g]}
            )
        )

    def add_color(row, fig):
        if row['direction'] == 'east':
            i = east_seg_id[round(row['lon3'], 3)]
            seg_start = east_seg[i]
            seg_end = east_seg[i+1]
            lat_a = [seg_start[1],seg_end[1]]
            lon_a = [seg_start[2],seg_end[2]]
            color = los_color[row['los']]
            legendgroup = 'East'
        else:
            i = west_seg_id[round(row['lon3'], 3)]
            seg_start = west_seg[i]
            seg_end = west_seg[i+1]
            lat_a = [seg_start[1],seg_end[1]]
            lon_a = [seg_start[2],seg_end[2]]
            color = los_color[row['los']]
            legendgroup = 'West'
        fig.add_trace(go.Scattermapbox(
            name = "",
            mode = "markers+lines",
            legendgroup = legendgroup,
            showlegend = False,
            lat = lat_a,
            lon = lon_a,
            line = {'color':color ,'width':5},
            marker = {'size': 6},
            opacity = 0.7)
        )
    df.apply(lambda row: add_color(row,fig), axis=1)

    fig.update_layout(
        title= "Level of Service : " + date,
        autosize=True,
        margin ={'l':0,'t':32,'b':0,'r':0},
        mapbox = {
            'style': "open-street-map",
            'center': {'lon': 100.565, 'lat': 13.72},
            'zoom': 14}
    )


    return fig


load_segment()
# connect_bq()

layout = html.Div(children=[
    html.H1(
        children='Live สภาพการจราจรถนนพระราม 4',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(id='live-update-text'),
    html.Div([dcc.Graph(id='live-update-map')], style={'padding' : 20}),
    html.Div([dcc.Graph(id='live-update-graph')],style={'padding' : 20}),
    dcc.Interval(
        id='interval-component',
        interval=UPDATE_INTERVAL*1000, # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-component2',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    #Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component2', 'n_intervals')])
def update_time(n):
    now = datetime.datetime.now()
    cur_time = now.strftime("%H:%M:%S")
    style = {'padding': '5px', 'fontSize': '16px'}
    return cur_time     



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

    return plot_line(df,now)#, now

@app.callback(Output('live-update-map', 'figure'),
            [Input('intermediate-value', 'children')])
def update_map(jsonified_data):
    data = json.loads(jsonified_data)
    df = pd.read_json(data['df'], orient='split')
    now = data['now']

    return plot_map(df,now)#, now