import dash

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.config.suppress_callback_exceptions = True

colors = {
    'background': '#E8EAF6',
    'text': '#7FDBFF'
}