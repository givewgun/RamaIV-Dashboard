import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
from app import app
from tabs import tab_1
from tabs import tab_2
from tabs import tab_3
import datetime


server = app.server

app.layout = html.Div(
    [
        html.Div(
            className="row header",
            children=[
                html.Button(id="menu", children=dcc.Markdown("&#8801")),
                html.Span(
                    className="app-title",
                    children=[
                        dcc.Markdown("**RAMA 4 Dashboard**"),
                    ],
                ),
                # html.Span(
                #     className="app-title",
                #     children=[
                #         html.Div(id='live-update-text'),
                #         dcc.Interval(
                #             id='current-time-interval',
                #             interval=1*1000, # in milliseconds
                #             n_intervals=0
                #         ),
                #     ],
                # ),
                html.Img(src=app.get_asset_url("Logo.jpg"), style={'height':'15%', 'width':'15%'}),
                html.A(
                    id="learn_more",
                    children=html.Button("Learn More"),
                    href="https://plot.ly/dash/",
                ),
            ],
        ),
        html.Div(
            id="tabs",
            className="row tabs",
            children=[
                dcc.Link("Live update", href="/"),
                dcc.Link("Forecast", href="/"),
                dcc.Link("Historical", href="/"),
            ],
        ),
        html.Div(
            id="mobile_tabs",
            className="row tabs",
            style={"display": "none"},
            children=[
                dcc.Link("Live update", href="/"),
                dcc.Link("Forecast", href="/"),
                dcc.Link("Historical", href="/"),
            ],
        ),
        dcc.Location(id="url", refresh=False),
        html.Div(id="tab_content"),
        html.Link(
            href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",
            rel="stylesheet",
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"
        ),

    ],
    className="row",
    style={"margin": "0%"},

    
)

# @app.callback(Output('live-update-text', 'children'),
#               [Input('current-time-interval', 'n_intervals')])
# def update_time(n):
#     now = datetime.datetime.now()
#     cur_time = now.strftime("%H:%M")
#     # style = {'padding': '5px', 'fontSize': '16px'}

#     return html.P(children=[html.Small("Now : " + cur_time)])     

@app.callback(
    [
        Output("tab_content", "children"),
        Output("tabs", "children"),
        Output("mobile_tabs", "children"),
    ],
    [Input("url", "pathname")],
)
def display_page(pathname):
    tabs = [
        dcc.Link("Live update", href="/live"),
        dcc.Link("Forecast", href="/forecast"),
        dcc.Link("Historical", href="/history"),
        # dcc.Link("Cases", href="/dash-salesforce-crm/cases"),
    ]
    if pathname == "/live":
        tabs[0] = dcc.Link(
            dcc.Markdown("**&#9632 Live update**"),
            href="/live",
        )
        return tab_1.layout, tabs, tabs
    elif pathname == "/forecast":
        # print("forecast")
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 Forecast**"), 
            href="/forecast",
        )
        return tab_2.layout, tabs, tabs
    elif pathname == "/history":
        tabs[2] = dcc.Link(
            dcc.Markdown("**&#9632 Historical**"), 
            href="/history",
        )
        return tab_3.layout, tabs, tabs
    else:
        tabs[0] = dcc.Link(
            dcc.Markdown("**&#9632 Live update**"),
            href="/live",
        )
        return tab_1.layout, tabs, tabs
        # tabs[0] = dcc.Link(
        #     dcc.Markdown("**&#9632 Live update**"),
        #     href="/live",
        # )
        # return tab_1.layout, tabs, tabs
    # tabs[1] = dcc.Link(
    #     dcc.Markdown("**&#9632 Leads**"), href="/dash-salesforce-crm/leads"
    # )
    # return tab_1.layout, tabs, tabs


@app.callback(
    Output("mobile_tabs", "style"),
    [Input("menu", "n_clicks")],
    [State("mobile_tabs", "style")],
)
def show_menu(n_clicks, tabs_style):
    if n_clicks:
        if tabs_style["display"] == "none":
            tabs_style["display"] = "flex"
        else:
            tabs_style["display"] = "none"
    return tabs_style


if __name__ == '__main__':
     app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)