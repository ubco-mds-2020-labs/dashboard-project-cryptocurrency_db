import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
#from vega_datasets import data
import pandas as pd
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Read in global data
source1 = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/price.csv", index_col=0)
crypto_usd_df = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/raw_data/crypto_usd.csv")
usd_exchange_rate_df = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/raw_data/usd_exchange_rate.csv")
source3 = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/data3.csv")
#source3 = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/ExchangeRate.csv")
#source3 = source3[['From Currency','To Currency', 'ExchangeRate']]
ratings = source1['Name'].unique()

crypto_usd = crypto_usd_df.set_index('CRYPTOCURRENCY').T.to_dict('list')
crypto_usd = {k:v[0] for k,v in crypto_usd.items()}

usd_exchange_rate = usd_exchange_rate_df.set_index('TO_CURRENCY').T.to_dict('list')
usd_exchange_rate = {k:v[0] for k,v in usd_exchange_rate.items()}


# Setup app and layout/frontend
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



alt.data_transformers.disable_max_rows()
brush = alt.selection_interval()  # selection of type "interval"
app.layout = html.Div(children=
    [
        html.Div(
                [
                    html.H1('Cryptocurrency Reporting Dashboard', style={'color': '#04EFB2', 'fontSize': 35, 'text-align': 'center'}),
                    html.P('Cryptocurrency is a form of payment that can be exchanged online for goods and services. Many companies have issued their own currencies, often called tokens, and these can be traded specifically for the good or service that the company provides. Think of them as you would arcade tokens or casino chips. You’ll need to exchange real currency for the cryptocurrency to access the good or service. Cryptocurrencies work using a technology called blockchain. Blockchain is a decentralized technology spread across many computers that manages and records transactions. Part of the appeal of this technology is its security.',
                    style={'color': 'white', 'fontSize': 15, 'text-align': 'center'}),
                    dcc.Dropdown(
                                id='ycol-widget', 
                                style={'float':'left', 'width': '40%'},
                                value='Close',  # REQUIRED to show the plot on the first page load
                                options=[{'label': col, 'value': col} for col in ['Open','Close','High','Low']]
                                ),
                    html.Div(children=
                            [
                                html.Iframe(
                                id='graph1',
                                style={'border-width': '0', 'width': '100%', 'height': '400px', 'float':'right'}
                                ),
                            ])   
                                
                ]
                ),
        html.Div(
                [
                    html.H1('Volume comparison of cryptocurrencies', style={'color': 'white', 'fontSize': 35, 'text-align': 'center'}),
                    html.Iframe(
                                id='graph2',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                ),
                    html.P('')
                                
                ]
                ),
        html.Div(
                [
                    html.H1('Relation of all cryptocurrencies vs Bitcoin', style={'color': 'white', 'fontSize': 35, 'text-align': 'center'}),
                    html.Iframe(
                                id='graph3',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                ),
                    html.Iframe(
                                id='graph4',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                ),
                    html.Iframe(
                                id='graph5',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                ),
                    html.Iframe(
                                id='graph6',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                ),
                    html.P('')
                                
                ]
                ),
        html.Div(
                [
                    html.H1('Buying Option:', style={'color': 'white', 'fontSize': 35, 'text-align': 'left'}),
                                
                ]
                ),
        html.Div(
                [
                    html.Div(
                            [
                                html.H3('Select a cryptocurrency', style={'color': 'white', 'fontSize': 25, 'text-align': 'left'}),
                                html.Div(
                                        [
                                            dcc.Dropdown(
                                            id='currency-dropdown2',
                                            value= list(crypto_usd.keys())[0],  # REQUIRED to show the plot on the first page load
                                            options=[{'label': k, 'value': k} for k in crypto_usd.keys()],
                                            style={'width': '50%', 'float':'center', 'margin': 10}
                                            ),
                                        ]
                                        ),
                                html.H5('How many units would you like to purchase?', style={'color': 'white', 'fontSize': 20}),
                                html.Div(
                                        [
                                            dcc.Input(id='units', 
                                            value=1, 
                                            type='number',
                                            style={'width': '30%', 'float':'center', 'margin': 12})
                                        ]
                                ),
                            ]),
                    html.Div(
                            [
                                html.H3('Select your currency', style={'color': 'white', 'fontSize': 25}),
                                dcc.Dropdown(
                                            id='currency-dropdown3',
                                            value=list(usd_exchange_rate.keys())[0],  # REQUIRED to show the plot on the first page load
                                            options=[{'label': k, 'value': k} for k in usd_exchange_rate.keys()],
                                            style={'width': '40%', 'float':'center', 'margin': 10}
                                            ),
                                html.H5('You will have the pay the below amount in the above currency', 
                                        style={'color': 'white', 'fontSize': 20}),
                                html.Div(id='my-output',
                                         style={'color': 'white', 'fontSize': 25, 'margin': 12})
                            ], className="six columns"),
                ], className="row")
    ],
    style={'padding':10}
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
        ).configure(background='#D9E9F0')
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

@app.callback(
    Output('graph3', 'srcDoc'),
    Input('ycol-widget', 'value'))
def plot_altair3(ycol):
    chart3 = alt.Chart(source3).mark_circle(size=4, opacity=0.8).encode(
        alt.X(alt.repeat("column"), type='quantitative',scale=alt.Scale(zero=False)),
        alt.Y(alt.repeat("row"), type='quantitative',scale=alt.Scale(zero=False)),
        ).properties(
            width=250,
            height=250
            ).repeat(
                row=['bitcoin_MAvg_Close'],
                column=['bitcoin_cash_MAvg_Close',
       'bitconnect_MAvg_Close', 'dash_MAvg_Close', 'ethereum_MAvg_Close',
       ]
            ).configure_axis(labelFontSize=7, titleFontSize=7)
    return chart3.to_html()

@app.callback(
    Output('graph4', 'srcDoc'),
    Input('ycol-widget', 'value'))
def plot_altair4(ycol):
    chart4 = alt.Chart(source3).mark_circle(size=4, opacity=0.8).encode(
        alt.X(alt.repeat("column"), type='quantitative',scale=alt.Scale(zero=False)),
        alt.Y(alt.repeat("row"), type='quantitative',scale=alt.Scale(zero=False)),
        ).properties(
            width=250,
            height=250
            ).repeat(
                row=['bitcoin_MAvg_Close'],
                column=[
       'ethereum_classic_MAvg_Close', 'iota_MAvg_Close', 'litecoin_MAvg_Close',
       'monero_MAvg_Close']
            ).configure_axis(labelFontSize=7, titleFontSize=7)
    return chart4.to_html()

@app.callback(
    Output('graph5', 'srcDoc'),
    Input('ycol-widget', 'value'))
def plot_altair5(ycol):
    chart5 = alt.Chart(source3).mark_circle(size=4, opacity=0.8).encode(
        alt.X(alt.repeat("column"), type='quantitative',scale=alt.Scale(zero=False)),
        alt.Y(alt.repeat("row"), type='quantitative',scale=alt.Scale(zero=False)),
        ).properties(
            width=250,
            height=250
            ).repeat(
                row=['bitcoin_MAvg_Close'],
                column=['nem_MAvg_Close', 'neo_MAvg_Close',
       'numeraire_MAvg_Close', 'omisego_MAvg_Close']
            ).configure_axis(labelFontSize=7, titleFontSize=7)
    return chart5.to_html()

@app.callback(
    Output('graph6', 'srcDoc'),
    Input('ycol-widget', 'value'))
def plot_altair6(ycol):
    chart6 = alt.Chart(source3).mark_circle(size=4, opacity=0.8).encode(
        alt.X(alt.repeat("column"), type='quantitative',scale=alt.Scale(zero=False)),
        alt.Y(alt.repeat("row"), type='quantitative',scale=alt.Scale(zero=False)),
        ).properties(
            width=250,
            height=250
            ).repeat(
                row=['bitcoin_MAvg_Close'],
                column=['qtum_MAvg_Close',
       'ripple_MAvg_Close', 'stratis_MAvg_Close', 'waves_MAvg_Close']
            ).configure_axis(labelFontSize=7, titleFontSize=7)
    return chart6.to_html()



if __name__ == '__main__':
    app.run_server(debug=True)