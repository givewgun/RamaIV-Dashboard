import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def annotate_line(fig, title, date):
    fig.update_layout(
        title='%s for %s' % (title, date),
        xaxis_title="longitude",
        xaxis_showgrid=False,
        xaxis_range=[100.533, 100.594],
        yaxis_title="speed km/h",
        yaxis_range=[0, 90],
        yaxis_showgrid=False,
        xaxis_nticks=35,
        yaxis_nticks=35,
        autosize=True,
        # height = 600,
        # width = 1400,
        shapes=[
            dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=100.536, x1=100.536,
            ),
            dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=100.545, x1=100.545,
            ),
            dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=100.552, x1=100.552,
            ),
            dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=100.558, x1=100.558,
            ),
            dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=100.567, x1=100.567,
            ),
            dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=100.584, x1=100.584,
            ),
            dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='x', x0=100.592, x1=100.592,
            ),
            # speed
            dict(
                layer="below",
                x0=100.533,
                x1=100.594,
                y0=0,
                y1=21,
                type='rect',
                fillcolor='#EF9A9A',
                line_width=0
            ),
            dict(
                layer="below",
                x0=100.533,
                x1=100.594,
                y0=21,
                y1=26,
                type='rect',
                fillcolor='#FFC300',
                line_width=0
            ),
            dict(
                layer="below",
                x0=100.533,
                x1=100.594,
                y0=26,
                y1=46,
                type='rect',
                fillcolor='#FFFF8D',
                line_width=0
            ),
            dict(
                layer="below",
                x0=100.533,
                x1=100.594,
                y0=46,
                y1=90,
                type='rect',
                fillcolor='#CCFF90',
                line_width=0
            ),

        ])

    fig.add_annotation(
        x=100.536,
        y=70,
        text="แยกศาลาแดง",
        showarrow=False,
        font=dict(
            family='Courier New, monospace',
            size=18,
        )
    )

    fig.add_annotation(
        x=100.545,
        y=70,
        text="แยกวิทยุ",
        showarrow=False,
        font=dict(
            family='Courier New, monospace',
            size=18,
        )
    )

    fig.add_annotation(
        x=100.551,
        y=70,
        text="แยกใต้ทางด่วน",
        showarrow=False,
        font=dict(
            family='Courier New, monospace',
            size=18,
        )
    )

    fig.add_annotation(
        x=100.558,
        y=70,
        text="แยกพระราม4",
        showarrow=False,
        font=dict(
            family='Courier New, monospace',
            size=18,
        )
    )

    fig.add_annotation(
        x=100.567,
        y=70,
        text="แยกเกษมราษฎร์",
        showarrow=False,
        font=dict(
            family='Courier New, monospace',
            size=18,
        )
    )

    fig.add_annotation(
        x=100.584,
        y=70,
        text="แยกกล้วยน้ำไท",
        showarrow=False,
        font=dict(
            family='Courier New, monospace',
            size=18,
        )
    )

    fig.add_annotation(
        x=100.592,
        y=70,
        text="แยกพระขโนง",
        showarrow=False,
        font=dict(
            family='Courier New, monospace',
            size=18,
        )
    )


def plot_line_csv(df, date):
    fig = px.line(df, x="lon3", y="speed_km/h", title='ค.เร็วเฉลี่ย(km/h) ทุกๆ100เมตร ',color = "direction",animation_frame="round_min")
    annotate_line(fig, 'Speed line', date)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    return fig

def plot_line(df, date):
    fig = px.line(df, x="lon3", y="speed_kph", title='ค.เร็วเฉลี่ย(km/h) ทุกๆ100เมตร ',color = "direction")
    annotate_line(fig, 'Speed line', date)
    return fig
    
def plot_line_pred(df, date):
    fig = px.line(df, x="lon3", y="speed_kph", title='ค.เร็วเฉลี่ย(km/h) ทุกๆ100เมตร ',color = "direction",animation_frame="time")
    annotate_line(fig, 'Speed line prediction', date)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    return fig