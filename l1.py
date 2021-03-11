import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
#from vega_datasets import data
import pandas as pd
import dash_bootstrap_components as dbc


# Read in global data
source1 = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/price.csv", index_col=0)
unique_cryptocurrency = source1['Name'].unique()

# Setup app and layout/frontend
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = html.Div([
    html.Iframe(
        id='graph1',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}
                ),
    dcc.Dropdown(
        id='ycol-widget',
        value='Close',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in ['Open','Close','High','Low','Volume']]
                )
                    ])

# Set up callbacks/backend
@app.callback(
    Output('graph1', 'srcDoc'),
    Input('ycol-widget', 'value'))
def plot_altair(ycol):
    chart = alt.Chart(source1).mark_area(clip=True, opacity=0.6).encode(
        x=alt.X('New_date1', axis=alt.Axis(labels=False)),
        y=ycol,
        color='Name',
        tooltip=['Name','Date','Open','Close','Low','High','Volume']).properties(
        width=1250,
        height=300)

    return chart.to_html()




if __name__ == '__main__':
    app.run_server(debug=True)