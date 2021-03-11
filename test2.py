  
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np

source2 = pd.read_csv("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db/ExchangeRate.csv")
source2 = source2[['From Currency','To Currency', 'ExchangeRate']]
#unique_cryptocurrency = source1['Name'].unique()

app = dash.Dash()
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Select a cryptocurrency'),
            dcc.Dropdown(
                        id='FromCurrency',
                        value='bitcoin',  # REQUIRED to show the plot on the first page load
                        options=[{'label': col, 'value': col} for col in ['bitcoin', 'dash', 'bitcoin_cash', 'bitconnect', 'ethereum',
                                                                            'iota', 'litecoin', 'monero', 'nem', 'neo', 'numeraire', 'omisego',
                                                                                'qtum', 'ripple', 'stratis', 'waves']]
                        ),
            html.H4('How many units would you like to purchase?'),
            dcc.Input(id='widget-1', type="number")
                ], className="six columns"),
        html.Div([
            html.H3('Select your currency'),
            dcc.Dropdown(
                        id='ToCurrency',
                        value='CAD',  # REQUIRED to show the plot on the first page load
                        options=[{'label': col, 'value': col} for col in ['CAD', 'CNY', 'INR', 'USD', 'YEN']]
                        ),
            html.H4('You will have to pay the below amount in the above currency'),
            dcc.Textarea(id='widget-2')
                ], className="six columns"),
    ], className="row")
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
@app.callback(
    Output('widget-2', 'value'),
    Input('widget-1', 'value'))
def update_output(input_value):
    x = input_value+input_value
    return 'You have entered: \n{}'.format(x)

if __name__ == '__main__':
    app.run_server(debug=True)