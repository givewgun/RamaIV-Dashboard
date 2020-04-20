import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app import app

date_dict = {
    'all_weekday':'วันธรรมดา (จ - ศ)',
    'normal_weekend':'วันหยุด (ส - อา)',
    'normal_monday':'วันจันทร์',
    'normal_friday':'วันศุกร์',
    'mother_day':'วันแม่'
}

date_dropdown = [{'label': date_dict[k],'value': k } for k in date_dict]

df_date = {}

def load_data(date):
    f = 'https://storage.googleapis.com/speed_csv/speed_%s.csv'%(date)
    df = pd.read_csv(f)
    df.sort_values(by=['round_min','lon3'], inplace = True)
    return df

def init_data():
    for k in date_dict:
        df_date[k] = load_data(k)

init_data()

#######################################################################################
def format_df(df):
    east_df = df[df['direction'] == 'east']
    east_df.sort_values(by=['round_min','lon3'], inplace = True)
    west_df = df[df['direction'] == 'west']
    west_df.sort_values(by=['round_min','lon3'], inplace = True)
    return [east_df, west_df]


def plot_heat(df,date):
    east_df, west_df = format_df(df)
    f1 =go.Heatmap(
        z=east_df['speed_km/h'],
        x=east_df['lon3'],
        y=east_df['round_min'],
        hovertemplate =
        '<b>Speed</b>: %{z} km/h<br>'+
        '<b>Time</b>: %{y}<br>'+
        '<b>Longitude</b>: %{x}'
        ,
        colorscale='rdylgn',
        colorbar={"title": 'Speed km/h'},
        showscale = False,
        xgap = 0,
        ygap = 0.1)

    f2 = go.Heatmap(
            z=west_df['speed_km/h'],
            x=west_df['lon3'],
            y=west_df['round_min'],
            hovertemplate =
            '<b>Speed</b>: %{z} km/h<br>'+
            '<b>Time</b>: %{y}<br>'+
            '<b>Longitude</b>: %{x}'
            ,
            colorscale='rdylgn',
            colorbar={"title": 'Speed km/h'},
            xgap = 0,
            ygap = 0.1)

    sub = make_subplots(rows=1, cols=2, subplot_titles=("ขาเข้า","ขาออก"))
    sub.add_trace(f1, row = 1, col = 2)
    sub.add_trace(f2, row = 1, col = 1)

    sub.update_xaxes(title_text="longitude", 
                    tickmode = 'array',
                    tickvals = [100.536,100.545, 100.552, 100.558, 100.567, 100.584,100.592],
                    ticktext = ['แยกศาลาแดง','แยกวิทยุ', 'แยกใต้ทางด่วน', 'แยกพระราม4', 'แยกเกษมราฏฐ์', "แยกกล้วยน้ำไท","แยกพระขโนง"],
                    tickangle = 45
                    , row=1, col=2, nticks=35)
    sub.update_xaxes(title_text="longitude", 
                    tickmode = 'array',
                    tickvals = [100.536,100.545, 100.552, 100.558, 100.567, 100.584,100.592],
                    ticktext = ['แยกศาลาแดง','แยกวิทยุ', 'แยกใต้ทางด่วน', 'แยกพระราม4', 'แยกเกษมราฏฐ์', "แยกกล้วยน้ำไท","แยกพระขโนง"],
                    tickangle = 45
                    ,row=1, col=1, nticks=35)

    sub.update_yaxes(row=1, col=2, nticks=42)
    sub.update_yaxes(title_text="time", row=1, col=1, nticks=35)


    # Update title and height
    sub.update_layout(
        title_text="Speed Heatmap %s"%(date_dict[date]), 
        height=600, 
        # width = 1200,
        autosize=True,
        )
    

    return sub


def plot_line(df,date):
    fig = px.line(df, x="lon3", y="speed_km/h", title='ค.เร็วเฉลี่ย(km/h) ทุกๆ100เมตร ',color = "direction",animation_frame="round_min")

    fig.update_layout(
        title='Speed line %s'%(date_dict[date]),
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

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500

    return fig

    
# df = load_data()


layout = html.Div(children=[
    html.H1(
        children='พระราม 4 Dashboard',
        style={
            'textAlign': 'center',
        }
    ),

    html.Div(children='ความเร็วเฉลี่ยบนถนนพระรามที่ 4', style={
        'textAlign': 'center',
    }),

    html.Div(children = [dcc.Dropdown(
        id='date-dropdown',
        options=date_dropdown,
        value='all_weekday'
        )],style={'textAlign': 'center','padding' : 20}
    ),
    

    html.Div(id='dd-output-container'),


    

    dcc.Loading(id = 'loading-speed',
        children = [
            html.Div([dcc.Graph(
                id='speed-line',
            # figure= plot_line(df)
            )],style={'padding' : 20})
        ]
    ),
    
    dcc.Loading(id = 'loading-heat',
        children = [
            html.Div([dcc.Graph(
                id='speed-heat',
                # figure= plot_heat(df)
            )], style={'padding' : 20})
        ]
    ),
    

    
])



@app.callback(
    dash.dependencies.Output('speed-line', 'figure'),
    [dash.dependencies.Input('date-dropdown', 'value')])
def update_speed(value):
    return plot_line(df_date[value],value)


@app.callback(
    dash.dependencies.Output('speed-heat', 'figure'),
    [dash.dependencies.Input('date-dropdown', 'value')])
def update_heat(value):
    # df = load_data(value)
    return plot_heat(df_date[value],value)


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('date-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)