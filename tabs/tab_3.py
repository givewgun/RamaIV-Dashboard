import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from tabs.utils import line_plot, heat_plot
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
    

    # html.Div(id='dd-output-container'),


    

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
    return line_plot.plot_line_csv(df_date[value],date_dict[value])


@app.callback(
    dash.dependencies.Output('speed-heat', 'figure'),
    [dash.dependencies.Input('date-dropdown', 'value')])
def update_heat(value):
    # df = load_data(value)
    return heat_plot.plot_heat(df_date[value],date_dict[value])


# @app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [dash.dependencies.Input('date-dropdown', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)