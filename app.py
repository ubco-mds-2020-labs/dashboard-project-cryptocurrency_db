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



alt.data_transformers.disable_max_rows()
brush = alt.selection_interval()  # selection of type "interval"
app.layout = html.Div(children=
