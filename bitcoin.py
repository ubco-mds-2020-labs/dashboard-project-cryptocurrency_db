import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc
import pandas as pd


# Read in global data
cars = pd.read_csv("data.csv")

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1('My mudplank'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='xcol-widget',
                value='Date',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in cars.columns]),
            dcc.Dropdown(
                id='ycol-widget',
                value='Bitcoin_CLOSE',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in cars.columns])],
            md=4),
        dbc.Col(
            html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100%', 'height': '400px'}))])])
# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(cars).mark_point().encode(
        x=xcol,
        y=ycol,
        tooltip='Bitcoin_CLOSE').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)