import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
        title_text="Speed Heatmap %s"%(date), 
        height=600, 
        # width = 1200,
        autosize=True,
        )
    

    return sub