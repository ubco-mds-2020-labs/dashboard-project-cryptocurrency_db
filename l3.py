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
crypto_usd_df = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/raw_data/crypto_usd.csv")
usd_exchange_rate_df = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/raw_data/usd_exchange_rate.csv")
#We are not using source2 = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/data2.csv", index_col=0)
source3 = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/ExchangeRate.csv")
source3 = source3[['From Currency','To Currency', 'ExchangeRate']]
ratings = source1['Name'].unique()

crypto_usd = crypto_usd_df.set_index('CRYPTOCURRENCY').T.to_dict('list')
crypto_usd = {k:v[0] for k,v in crypto_usd.items()}

usd_exchange_rate = usd_exchange_rate_df.set_index('TO_CURRENCY').T.to_dict('list')
usd_exchange_rate = {k:v[0] for k,v in usd_exchange_rate.items()}


# Setup app and layout/frontend
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Plot static graphs here


alt.data_transformers.disable_max_rows()
brush = alt.selection_interval()  # selection of type "interval"
app.layout = html.Div(children=
    [
        html.Div(
                [
                    html.H1('Cryptocurrency Reporting Dashboard', style={'color': 'white', 'fontSize': 35}),
                    dcc.Dropdown(
                                id='ycol-widget',
                                value='Close',  # REQUIRED to show the plot on the first page load
                                options=[{'label': col, 'value': col} for col in ['Open','Close','High','Low']]
                                ),
                    html.Iframe(
                                id='graph1',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                ),
                    html.P('')
                                
                ]
                ),
        html.Div(
                [
                    html.H1('Volume comparison of cryptocurrencies', style={'color': 'white', 'fontSize': 35}),
                    html.Iframe(
                                id='graph2',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                ),
                    html.P('')
                                
                ]
                ),
        html.Div(
                [
                    html.Div(
                            [
                                html.H3('Select a cryptocurrency', style={'color': 'white', 'fontSize': 35, 'margin':25}),
                                dcc.Dropdown(
                                            id='currency-dropdown2',
                                            value= list(crypto_usd.keys())[0],  # REQUIRED to show the plot on the first page load
                                            options=[{'label': k, 'value': k} for k in crypto_usd.keys()]
                                            ),
                                html.H4('How many units would you like to purchase?', style={'color': 'white', 'fontSize': 20, 'margin':25}),
                                dcc.Input(id='units', value=1, type='number')
                            ], className="six columns"),
                    html.Div(
                            [
                                html.H3('Select your currency', style={'color': 'white', 'fontSize': 35, 'margin':25}),
                                dcc.Dropdown(
                                            id='currency-dropdown3',
                                            value=list(usd_exchange_rate.keys())[0],  # REQUIRED to show the plot on the first page load
                                            options=[{'label': k, 'value': k} for k in usd_exchange_rate.keys()]
                                            ),
                                html.H4('You will have to pay the below amount in the above currency', style={'color': 'white', 'fontSize': 20, 'margin':25}),
                                html.Div(id='my-output')
                            ], className="six columns"),
                ], className="row")
    ]
)

# Set up callbacks/backend
@app.callback(
    Output('graph1', 'srcDoc'),
    Input('ycol-widget', 'value'))
def plot_altair(ycol):
    chart = alt.Chart(source1).mark_line(clip=True, size=3).encode(
        x=alt.X('New_date1', axis=alt.Axis(labels=False)),
        y=ycol,
        color='Name',
        tooltip=['Name','Date','Open','Close','Low','High']).properties(
        width=1250,
        height=300).add_selection(
        brush
        )
    return chart.to_html()

@app.callback(
    Output('graph2', 'srcDoc'),
    Input('ycol-widget', 'value'))
def plot_altair2(ycol):
    chart2 = alt.Chart(source1).mark_bar(clip=True).encode(
        x=alt.X('New_date1', axis=alt.Axis(labels=False)),
        y="Volume",
        color="Name",
        tooltip=['Name','Volume'],
        ).properties(
        width=1150,
        height=300)
        
    return chart2.to_html()

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='currency-dropdown2', component_property='value'),
    Input(component_id='currency-dropdown3', component_property='value'),
    Input(component_id='units', component_property='value')]
)
def update_output_div(crypto_name, curr_name, units):
    total_cost = round(float(crypto_usd[crypto_name]) * float(usd_exchange_rate[curr_name]) * float(units),1)
    return 'Total Cost: {}'.format(total_cost)





if __name__ == '__main__':
    app.run_server(debug=True)