
import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from tabs.utils import segmet_loader

east_seg = segmet_loader.east_seg
east_seg_id = segmet_loader.east_seg_id
west_seg = segmet_loader.west_seg
west_seg_id = segmet_loader.west_seg_id

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